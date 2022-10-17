from abc import ABC, abstractmethod
from typing import Dict, Type, Callable

from domain.cqrs.effects import Query


class QueryBus(ABC):
    @abstractmethod
    def handle(self, query: Query) -> Dict:
        pass

    @abstractmethod
    def register(self, query_type: Type[Query], handler: Callable[[Query], Dict]) -> None:
        pass
