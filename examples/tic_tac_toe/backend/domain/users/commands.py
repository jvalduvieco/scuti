from dataclasses import dataclass
from datetime import datetime

from domain.games.types import UserId
from domain.operation_id import OperationId

from mani.domain.cqrs.effects import Command


@dataclass(frozen=True)
class CreateUser(Command):
    id: UserId
    alias: str
    created_at: datetime
    operation_id: OperationId


@dataclass(frozen=True)
class UpdateUser(Command):
    id: UserId
    alias: str
    operation_id: OperationId
