from dataclasses import dataclass, field
from typing import Optional, List

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from domain.games.types import GameId, UserId
from domain.operation_id import OperationId
from mani.domain.cqrs.effects import Event

TicTacToeBoardAsLists = List[List[UserId]]


@dataclass(frozen=True)
class GameStarted(Event):
    game_id: GameId
    first_player: UserId
    second_player: UserId
    board: TicTacToeBoardAsLists
    stage: GameStage
    parent_operation_id: OperationId


@dataclass(frozen=True)
class WaitingForPlayerPlay(Event):
    game_id: GameId
    player_id: UserId


@dataclass(frozen=True)
class BoardUpdated(Event):
    game_id: GameId
    board: TicTacToeBoardAsLists


@dataclass(frozen=True)
class GameErrorOccurred(Event):
    game_id: GameId
    player: UserId
    reason: GameErrorReasons
    parent_operation_id: OperationId


@dataclass(frozen=True)
class GameEnded(Event):
    game_id: GameId
    result: GameStage
    winner: Optional[UserId] = field(default=None)
