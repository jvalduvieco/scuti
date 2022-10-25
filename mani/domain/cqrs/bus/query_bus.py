from abc import ABC, abstractmethod
from typing import Dict, Type, Callable, Any

from mani.domain.cqrs.effects import Query


class QueryBus(ABC):
    @abstractmethod
    def handle(self, query: Query) -> Dict:
        pass

    @abstractmethod
    def subscribe(self, query_type: Type[Query], handler: Callable[[Query], Dict[str, Any]]) -> None:
        pass
