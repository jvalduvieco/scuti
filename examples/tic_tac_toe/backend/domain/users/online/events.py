from dataclasses import dataclass
from typing import List

from domain.games.types import UserId
from domain.operation_id import OperationId
from scuti.domain.cqrs.effects import Event


@dataclass(frozen=True)
class UserConnected(Event):
    id: UserId
    operation_id: OperationId


@dataclass(frozen=True)
class UsersOnlineUpdated(Event):
    online_users: List[UserId]
    parent_operation_id: OperationId


@dataclass(frozen=True)
class UserDisconnected(Event):
    id: UserId
    operation_id: OperationId
