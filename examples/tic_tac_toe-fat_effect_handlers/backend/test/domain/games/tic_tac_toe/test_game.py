from typing import List
from unittest import TestCase

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from domain.games.tic_tac_toe.types import GameErrorReasons, GameStage
from domain.games.types import GameId, PlayerId
from domain.operation_id import OperationId
from infrastructure.domain.tic_tac_toe.game_repository_in_memory import GameRepositoryInMemory
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Effect
from test.tools.simple_fake_event_bus import SimpleFakeEventBus
from mani.infrastructure.tools.list import filter_none


class TestTicTacToeGame(TestCase):
    def setUp(self) -> None:
        self.a_game = TicTacToeGame()
        self.game_id = GameId()
        self.first_player = PlayerId()
        self.second_player = PlayerId()

    def test_a_game_can_be_started(self):
        operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player)
        ])

        self.assertEqual([GameStarted(game_id=self.game_id,
                                      first_player=self.first_player,
                                      second_player=self.second_player,
                                      board=TicTacToeBoard().to_list(),
                                      stage=GameStage.IN_PROGRESS,
                                      parent_operation_id=operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard().to_list()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.first_player)],
                         effects)

    def test_a_player_can_play_if_it_is_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.first_player, x=0, y=0)
        ])

        self.assertEqual([GameStarted(game_id=self.game_id,
                                      first_player=self.first_player,
                                      second_player=self.second_player,
                                      board=TicTacToeBoard().to_list(),
                                      stage=GameStage.IN_PROGRESS,
                                      parent_operation_id=operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard().to_list()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.first_player),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.second_player),
                          BoardUpdated(game_id=self.game_id,
                                       board=TicTacToeBoard(cells={(0, 0): self.first_player}).to_list()),
                          ],
                         effects)

    def test_a_player_can_not_play_if_it_is_not_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.second_player, x=0, y=0)
        ])

        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                          player=self.second_player,
                                          game_id=self.game_id,
                                          parent_operation_id=another_operation_id)
                        in effects)

    def test_a_player_can_not_play_to_an_already_filled_position(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        yet_another_operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=yet_another_operation_id, player=self.second_player, x=0,
                      y=0)
        ])

        self.assertTrue(
            GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                              player=self.second_player,
                              game_id=self.game_id,
                              parent_operation_id=yet_another_operation_id)
            in effects)

    def test_a_player_can_not_play_off_the_limits(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.first_player, x=3, y=3)
        ])

        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                          player=self.first_player,
                                          game_id=self.game_id,
                                          parent_operation_id=another_operation_id)
                        in effects)

    def test_a_player_can_win_the_game_if_manages_to_place_three_marks_in_a_row(self):
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=OperationId(), first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=2),
        ])

        self.assertTrue(
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.first_player)
            in effects)

    def test_game_end_in_draw_if_board_is_filled_and_not_player_has_three_in_a_row(self):
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=OperationId(), first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=2, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=2, y=2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=1, y=2),
        ])

        self.assertTrue(
            GameEnded(game_id=self.game_id, result=GameStage.DRAW, winner=None)
            in effects)

    def test_a_player_can_not_play_if_game_has_ended(self):
        last_operation_id = OperationId()
        state, effects = self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=OperationId(), first_player=self.first_player,
                    second_player=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.second_player, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player=self.first_player, x=0, y=2),
            PlaceMark(game_id=self.game_id, operation_id=last_operation_id, player=self.second_player, x=1, y=2),
        ])

        self.assertTrue(
            GameErrorOccurred(game_id=self.game_id, player=self.second_player, parent_operation_id=last_operation_id,
                              reason=GameErrorReasons.GAME_ALREADY_ENDED)
            in effects)

    def __feed_effects(self, into: EffectHandler, effects: List[Effect]):
        current_state = None
        emitted_effects = []
        for effect in effects:
            if current_state is not None:
                state, effects = into.handle(current_state, effect)
            else:
                state, effects = into.handle(effect)
            current_state = state
            emitted_effects += filter_none(effects)
        return current_state, emitted_effects
