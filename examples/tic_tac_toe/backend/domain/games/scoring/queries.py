from dataclasses import dataclass

from domain.operation_id import OperationId

from scuti.domain.cqrs.effects import Query


@dataclass(frozen=True)
class GetTopThreePlayers(Query):
    operation_id: OperationId
