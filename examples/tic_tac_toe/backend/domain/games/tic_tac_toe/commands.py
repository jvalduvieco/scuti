from dataclasses import dataclass

from domain.games.types import GameId, UserId
from domain.operation_id import OperationId

from mani.domain.cqrs.effects import Command


@dataclass(frozen=True)
class CreateGame(Command):
    operation_id: OperationId
    game_id: GameId
    creator: UserId


@dataclass(frozen=True)
class JoinGame(Command):
    operation_id: OperationId
    game_id: GameId
    player_id: UserId


@dataclass(frozen=True)
class PlaceMark(Command):
    operation_id: OperationId
    game_id: GameId
    player: UserId
    x: int
    y: int
