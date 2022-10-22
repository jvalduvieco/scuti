from dataclasses import dataclass

from backend.domain.operatuion_id import OperationId
from backend.domain.games.types import GameId, PlayerId
from domain.cqrs.effects import Command


@dataclass(frozen=True)
class NewGame(Command):
    operation_id: OperationId
    game_id: GameId
    player_1: PlayerId
    player_2: PlayerId


@dataclass(frozen=True)
class PlaceMark(Command):
    operation_id: OperationId
    game_id: GameId
    player_id: PlayerId
    x: int
    y: int
