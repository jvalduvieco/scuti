from injector import inject
from plum import dispatch

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from domain.games.tic_tac_toe.game import Game
from domain.games.tic_tac_toe.game_repository import GameRepository
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus


class TicTacToeGame(EffectHandler):
    @inject
    def __init__(self, game_repository: GameRepository, event_bus: EventBus):
        self.__game_repository = game_repository
        self.__event_bus = event_bus

    @dispatch
    def handle(self, command: NewGame) -> None:
        current_game = Game(id=command.game_id,
                            first_player=command.first_player,
                            second_player=command.second_player,
                            board=TicTacToeBoard(),
                            stage=GameStage.IN_PROGRESS,
                            waiting_for_player=command.first_player)
        self.__game_repository.save(current_game)
        self.__event_bus.handle([
            GameStarted(game_id=current_game.id,
                        first_player=current_game.first_player,
                        second_player=current_game.second_player,
                        board=current_game.board.to_list(),
                        stage=current_game.stage,
                        parent_operation_id=command.operation_id),
            BoardUpdated(game_id=current_game.id, board=current_game.board.to_list()),
            WaitingForPlayerPlay(game_id=current_game.id,
                                 player_id=current_game.first_player)
        ])

    @dispatch
    def handle(self, command: PlaceMark):
        game_state = self.__game_repository.by_id(command.game_id)
        if game_state.waiting_for_player != command.player:
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                                       player=command.player,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        elif game_state.board.is_off_limits(command.x, command.y):
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.POSITION_OFF_LIMITS,
                                                       player=command.player,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id
                                                       )])
        elif not game_state.board.is_cell_free(command.x, command.y):
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                                                       player=command.player,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        elif game_state.stage != GameStage.IN_PROGRESS:
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.GAME_ALREADY_ENDED,
                                                       player=command.player,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        else:
            next_game_state = game_state.place(command.player, command.x, command.y)
            self.__event_bus.handle([
                WaitingForPlayerPlay(game_id=next_game_state.id, player_id=next_game_state.waiting_for_player),
                BoardUpdated(game_id=game_state.id, board=next_game_state.board.to_list())
            ])
            self.__game_repository.save(next_game_state)
            stage = next_game_state.stage
            if stage != GameStage.IN_PROGRESS:
                self.__event_bus.handle([GameEnded(game_id=game_state.id, result=stage, winner=next_game_state.winner)])
