from __future__ import annotations

from dataclasses import dataclass
from typing import List, Generator
from unittest import TestCase

from domain.model.identifiable.identifiable_entity import IdentifiableEntity, IdentifiableEntityType
from domain.model.identifiable.identifier import IdentifierType
from domain.model.repository.repository import Repository
from infrastructure.domain.model.identifier.uuid_id import UuidId


@dataclass(frozen=True)
class Something(IdentifiableEntity[UuidId]):
    id: UuidId


class SomethingRepositoryInMemory(Repository[Something, UuidId]):
    def __init__(self, initial_values: List[Something] = None):
        initial_values = initial_values if initial_values is not None else []
        self.__entities = {value.id: value for value in initial_values}

    def save(self, entity: Something):
        self.__entities = {entity.id: entity}

    def by_id(self, an_id: UuidId) -> Something:
        return self.__entities[an_id]

    def delete(self, an_id: UuidId):
        del (self.__entities[an_id])

    def all(self) -> Generator[IdentifiableEntityType[IdentifierType]]:
        for entity in self.__entities.values():
            yield entity


class TestRepository(TestCase):
    def test_repositories_can_be_instantiated(self):
        a_repository = SomethingRepositoryInMemory()
        self.assertTrue(a_repository)

    def test_repositories_can_save_entities_and_retrieve(self):
        a_repository = SomethingRepositoryInMemory()
        something_nice = Something(id=UuidId())
        a_repository.save(something_nice)
        something_nice_from_the_repository = a_repository.by_id(something_nice.id)
        self.assertEqual(something_nice, something_nice_from_the_repository)

    def test_can_delete_entities_by_a_given_id(self):
        a_repository = SomethingRepositoryInMemory()
        something_nice = Something(id=UuidId())
        a_repository.save(something_nice)
        a_repository.delete(something_nice.id)

        self.assertEqual([], list(a_repository.all()))
