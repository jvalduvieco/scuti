from datetime import datetime

from domain.games.scoring.domain_module import ScoringDomainModule
from domain.games.scoring.events import PlayerScoreChanged
from domain.games.scoring.queries import GetTopThreePlayers
from domain.games.scoring.user_score import UserScore
from domain.games.tic_tac_toe.events import GameEnded
from domain.games.tic_tac_toe.types import GameStage
from domain.games.types import UserId, GameId
from domain.operation_id import OperationId
from domain.users.domain_module import UserDomainModule
from domain.users.events import UserCreated
from domain.users.user import User
from hamcrest import has_item, not_, instance_of
from mani.domain.testing.test_cases.domain_test_case import DomainTestCase


class ScoringTestCase(DomainTestCase):
    modules = [UserDomainModule, ScoringDomainModule]

    def setUp(self) -> None:
        super().setUp()
        self.game_id = GameId()
        self.first_player = UserId()
        self.second_player = UserId()

    def test_can_record_a_win(self):
        self.feed_effects([
            UserCreated(user=User(
                id=self.first_player,
                alias='foo',
                created_at=datetime.now()),
                parent_operation_id=OperationId()),
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player)
        ])
        self.assertThatHandledEffects(has_item(PlayerScoreChanged(player_id=self.first_player, score=100)))

    def test_can_record_a_draw(self):
        self.feed_effects([
            GameEnded(game_id=self.game_id, result=GameStage.DRAW, winner=None)
        ])
        self.assertThatHandledEffects(not_(instance_of(PlayerScoreChanged)))

    def test_can_query_top_three(self):
        self.feed_effects([
            UserCreated(user=User(
                id=self.first_player,
                alias='foo',
                created_at=datetime.now()),
                parent_operation_id=OperationId()),
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player),
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player)
        ])
        operation_id = OperationId()
        response = self.make_query(GetTopThreePlayers(operation_id=operation_id))
        self.assertThatHandledEffects(has_item(PlayerScoreChanged(player_id=self.first_player, score=100)))
        self.assertEqual(
            {"list": [UserScore(id=self.first_player, score=200)], "parent_operation_id": operation_id},
            response)
