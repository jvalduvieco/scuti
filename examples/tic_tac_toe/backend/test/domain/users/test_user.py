from datetime import datetime

from domain.games.types import UserId
from domain.operation_id import OperationId
from domain.users.commands import CreateUser, UpdateUser
from domain.users.events import UserCreated, UserUpdated
from domain.users.user import User
from domain.users.user_handler import UserHandler

from scuti.domain.testing.test_cases.effect_handler_test_case import EffectHandlerTestCase


class UserTestCase(EffectHandlerTestCase):
    def setUp(self) -> None:
        self.a_user_handler = UserHandler()

    def test_can_be_created(self):
        a_user_id = UserId()
        operation_id = OperationId()
        now = datetime.now()
        state, effects = self.feed_effects(self.a_user_handler, [
            CreateUser(id=a_user_id, alias="foo", created_at=now, operation_id=operation_id)
        ])
        self.assertEqual(
            [UserCreated(user=User(id=a_user_id, alias="foo", created_at=now), parent_operation_id=operation_id)],
            effects)
        self.assertEqual(User(id=a_user_id, alias="foo", created_at=now), state)

    def test_can_be_modified(self):
        a_user_id = UserId()
        operation_id = OperationId()
        now = datetime.now()
        state, effects = self.feed_effects(self.a_user_handler, [
            CreateUser(id=a_user_id, alias="foo", created_at=now, operation_id=operation_id),
            UpdateUser(id=a_user_id, alias="bar", operation_id=operation_id)
        ])
        self.assertEqual(
            UserUpdated(user=User(id=a_user_id, alias="bar", created_at=now), parent_operation_id=operation_id),
            effects[-1])
        self.assertEqual(User(id=a_user_id, alias="bar", created_at=now), state)
