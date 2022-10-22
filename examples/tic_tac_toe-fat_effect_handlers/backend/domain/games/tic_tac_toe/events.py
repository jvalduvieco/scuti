from dataclasses import dataclass, field
from typing import Optional

from backend.domain.games.tic_tac_toe.board import TicTacToeBoard
from backend.domain.games.tic_tac_toe.game import GameStage
from backend.domain.operatuion_id import OperationId
from backend.domain.games.tic_tac_toe.types import GameErrorReasons
from backend.domain.games.types import GameId, PlayerId
from domain.cqrs.effects import Event


@dataclass(frozen=True)
class GameStarted(Event):
    game_id: GameId
    player_1: PlayerId
    player_2: PlayerId
    board: TicTacToeBoard
    parent_operation_id: OperationId


@dataclass(frozen=True)
class WaitingForPlayerPlay(Event):
    game_id: GameId
    player_id: PlayerId


@dataclass(frozen=True)
class BoardUpdated(Event):
    game_id: GameId
    board: TicTacToeBoard


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
