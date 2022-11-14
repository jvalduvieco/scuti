from dataclasses import replace
from typing import List, Tuple

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import CreateGame, PlaceMark, JoinGame
from domain.games.tic_tac_toe.events import GameCreated, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded, GameStarted, MarkPlaced
from domain.games.tic_tac_toe.game import Game
from domain.games.tic_tac_toe.game_repository import ByGameId
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from domain.users.events import PlayerJoinedAGame
from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from mani.domain.cqrs.effects import Effect
from plum import dispatch


class TicTacToeGame(ManagedStateEffectHandler):

    @dispatch
    def handle(self, command: CreateGame):
        current_game = Game(id=command.game_id,
                            board=TicTacToeBoard(),
                            stage=GameStage.WAITING_FOR_PLAYERS)
        return current_game, [
            GameCreated(game_id=current_game.id,
                        board=current_game.board.to_list(),
                        creator=command.creator,
                        stage=current_game.stage,
                        parent_operation_id=command.operation_id)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: Game, effect: JoinGame) -> Tuple[Game, List[Effect]]:
        number_of_players = len(state.players)
        if number_of_players == 0:
            new_state = replace(state, players=[*state.players, effect.player_id])
            return new_state, [
                PlayerJoinedAGame(game_id=new_state.id, player_id=effect.player_id,
                                  parent_operation_id=effect.operation_id)]
        elif number_of_players == 1:
            new_state = replace(state, players=[*state.players, effect.player_id], stage=GameStage.IN_PROGRESS,
                                waiting_for_player=state.players[0])
            return new_state, [
                PlayerJoinedAGame(game_id=new_state.id, player_id=effect.player_id,
                                  parent_operation_id=effect.operation_id),
                GameStarted(game_id=new_state.id, players=new_state.players, board=new_state.board.to_list()),
                WaitingForPlayerPlay(game_id=new_state.id, player_id=new_state.waiting_for_player)]
        else:
            return state, [
                GameErrorOccurred(reason=GameErrorReasons.ALL_PLAYERS_ALREADY_JOINED,
                                  parent_operation_id=effect.operation_id,
                                  player=effect.player_id, game_id=effect.game_id)]

    @dispatch
    @state_fetcher(ByGameId)
    def handle(self, state: Game, command: PlaceMark):
        error_effects = []
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
            return state, error_effects

        next_game_state = state.place(command.player, command.x, command.y)
        stage = next_game_state.stage
        return next_game_state, [
            MarkPlaced(game_id=next_game_state.id, player=command.player, x=command.x, y=command.y,
                       parent_operation_id=command.operation_id),
            WaitingForPlayerPlay(game_id=next_game_state.id, player_id=next_game_state.waiting_for_player),
            BoardUpdated(game_id=next_game_state.id, board=next_game_state.board.to_list()),
            GameEnded(game_id=next_game_state.id,
                      result=stage,
                      winner=next_game_state.winner) if stage != GameStage.IN_PROGRESS else None
        ]
