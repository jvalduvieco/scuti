from __future__ import annotations

from dataclasses import dataclass
from unittest import TestCase

from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntity
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


@dataclass(frozen=True)
class Something(IdentifiableEntity[UuidId]):
    id: UuidId


class SomethingRepositoryInMemory(InMemoryRepository[Something, UuidId]):
    pass


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
