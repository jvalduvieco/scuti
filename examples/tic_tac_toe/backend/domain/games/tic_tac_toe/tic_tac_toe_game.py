from plum import dispatch

from backend.domain.games.tic_tac_toe.board import TicTacToeBoard
from backend.domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from backend.domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from backend.domain.games.tic_tac_toe.game import Game, GameStage
from backend.domain.games.tic_tac_toe.types import GameErrorReasons
from backend.infrastructure.domain.tic_tac_toe.game_repository_in_memory import GameRepositoryInMemory
from domain.cqrs.bus.effect_handler import EffectHandler
from domain.cqrs.bus.event_bus import EventBus


class TicTacToeGame(EffectHandler):
    def __init__(self, game_repository: GameRepositoryInMemory, event_bus: EventBus):
        self.__game_repository = game_repository
        self.__event_bus = event_bus

    @dispatch
    def handle(self, command: NewGame) -> None:
        current_game = Game(id=command.game_id,
                            player_1=command.player_1,
                            player_2=command.player_2,
                            board=TicTacToeBoard(),
                            stage=GameStage.IN_PROGRESS,
                            waiting_for_player=command.player_1)
        self.__game_repository.save(current_game)
        self.__event_bus.handle([
            GameStarted(game_id=current_game.id,
                        player_1=current_game.player_1,
                        player_2=current_game.player_2,
                        board=current_game.board,
                        parent_operation_id=command.operation_id),
            BoardUpdated(game_id=current_game.id, board=current_game.board),
            WaitingForPlayerPlay(game_id=current_game.id,
                                 player_id=current_game.player_1)
        ])

    @dispatch
    def handle(self, command: PlaceMark):
        game_state = self.__game_repository.by_id(command.game_id)
        if game_state.waiting_for_player != command.player_id:
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                                       player=command.player_id,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        elif game_state.board.is_off_limits(command.x, command.y):
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                                       player=command.player_id,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id
                                                       )])
        elif not game_state.board.is_cell_free(command.x, command.y):
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                                                       player=command.player_id,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        else:
            next_game_state = game_state.place(command.player_id, command.x, command.y)
            self.__event_bus.handle([BoardUpdated(game_id=game_state.id, board=next_game_state.board)])
            self.__game_repository.save(next_game_state)
            stage = next_game_state.stage
            if stage != GameStage.IN_PROGRESS:
                self.__event_bus.handle([GameEnded(game_id=game_state.id, result=stage, winner=next_game_state.winner)])
