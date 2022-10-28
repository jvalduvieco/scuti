from dataclasses import dataclass
from typing import Type
from unittest import TestCase

from hamcrest import assert_that, contains_exactly

from mani.domain.testing.matchers.something_like import SomethingLike


class TestSomethingLike(TestCase):
    def test_partial_match_can_match_by_type(self):
        @dataclass(frozen=True)
        class Something:
            id: int
            content: str

        subject = [Something(1, "a")]
        assert_that(subject, contains_exactly(SomethingLike(Something)))

    def test_partial_type_match_does_not_match_another_type(self):
        @dataclass(frozen=True)
        class Something:
            id: int
            content: str

        class Popo:
            id: int
            content: str

        subject = [Something(1, "a")]
        with self.assertRaises(AssertionError):
            assert_that(subject, contains_exactly(SomethingLike(Popo)))

    def test_partial_match_can_match_by_some_properties(self):
        @dataclass(frozen=True)
        class Something:
            id: int
            content: str

        subject = [Something(1, "a")]
        assert_that(subject, contains_exactly(SomethingLike(a_type=Something, id=1)))
        assert_that(subject, contains_exactly(SomethingLike(a_type=Something, id=1, content="a")))

    def test_partial_match_can_match_only_by_some_properties(self):
        @dataclass(frozen=True)
        class Something:
            id: int
            content: str

        subject = [Something(1, "a")]
        assert_that(subject, contains_exactly(SomethingLike(id=1)))
