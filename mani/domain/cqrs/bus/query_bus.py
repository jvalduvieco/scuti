from abc import ABC, abstractmethod
from typing import Dict, Type, Callable

from mani.domain.cqrs.effects import Query
from mani.domain.cqrs.bus.bus import Bus


class QueryBus(ABC, Bus):
    @abstractmethod
    def handle(self, query: Query) -> Dict:
        pass

    @abstractmethod
    def subscribe(self, query_type: Type[Query], handler: Callable[[Query], Dict]) -> None:
        pass
