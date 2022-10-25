from unittest import TestCase

from infrastructure.tools.list import all_equal_and_not_none


class TestAllEqualAndNotNone(TestCase):
    def test_returns_true_if_all_items_are_equal_and_not_none(self):
        a_list = [1, 1, 1]
        self.assertTrue(all_equal_and_not_none(a_list))

    def test_returns_false_if_all_items_are_not_equal(self):
        a_list = [1, 2, 1]
        self.assertFalse(all_equal_and_not_none(a_list))
        another_list = [1, None, 1]
        self.assertFalse(all_equal_and_not_none(another_list))

    def test_returns_false_if_all_items_are_none(self):
        a_list = [None, None, None]
        self.assertFalse(all_equal_and_not_none(a_list))
