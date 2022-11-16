from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import CreateGame, PlaceMark, JoinGame
from domain.games.tic_tac_toe.domain_module import TicTacToeDomainModule
from domain.games.tic_tac_toe.events import GameCreated, WaitingForPlayerPlay, GameEnded
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from domain.games.tic_tac_toe.types import GameStage
from domain.games.types import GameId, UserId
from domain.operation_id import OperationId
from hamcrest import has_items, has_item
from mani.domain.testing.test_cases.domain_test_case import DomainTestCase
from mani.domain.time.units import Millisecond


class TestTicTacToeApp(DomainTestCase):
    modules = [TicTacToeDomainModule]

    def setUp(self) -> None:
        super().setUp()
        self.a_game = TicTacToeGame()
        self.game_id = GameId()
        self.first_player = UserId()
        self.second_player = UserId()

    def test_a_game_can_be_started(self):
        operation_id = OperationId()
        self.feed_effects([
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player)
        ]
        )

        self.assertThatHandledEffects(
            has_items(GameCreated(game_id=self.game_id,
                                  creator=self.first_player,
                                  board=TicTacToeBoard().to_list(),
                                  stage=GameStage.WAITING_FOR_PLAYERS,
                                  parent_operation_id=operation_id),
                      WaitingForPlayerPlay(game_id=self.game_id, player_id=self.first_player,
                                           timeout=Millisecond(20000))))

    def test_a_player_can_win_the_game_if_manages_to_place_three_marks_in_a_row(self):
        self.feed_effects([
            CreateGame(game_id=self.game_id, operation_id=OperationId(), creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=2),
        ])

        self.assertThatHandledEffects(has_item(
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player)))
