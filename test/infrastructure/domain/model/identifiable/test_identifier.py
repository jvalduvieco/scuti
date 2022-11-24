from unittest import TestCase

from parameterized import parameterized_class

from scuti.infrastructure.domain.model.identifiable.string_id import StringId
from scuti.infrastructure.domain.model.identifiable.uuid_id import UuidId


@parameterized_class(('type', 'expected'), [
    (StringId, "ABC"),
    (UuidId, "c60c4b05-7335-45a4-82c9-db166f8d3e04"),
])
class TestIdentifier(TestCase):
    def test_identifiers_can_be_serialized(self):
        an_id = self.type(self.expected)
        self.assertEqual(self.expected, an_id.serialize())

    def test_equal_to_another_identifier_with_the_same_value(self):
        self.assertEqual(self.type(self.expected), self.type(self.expected))

    def test_should_be_stringifiables(self):
        self.assertEqual(f"{self.type.__name__}(id='{self.expected}')", str(self.type(self.expected)))

    def test_should_be_hasheable(self):
        a_dict = {self.type(self.expected): self.expected}
        self.assertEqual(self.expected, a_dict[self.type(self.expected)])

    def test_generate_a_random_valid_value_if_none_is_provided(self):
        self.assertEqual(self.type, type(self.type()))
        random_id = self.type().id
        self.assertEqual(f"{self.type.__name__}(id='{random_id}')", str(self.type(random_id)))
