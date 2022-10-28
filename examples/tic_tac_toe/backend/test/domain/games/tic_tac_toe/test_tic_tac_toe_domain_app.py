from typing import List

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from domain.games.tic_tac_toe.domain_module import TicTacToeDomainModule
from domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from domain.games.tic_tac_toe.types import GameErrorReasons, GameStage
from domain.games.types import GameId, PlayerId
from domain.operation_id import OperationId
from hamcrest import has_items, has_item
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Effect
from mani.domain.testing.test_cases.domain_test_case import DomainTestCase
from mani.infrastructure.tools.list import filter_none


class TestTicTacToeApp(DomainTestCase):
    modules = [TicTacToeDomainModule]

    def setUp(self) -> None:
        super().setUp()
        self.a_game = TicTacToeGame()
        self.game_id = GameId()
        self.first_player = PlayerId()
        self.second_player = PlayerId()

    def test_a_game_can_be_started(self):
        operation_id = OperationId()
        self.feed_effects([
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player)]
        )

        self.assertThatHandledEffects(
            has_items(GameStarted(game_id=self.game_id,
                                  first_player=self.first_player,
                                  second_player=self.second_player,
                                  board=TicTacToeBoard().to_list(),
                                  stage=GameStage.IN_PROGRESS,
                                  parent_operation_id=operation_id),
                      BoardUpdated(game_id=self.game_id, board=TicTacToeBoard().to_list()),
                      WaitingForPlayerPlay(game_id=self.game_id, player_id=self.first_player)))

    def test_a_player_can_win_the_game_if_manages_to_place_three_marks_in_a_row(self):
        self.feed_effects([
            NewGame(game_id=self.game_id, operation_id=OperationId(), first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=2),
        ])

        self.assertThatHandledEffects(has_item(
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player)))
