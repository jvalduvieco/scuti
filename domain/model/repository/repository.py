from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator

from domain.model.identifiable.identifiable_entity import IdentifiableEntityType, IdentifiableEntity
from domain.model.identifiable.identifier import IdentifierType


class Repository(Generic[IdentifiableEntityType, IdentifierType], ABC):
    @abstractmethod
    def save(self, entity: IdentifiableEntity[IdentifierType]):
        pass

    @abstractmethod
    def delete(self, entity: IdentifiableEntity[IdentifierType]):
        pass

    @abstractmethod
    def by_id(self, an_id: IdentifierType) -> IdentifiableEntity[IdentifierType]:
        pass

    @abstractmethod
    def all(self) -> Iterator[IdentifiableEntityType[IdentifierType]]:
        pass
