from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from domain.games.tic_tac_toe.game import Game
from domain.games.tic_tac_toe.game_repository import ByGameId
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from plum import dispatch


class TicTacToeGame(EffectHandler):

    @dispatch
    def handle(self, command: NewGame):
        current_game = Game(id=command.game_id,
                            first_player=command.first_player,
                            second_player=command.second_player,
                            board=TicTacToeBoard(),
                            stage=GameStage.IN_PROGRESS,
                            waiting_for_player=command.first_player)
        return current_game, [
            GameStarted(game_id=current_game.id,
                        first_player=current_game.first_player,
                        second_player=current_game.second_player,
                        board=current_game.board.to_list(),
                        stage=current_game.stage,
                        parent_operation_id=command.operation_id),
            BoardUpdated(game_id=current_game.id, board=current_game.board.to_list()),
            WaitingForPlayerPlay(game_id=current_game.id,
                                 player_id=current_game.first_player)
        ]

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
            WaitingForPlayerPlay(game_id=next_game_state.id, player_id=next_game_state.waiting_for_player),
            BoardUpdated(game_id=next_game_state.id, board=next_game_state.board.to_list()),
            GameEnded(game_id=next_game_state.id,
                      result=stage,
                      winner=next_game_state.winner) if stage != GameStage.IN_PROGRESS else None
        ]
