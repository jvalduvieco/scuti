from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

from domain.games.types import UserId
from domain.users.online.events import UserConnected, UserDisconnected, UsersOnlineUpdated
from domain.users.online.queries import GetUsersOnline
from injector import inject
from plum import dispatch

from scuti.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher, Singleton
from scuti.domain.time.wall_clock import WallClock


@dataclass(frozen=True)
class UsersOnlineState:
    online_users: Dict[UserId, datetime] = field(default_factory=dict)


class UsersOnlineHandler(ManagedStateEffectHandler):
    @inject
    def __init__(self, clock: WallClock):
        """
        As you can see effect handlers dependencies can be injected
        """
        self._clock = clock

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, state: UsersOnlineState | None, effect: UserConnected):
        """
        These handlers act as a singleton, so there will be only one instance in the domain. A predefined
        `Singleton` state fetcher is available for you.
        In case multiple stages can be handled, use a Union
        """
        if not state:
            state = UsersOnlineState()
        state.online_users[effect.id] = self._clock.now()
        return state, [
            UsersOnlineUpdated(online_users=list(state.online_users.keys()), parent_operation_id=effect.operation_id)]

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, state: UsersOnlineState | None, effect: UserDisconnected):
        if not state:
            return state, []
        del state.online_users[effect.id]
        return state, [
            UsersOnlineUpdated(online_users=list(state.online_users.keys()), parent_operation_id=effect.operation_id)]

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, state: UsersOnlineState | None, effect: GetUsersOnline) -> Dict:
        """
        Handlers can also answer queries about its internal state. Usually query responses are modelled as
        dictionaries as this data is leaving the domain very quickly so no need for type hinting or synchronization
        between code in the domain. This is a developer decision, dataclasses could be used.
        """
        return {"online_users": list(state.online_users.keys()) if state else [],
                "parent_operation_id": effect.operation_id}
