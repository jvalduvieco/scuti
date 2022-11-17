from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import CreateGame, PlaceMark, JoinGame
from domain.games.tic_tac_toe.events import GameCreated, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded, GameStarted, MarkPlaced, TurnTimeout
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from domain.games.tic_tac_toe.types import GameErrorReasons, GameStage
from domain.games.types import GameId, UserId
from domain.operation_id import OperationId
from domain.users.events import PlayerJoinedAGame

from mani.domain.cqrs.event_scheduler.commands import ScheduleEvent, CancelScheduledEvents
from mani.domain.testing.matchers.any_id import match_any_id
from mani.domain.testing.test_cases.effect_handler_test_case import EffectHandlerTestCase
from mani.domain.time.units import Millisecond


class TestTicTacToeGame(EffectHandlerTestCase):
    def setUp(self) -> None:
        self.a_game = TicTacToeGame()
        self.game_id = GameId()
        self.first_player = UserId()
        self.second_player = UserId()

    def test_a_game_can_be_started(self):
        operation_id = OperationId()
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player)
        ])

        self.assertEqual([GameCreated(game_id=self.game_id,
                                      creator=self.first_player,
                                      stage=GameStage.WAITING_FOR_PLAYERS,
                                      parent_operation_id=operation_id)],
                         effects)

    def test_a_player_can_play_if_it_is_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.first_player, x=0, y=0)
        ])

        turn_timeout = Millisecond(20000)
        self.assertEqual([GameCreated(game_id=self.game_id,
                                      creator=self.first_player,
                                      stage=GameStage.WAITING_FOR_PLAYERS,
                                      parent_operation_id=operation_id),
                          PlayerJoinedAGame(game_id=self.game_id, player_id=self.first_player,
                                            parent_operation_id=match_any_id(OperationId)),
                          PlayerJoinedAGame(game_id=self.game_id, player_id=self.second_player,
                                            parent_operation_id=match_any_id(OperationId)),
                          GameStarted(game_id=self.game_id, players=[self.first_player, self.second_player],
                                      board=TicTacToeBoard().to_list()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.first_player,
                                               timeout=turn_timeout),
                          ScheduleEvent(event=TurnTimeout(game_id=self.game_id,
                                                          player_id=self.first_player),
                                        when=turn_timeout,
                                        key=str(self.game_id),
                                        operation_id=match_any_id(OperationId)),
                          CancelScheduledEvents(operation_id=match_any_id(OperationId), key=str(self.game_id)),
                          MarkPlaced(game_id=self.game_id,
                                     player=self.first_player,
                                     x=0,
                                     y=0,
                                     parent_operation_id=match_any_id(OperationId)),

                          BoardUpdated(game_id=self.game_id,
                                       board=TicTacToeBoard(cells={(0, 0): self.first_player}).to_list()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.second_player,
                                               timeout=turn_timeout),
                          ScheduleEvent(event=TurnTimeout(game_id=self.game_id,
                                                          player_id=self.second_player),
                                        when=turn_timeout,
                                        key=str(self.game_id),
                                        operation_id=match_any_id(OperationId)),
                          ],
                         effects)

    def test_a_player_can_not_play_if_it_is_not_her_turn(self):
        operation_id = OperationId()
        another_operation_id = OperationId()
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
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
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
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
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=operation_id, creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
            PlaceMark(game_id=self.game_id, operation_id=another_operation_id, player=self.first_player, x=3, y=3)
        ])

        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                          player=self.first_player,
                                          game_id=self.game_id,
                                          parent_operation_id=another_operation_id)
                        in effects)

    def test_a_player_can_win_the_game_if_manages_to_place_three_marks_in_a_row(self):
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=OperationId(), creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
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
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=OperationId(), creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
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
        state, effects = self.feed_effects(self.a_game, [
            CreateGame(game_id=self.game_id, operation_id=OperationId(), creator=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.first_player),
            JoinGame(game_id=self.game_id, operation_id=OperationId(), player_id=self.second_player),
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
