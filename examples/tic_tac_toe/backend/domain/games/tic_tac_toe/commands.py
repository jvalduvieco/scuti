from dataclasses import dataclass

from domain.games.types import GameId, PlayerId
from domain.operation_id import OperationId
from mani.domain.cqrs.effects import Command


@dataclass(frozen=True)
class NewGame(Command):
    operation_id: OperationId
    game_id: GameId
    first_player: PlayerId
    second_player: PlayerId


@dataclass(frozen=True)
class PlaceMark(Command):
    operation_id: OperationId
    game_id: GameId
    player: PlayerId
    x: int
    y: int
