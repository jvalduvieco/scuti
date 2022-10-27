from dataclasses import dataclass, field
from typing import Optional, List

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.tic_tac_toe.types import GameStage, GameErrorReasons
from domain.games.types import GameId, PlayerId
from domain.operation_id import OperationId
from mani.domain.cqrs.effects import Event

TicTacToeBoardAsLists = List[List[PlayerId]]


@dataclass(frozen=True)
class GameStarted(Event):
    game_id: GameId
    first_player: PlayerId
    second_player: PlayerId
    board: TicTacToeBoardAsLists
    stage: GameStage
    parent_operation_id: OperationId


@dataclass(frozen=True)
class WaitingForPlayerPlay(Event):
    game_id: GameId
    player_id: PlayerId


@dataclass(frozen=True)
class BoardUpdated(Event):
    game_id: GameId
    board: TicTacToeBoardAsLists


@dataclass(frozen=True)
class GameErrorOccurred(Event):
    game_id: GameId
    player: PlayerId
    reason: GameErrorReasons
    parent_operation_id: OperationId


@dataclass(frozen=True)
class GameEnded(Event):
    game_id: GameId
    result: GameStage
    winner: Optional[PlayerId] = field(default=None)
