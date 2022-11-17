from dataclasses import replace

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import CreateGame, PlaceMark, JoinGame
from domain.games.tic_tac_toe.events import GameCreated, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded, GameStarted, MarkPlaced, TurnTimeout
from domain.games.tic_tac_toe.game import GameWaitingForPlayers, GameInProgress
from domain.games.tic_tac_toe.game_repository import ByGameId
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from domain.operation_id import OperationId
from domain.users.events import PlayerJoinedAGame
from plum import dispatch

from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from mani.domain.cqrs.bus.state_management.evolve import evolve
from mani.domain.cqrs.event_scheduler.commands import ScheduleEvent, CancelScheduledEvents
from mani.domain.time.units import Millisecond


class TicTacToeGame(ManagedStateEffectHandler):
    turn_timeout = Millisecond(20000)

    @dispatch
    def handle(self, command: CreateGame):
        current_game = GameWaitingForPlayers(id=command.game_id)
        return current_game, [
            GameCreated(game_id=current_game.id,
                        creator=command.creator,
                        stage=GameStage.WAITING_FOR_PLAYERS,
                        parent_operation_id=command.operation_id)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameWaitingForPlayers, effect: JoinGame):
        number_of_players = len(state.players)
        if number_of_players == 0:
            next_state = replace(state, players=[*state.players, effect.player_id])
            return next_state, [
                PlayerJoinedAGame(game_id=next_state.id, player_id=effect.player_id,
                                  parent_operation_id=effect.operation_id)]
        elif number_of_players == 1:
            next_state = evolve(state, GameInProgress,
                                players=[*state.players, effect.player_id],
                                board=TicTacToeBoard(),
                                stage=GameStage.IN_PROGRESS,
                                waiting_for_player=state.players[0])
            return next_state, [
                PlayerJoinedAGame(game_id=next_state.id, player_id=effect.player_id,
                                  parent_operation_id=effect.operation_id),
                GameStarted(game_id=next_state.id, players=next_state.players, board=next_state.board.to_list()),
                *self._next_turn(next_state)
            ]
        else:
            return state, [
                GameErrorOccurred(reason=GameErrorReasons.ALL_PLAYERS_ALREADY_JOINED,
                                  parent_operation_id=effect.operation_id,
                                  player=effect.player_id, game_id=effect.game_id)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameInProgress, command: PlaceMark):
        error_effects = []
        final_effects = [CancelScheduledEvents(operation_id=OperationId(), key=str(state.id))]
        if state.waiting_for_player != command.player:
            error_effects += [GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                                player=command.player,
                                                game_id=state.id,
                                                parent_operation_id=command.operation_id)]
        elif state.board.is_off_limits(command.x, command.y):
            error_effects += [GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                                player=command.player,
                                                game_id=state.id,
                                                parent_operation_id=command.operation_id
                                                )]
        elif not state.board.is_cell_free(command.x, command.y):
            error_effects += [GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                                                player=command.player,
                                                game_id=state.id,
                                                parent_operation_id=command.operation_id)]
        elif state.stage != GameStage.IN_PROGRESS:
            error_effects += [GameErrorOccurred(reason=GameErrorReasons.GAME_ALREADY_ENDED,
                                                player=command.player,
                                                game_id=state.id,
                                                parent_operation_id=command.operation_id)]
        if error_effects:
            return state, error_effects + final_effects

        next_state = state.place(command.player, command.x, command.y)
        stage = next_state.stage
        if stage == GameStage.IN_PROGRESS:
            next_effects = self._next_turn(next_state)
        else:
            next_effects = [GameEnded(game_id=next_state.id,
                                      result=stage,
                                      winner=next_state.winner)]
        return next_state, [
            *final_effects,
            MarkPlaced(game_id=next_state.id, player=command.player, x=command.x, y=command.y,
                       parent_operation_id=command.operation_id),
            BoardUpdated(game_id=next_state.id, board=next_state.board.to_list()),
            *next_effects,
        ]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameInProgress, command: TurnTimeout):
        next_state = state.cancel_game()
        return next_state, [GameEnded(game_id=next_state.id,
                                      result=next_state.stage,
                                      winner=next_state.winner)]

    def _next_turn(self, state: GameInProgress):
        return [
            WaitingForPlayerPlay(game_id=state.id, player_id=state.waiting_for_player, timeout=self.turn_timeout),
            ScheduleEvent(TurnTimeout(game_id=state.id, player_id=state.waiting_for_player),
                          operation_id=OperationId(), key=str(state.id), when=self.turn_timeout)
        ]
