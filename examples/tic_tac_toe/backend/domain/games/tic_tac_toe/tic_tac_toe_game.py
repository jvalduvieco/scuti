from dataclasses import replace
from typing import List, Tuple

from plum import dispatch

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import CreateGame, JoinGame, PlaceMark
from domain.games.tic_tac_toe.events import BoardUpdated, GameCreated, GameEnded, GameErrorOccurred, GameStarted, \
    GameStateReadyToBeCleaned, MarkPlaced, TurnTimeout, WaitingForPlayerPlay
from domain.games.tic_tac_toe.game import GameInProgress, GameWaitingForPlayers
from domain.games.tic_tac_toe.game_repository import ByGameId
from domain.games.tic_tac_toe.types import GameErrorReasons, GameStage
from domain.operation_id import OperationId
from domain.users.events import PlayerJoinedAGame
from scuti.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from scuti.domain.cqrs.bus.state_management.commands import DeleteState
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from scuti.domain.cqrs.bus.state_management.evolve import evolve
from scuti.domain.cqrs.effects import Effect
from scuti.domain.cqrs.event_scheduler.commands import CancelScheduledEvents, ScheduleEvent
from scuti.domain.time.units import Millisecond


class TicTacToeGame(ManagedStateEffectHandler):
    """
    This is an "effect handler". Its mission is to receive effects and calculate state changes and create derived
    effects.
    These effect handlers can be used to:
     - Tie an entity to the busses, so it can communicate with the outside world
     - As a saga to model a real world procedure
     - Just as a stateless command / event handler
     - As a projection that adapts internal data model to the client needs
    """
    turn_timeout = Millisecond(20000)

    @dispatch
    def handle(self, command: CreateGame):
        """
        Create one `handle` method for every effect type you want to handle. In this case the effect `CreateGame` is
        a creational effect, so it creates a new entity so there is no previous state.
        You will receive the event in this method parameters and Scuti expects you to return a tuple containing next
        state and a list of effects that have been generated as `CreateGame` consequences.
        """
        next_state = GameWaitingForPlayers(id=command.game_id)
        return next_state, [
            GameCreated(game_id=next_state.id,
                        creator=command.creator,
                        stage=GameStage.WAITING_FOR_PLAYERS,
                        parent_operation_id=command.operation_id)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameWaitingForPlayers, effect: JoinGame) -> Tuple[GameWaitingForPlayers | GameInProgress,
                                                                              List[Effect]]:
        """
        When an entity has already been created Scuti needs some way to decide how current state should be retrieved
        based on the effect being handled. This is the mission of `state_fetcher` annotation.
        Creating state fetchers requires creating a function that will receive the current effect being handled,
        the repo associated to this effect handler and it is expected to return current state for this entity.
        So something like:
        ```python
        ByGameId = lambda eff, repo: repo.by_id(eff.game_id)
        ```
        When there is a state fetcher `handle` signature changes to receive state as a first parameter.
        In this case we're using several state types to represent the game stages. To change the type of the state
        use the helper function `evolve`. With these types you can have specific effect handlers for a given stage
        of the entity.
        See: [[domain/games/tic_tac_toe/game.py]]
        """
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
    def handle(self, state: GameInProgress, command: PlaceMark) -> Tuple[GameInProgress, List[Effect]]:
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
            # You can use functions to create you list of effects
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
    def handle(self, state: GameInProgress, command: TurnTimeout) -> Tuple[GameInProgress, List[Effect]]:
        next_state = state.cancel_game()
        return next_state, [GameEnded(game_id=next_state.id,
                                      result=next_state.stage,
                                      winner=next_state.winner)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameInProgress, event: GameEnded) -> Tuple[GameInProgress, List[Effect]]:
        """
        You can listen to your own events. Usually in these cases it is more efficient to extract a function that
        creates all derived events/commands.
        """
        return state, [ScheduleEvent(GameStateReadyToBeCleaned(game_id=event.game_id),
                                     when=Millisecond(10000), key=str(event.game_id),
                                     operation_id=OperationId())]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: GameInProgress, event: GameStateReadyToBeCleaned) -> Tuple[None, List[Effect]]:
        """
        You can delete states by issuing a `DeleteState` command
        """
        return None, [DeleteState(state.id)]

    def _next_turn(self, state: GameInProgress):
        return [
            WaitingForPlayerPlay(game_id=state.id, player_id=state.waiting_for_player, timeout=self.turn_timeout),
            # You can schedule events for the future
            ScheduleEvent(TurnTimeout(game_id=state.id, player_id=state.waiting_for_player),
                          operation_id=OperationId(), key=str(state.id), when=self.turn_timeout)
        ]
