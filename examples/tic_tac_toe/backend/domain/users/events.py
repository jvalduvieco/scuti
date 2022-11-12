from dataclasses import dataclass

from domain.games.types import UserId, GameId
from domain.operation_id import OperationId
from domain.users.user import User
from mani.domain.cqrs.effects import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user: User
    parent_operation_id: OperationId


@dataclass(frozen=True)
class UserUpdated(Event):
    user: User
    parent_operation_id: OperationId


@dataclass(frozen=True)
class UserInvited(Event):
    host: UserId
    invited: UserId
    game: GameId
    operation_id: OperationId


@dataclass(frozen=True)
class PlayerJoinedAGame(Event):
    game_id: GameId
    player_id: UserId
    parent_operation_id: OperationId
