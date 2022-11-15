from dataclasses import dataclass

from domain.games.types import UserId
from domain.operation_id import OperationId
from mani.domain.cqrs.effects import Query


@dataclass(frozen=True)
class GetUsersOnline(Query):
    operation_id: OperationId
