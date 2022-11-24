from dataclasses import dataclass

from domain.games.types import UserId
from domain.operation_id import OperationId

from scuti.domain.cqrs.effects import Query


@dataclass(frozen=True)
class GetUser(Query):
    operation_id: OperationId
    id: UserId
