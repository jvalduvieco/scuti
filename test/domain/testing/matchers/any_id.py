from unittest import TestCase

from mani.domain.model.identifiable.identifier import Identifier
from mani.domain.testing.matchers.any_id import AnyId
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId


class TestAnyId(TestCase):
    def test_matches_any_id(self):
        self.assertEqual(AnyId(), UuidId())

    def test_does_not_match_something_that_is_not_an_id(self):
        self.assertNotEqual(AnyId(), 42)

    def test_can_match_id_of_a_certain_type(self):
        self.assertEqual(AnyId(UuidId), UuidId())

    def test_any_id_does_not_match_an_id_of_another_type(self):
        class OperationId(Identifier):
            def serialize(self):
                return None

        self.assertNotEqual(AnyId(UuidId), OperationId())
