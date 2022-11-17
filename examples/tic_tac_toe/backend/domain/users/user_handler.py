from dataclasses import replace

from domain.users.commands import CreateUser, UpdateUser
from domain.users.events import UserCreated, UserUpdated
from domain.users.queries import GetUser
from domain.users.user import User
from domain.users.user_repository import ById
from plum import dispatch

from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher


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

    @dispatch
    @state_fetcher(ById)
    def handle(self, state: User, effect: GetUser):
        return {"user": state, "parent_operation_id": effect.operation_id}
