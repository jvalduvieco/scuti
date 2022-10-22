from abc import ABC, abstractmethod
from typing import Dict

from mani.domain.cqrs.effects import Query


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> Dict:
        pass
