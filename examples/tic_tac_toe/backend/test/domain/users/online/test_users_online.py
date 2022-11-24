from domain.games.types import UserId
from domain.operation_id import OperationId
from domain.users.online.events import UserConnected, UserDisconnected
from domain.users.online.queries import GetUsersOnline
from domain.users.online.users_online_handler import UsersOnlineHandler, UsersOnlineState
from scuti.domain.testing.test_cases.effect_handler_test_case import EffectHandlerTestCase
from scuti.infrastructure.time.WallClock.fake_wall_clock import FakeWallClock
from test.tools.domain.fixtures import a_perfect_date_and_time


class UsersOnlineTestCase(EffectHandlerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.effect_handler = UsersOnlineHandler(FakeWallClock(a_perfect_date_and_time()))

    def test_when_a_user_connects_that_user_is_online(self):
        user_id = UserId()
        state, effects = self.feed_effects(self.effect_handler,
                                           [UserConnected(user_id, OperationId())],
                                           None)
        self.assertEqual(UsersOnlineState(online_users={user_id: a_perfect_date_and_time()}), state)

    def test_when_a_user_that_was_online_disconnects_that_user_is_no_longer_online(self):
        user_id = UserId()
        state, effects = self.feed_effects(self.effect_handler,
                                           [
                                               UserConnected(user_id, OperationId()),
                                               UserDisconnected(user_id, OperationId())
                                           ],
                                           None)
        self.assertEqual(UsersOnlineState(online_users={}), state)

    def test_can_query_online_users(self):
        state, effects = self.feed_effects(self.effect_handler,
                                           [UserConnected(UserId(), OperationId()),
                                            UserConnected(UserId(), OperationId())],
                                           None)
        answer = self.effect_handler.handle(state, GetUsersOnline(OperationId()))
        self.assertEqual(2, len(answer))
