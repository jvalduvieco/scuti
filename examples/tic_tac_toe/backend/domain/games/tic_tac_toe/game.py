from dataclasses import dataclass, field, replace
from typing import Optional

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.types import GameStage
from domain.games.types import GameId, PlayerId
from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntity


@dataclass(frozen=True)
class Game(IdentifiableEntity[GameId]):
    id: GameId
    first_player: PlayerId
    second_player: PlayerId
    board: TicTacToeBoard
    stage: GameStage
    winner: Optional[PlayerId] = field(default=None)
    waiting_for_player: Optional[PlayerId] = field(default=None)

    def place(self, player: PlayerId, x: int, y: int):
        next_board = self.board.place(x=x, y=y, player_id=player)
        stage = self.__next_stage(next_board)
        winner = next_board.any_player_has_three_in_a_row()
        next_player = self.first_player if self.waiting_for_player == self.second_player else self.second_player
        return replace(self,
                       waiting_for_player=next_player,
                       winner=winner,
                       stage=stage,
                       board=next_board)

    def __next_stage(self, next_board: TicTacToeBoard):
        if next_board.any_player_has_three_in_a_row():
            return GameStage.PLAYER_WON
        elif next_board.is_full():
            return GameStage.DRAW
        else:
            return GameStage.IN_PROGRESS
