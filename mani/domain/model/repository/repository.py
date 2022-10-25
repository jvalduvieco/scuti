from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator

from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntityType
from mani.domain.model.identifiable.identifier import IdentifierType


class Repository(ABC, Generic[IdentifiableEntityType, IdentifierType]):
    @abstractmethod
    def save(self, entity: IdentifiableEntityType):
        pass

    @abstractmethod
    def delete(self, entity: IdentifierType):
        pass

    @abstractmethod
    def by_id(self, an_id: IdentifierType) -> IdentifiableEntityType:
        pass

    @abstractmethod
    def all(self) -> Iterator[IdentifiableEntityType]:
        pass
