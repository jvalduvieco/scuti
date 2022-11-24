from dataclasses import dataclass, field
from typing import List, Optional

from domain.games.tic_tac_toe.types import GameErrorReasons, GameStage
from domain.games.types import GameId, UserId
from domain.operation_id import OperationId
from scuti.domain.cqrs.effects import Event
from scuti.domain.time.units import Millisecond

TicTacToeBoardAsLists = List[List[UserId]]


@dataclass(frozen=True)
class GameCreated(Event):
    game_id: GameId
    creator: UserId
    stage: GameStage
    parent_operation_id: OperationId


@dataclass(frozen=True)
class GameStarted(Event):
    game_id: GameId
    players: List[UserId]
    board: TicTacToeBoardAsLists


@dataclass(frozen=True)
class WaitingForPlayerPlay(Event):
    game_id: GameId
    player_id: UserId
    timeout: Millisecond


@dataclass(frozen=True)
class TurnTimeout(Event):
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


@dataclass(frozen=True)
class MarkPlaced(Event):
    game_id: GameId
    player: UserId
    x: int
    y: int
    parent_operation_id: OperationId


@dataclass(frozen=True)
class GameStateReadyToBeCleaned(Event):
    game_id: GameId
