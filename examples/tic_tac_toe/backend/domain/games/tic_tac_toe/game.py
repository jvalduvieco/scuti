from dataclasses import dataclass, field, replace
from typing import Optional, List

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.types import GameStage
from domain.games.types import GameId, UserId

from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntity


@dataclass(frozen=True)
class GameWaitingForPlayers:
    id: GameId
    players: List[UserId] = field(default_factory=list)


@dataclass(frozen=True)
class GameInProgress(IdentifiableEntity[GameId]):
    id: GameId
    board: TicTacToeBoard
    stage: GameStage
    winner: Optional[UserId] = field(default=None)
    waiting_for_player: Optional[UserId] = field(default=None)
    players: List[UserId] = field(default_factory=list)

    def place(self, player: UserId, x: int, y: int):
        next_board = self.board.place(x=x, y=y, player_id=player)
        stage = self.__next_stage(next_board)
        winner = next_board.any_player_has_three_in_a_row()
        next_player = self.players[0] if self.waiting_for_player == self.players[1] else self.players[1]
        return replace(self,
                       waiting_for_player=next_player,
                       winner=winner,
                       stage=stage,
                       board=next_board)

    def cancel_game(self):
        return replace(self, stage=GameStage.GAME_ABORTED)

    def __next_stage(self, next_board: TicTacToeBoard):
        if next_board.any_player_has_three_in_a_row():
            return GameStage.PLAYER_WON
        elif next_board.is_full():
            return GameStage.DRAW
        else:
            return GameStage.IN_PROGRESS
