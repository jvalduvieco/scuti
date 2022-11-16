from unittest import TestCase

from mani.domain.model.identifiable.identifier import Identifier
from mani.domain.testing.matchers.any_id import match_any_id
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId


class TestAnyId(TestCase):
    def test_matches_any_id(self):
        self.assertEqual(match_any_id(), UuidId())

    def test_does_not_match_something_that_is_not_an_id(self):
        self.assertNotEqual(match_any_id(), 42)

    def test_can_match_id_of_a_certain_type(self):
        self.assertEqual(match_any_id(UuidId), UuidId())

    def test_any_id_does_not_match_an_id_of_another_type(self):
        class OperationId(Identifier):
            def serialize(self):
                return None

        self.assertNotEqual(match_any_id(UuidId), OperationId())

    def test_repr_specifies_it_is_a_matcher_for_a_type(self):
        self.assertEqual("<matches any UuidId>", match_any_id(UuidId).__repr__())

    def test_repr_specifies_it_is_a_matcher_for_a_descendant_of_identifier(self):
        self.assertEqual("<matches any descendant of Identifier>", match_any_id().__repr__())
