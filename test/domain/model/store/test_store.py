from dataclasses import dataclass
from unittest import TestCase

from scuti.infrastructure.domain.model.store.in_memory_store import InMemoryStore


@dataclass(frozen=True)
class Something:
    a_property: int
    another_property: str


class SomethingStoreInMemory(InMemoryStore[Something]):
    pass


class StoreTestCase(TestCase):
    def test_stores_can_be_instantiated(self):
        a_store = SomethingStoreInMemory()
        self.assertTrue(a_store)

    def test_stores_can_save_entities_and_retrieve(self):
        a_store = SomethingStoreInMemory()
        something_nice = Something(a_property=3, another_property="popo")
        a_store.save(something_nice)
        something_nice_from_store = a_store.get()
        self.assertEqual(something_nice, something_nice_from_store)
