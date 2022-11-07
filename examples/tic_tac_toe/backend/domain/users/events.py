from dataclasses import dataclass

from domain.operation_id import OperationId
from mani.domain.cqrs.effects import Event
from domain.users.user import User


@dataclass(frozen=True)
class UserCreated(Event):
    user: User
    parent_operation_id: OperationId


@dataclass(frozen=True)
class UserUpdated(Event):
    user: User
    parent_operation_id: OperationId
