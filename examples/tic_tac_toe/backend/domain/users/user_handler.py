from dataclasses import replace

from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from plum import dispatch
from domain.users.user import User
from domain.users.commands import CreateUser, UpdateUser
from domain.users.events import UserCreated, UserUpdated
from domain.users.user_repository import ById


class UserHandler(ManagedStateEffectHandler):
    @dispatch
    def handle(self, effect: CreateUser):
        user = User(effect.id, effect.alias, effect.created_at)
        return user, [
            UserCreated(user=user, parent_operation_id=effect.operation_id)]

    @dispatch
    @state_fetcher(ById)
    def handle(self, state: User, effect: UpdateUser):
        updated_user = replace(state, alias=effect.alias)
        return updated_user, [UserUpdated(user=updated_user, parent_operation_id=effect.operation_id)]
