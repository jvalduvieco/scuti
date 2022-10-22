from typing import List
from unittest import TestCase

from backend.domain.games.tic_tac_toe.board import TicTacToeBoard
from backend.domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from backend.domain.games.tic_tac_toe.events import GameStarted, WaitingForPlayerPlay, BoardUpdated, GameErrorOccurred, \
    GameEnded
from backend.domain.games.tic_tac_toe.game import GameStage
from backend.domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from backend.domain.games.tic_tac_toe.types import GameErrorReasons
from backend.domain.games.types import GameId, PlayerId
from backend.domain.operatuion_id import OperationId
from backend.infrastructure.domain.tic_tac_toe.game_repository_in_memory import GameRepositoryInMemory
from backend.test.tools.simple_fake_event_bus import SimpleFakeEventBus
from domain.cqrs.bus.effect_handler import EffectHandler
from domain.cqrs.effects import Effect


class TestTicTacToeGame(TestCase):
    def setUp(self) -> None:
        self.event_bus = SimpleFakeEventBus()
        self.game_repository = GameRepositoryInMemory()
        self.a_game = TicTacToeGame(event_bus=self.event_bus, game_repository=self.game_repository)
        self.game_id = GameId()
        self.player_1 = PlayerId()
        self.player_2 = PlayerId()

    def test_a_game_can_be_started(self):
        operation_id = OperationId()
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, player_1=self.player_1, player_2=self.player_2)
        ])

        self.assertEqual([GameStarted(game_id=self.game_id,
                                      player_1=self.player_1,
                                      player_2=self.player_2,
                                      board=TicTacToeBoard(),
                                      parent_operation_id=operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.player_1)],
                         self.event_bus.emitted_events)

    def test_a_player_can_play_if_it_is_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player_id=self.player_1, x=0, y=0)
        ])

        self.assertEqual([GameStarted(game_id=self.game_id,
                                      player_1=self.player_1,
                                      player_2=self.player_2,
                                      board=TicTacToeBoard(),
                                      parent_operation_id=operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.player_1),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard(cells={(0, 0): self.player_1})),
                          ],
                         self.event_bus.emitted_events)

    def test_a_player_can_not_play_if_it_is_not_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player_id=self.player_2, x=0, y=0)
        ])

        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                          player=self.player_2,
                                          game_id=self.game_id,
                                          parent_operation_id=another_operation_id)
                        in self.event_bus.emitted_events)

    def test_a_player_can_not_play_to_an_already_filled_position(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        yet_another_operation_id = OperationId()
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player_id=self.player_1, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=yet_another_operation_id, player_id=self.player_2, x=0,
                      y=0)
        ])

        self.assertTrue(
            GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                              player=self.player_2,
                              game_id=self.game_id,
                              parent_operation_id=yet_another_operation_id)
            in self.event_bus.emitted_events)

    def test_a_player_can_not_play_off_the_limits(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=operation_id, player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player_id=self.player_1, x=3, y=3)
        ])

        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                          player=self.player_1,
                                          game_id=self.game_id,
                                          parent_operation_id=another_operation_id)
                        in self.event_bus.emitted_events)

    def test_a_player_can_win_the_game_if_manages_to_place_three_marks_in_a_row(self):
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=OperationId(), player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=0, y=2),
        ])

        self.assertTrue(
            GameEnded(game_id=self.game_id, result=GameStage.PLAYER_WON, winner=self.player_1)
            in self.event_bus.emitted_events)

    def test_game_end_in_draw_if_board_is_filled_and_not_player_has_three_in_a_row(self):
        self.__feed_effects(self.a_game, [
            NewGame(game_id=self.game_id, operation_id=OperationId(), player_1=self.player_1,
                    player_2=self.player_2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=0, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=1, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=2, y=0),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=0, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=2, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=1, y=1),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=0, y=2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_2, x=2, y=2),
            PlaceMark(game_id=self.game_id, operation_id=OperationId(), player_id=self.player_1, x=1, y=2),
        ])

        self.assertTrue(
            GameEnded(game_id=self.game_id, result=GameStage.DRAW, winner=None)
            in self.event_bus.emitted_events)

    def __feed_effects(self, into: EffectHandler, effects: List[Effect]):
        [into.handle(effect) for effect in effects]
