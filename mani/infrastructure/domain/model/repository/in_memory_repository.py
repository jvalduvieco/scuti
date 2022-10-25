from abc import ABC
from typing import List, Generator

from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntityType
from mani.domain.model.identifiable.identifier import IdentifierType
from mani.domain.model.repository.repository import Repository


class InMemoryRepository(Repository[IdentifiableEntityType, IdentifierType]):
    def __init__(self, initial_values: List[IdentifiableEntityType] = None):
        initial_values = initial_values if initial_values is not None else []
        self.__entities = {value.id: value for value in initial_values}

    def save(self, entity: IdentifiableEntityType):
        self.__entities = {entity.id: entity}

    def by_id(self, an_id: IdentifierType) -> IdentifiableEntityType:
        return self.__entities[an_id]

    def delete(self, an_id: IdentifierType):
        del (self.__entities[an_id])

    def all(self) -> Generator[IdentifiableEntityType, None, None]:
        for entity in self.__entities.values():
            yield entity
