from dataclasses import dataclass, field, replace
from typing import Optional

from backend.domain.games.tic_tac_toe.board import TicTacToeBoard
from backend.domain.games.tic_tac_toe.types import GameStage
from backend.domain.games.types import GameId, PlayerId
from domain.model.identifiable.identifiable_entity import IdentifiableEntity


@dataclass(frozen=True)
class Game(IdentifiableEntity):
    id: GameId
    player_1: PlayerId
    player_2: PlayerId
    board: TicTacToeBoard
    stage: GameStage
    winner: Optional[PlayerId] = field(default=None)
    waiting_for_player: Optional[PlayerId] = field(default=None)

    def place(self, player: PlayerId, x: int, y: int):
        next_board = self.board.place(x=x, y=y, player_id=player)
        stage = self.__next_stage(next_board)
        winner = next_board.any_player_has_three_in_a_row()
        next_player = self.player_1 if self.waiting_for_player == self.player_2 else self.player_2
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
