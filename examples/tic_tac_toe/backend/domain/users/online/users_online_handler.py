from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

from domain.games.types import UserId
from domain.users.online.events import UserConnected, UsersOnlineUpdated
from domain.users.online.queries import GetUsersOnline
from injector import inject
from plum import dispatch

from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher, Singleton
from mani.domain.time.wall_clock import WallClock


@dataclass(frozen=True)
class UsersOnlineState:
    online_users: Dict[UserId, datetime] = field(default_factory=dict)


class UsersOnlineHandler(ManagedStateEffectHandler):
    @inject
    def __init__(self, clock: WallClock):
        self._clock = clock

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, state: UsersOnlineState | None, effect: UserConnected):
        if not state:
            state = UsersOnlineState()
        state.online_users[effect.id] = self._clock.now()
        return state, [
            UsersOnlineUpdated(online_users=list(state.online_users.keys()), parent_operation_id=effect.operation_id)]

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, state: UsersOnlineState | None, effect: GetUsersOnline) -> Dict:
        return {"online_users": list(state.online_users.keys()) if state else [],
                "parent_operation_id": effect.operation_id}
