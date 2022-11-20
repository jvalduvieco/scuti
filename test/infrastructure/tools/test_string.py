from unittest import TestCase

from mani.infrastructure.tools.string import camel_to_lower_snake, snake_to_lower_camel, snake_to_upper_camel


class TestStringTools(TestCase):
    def test_can_transform_upper_snake_to_came_case(self):
        a_string = "I_AM_UPPER_SNAKE_CASE"
        self.assertEqual("IAmUpperSnakeCase", snake_to_upper_camel(a_string))

    def test_can_transform_snake_case_to_upper_camel_case(self):
        a_string = "I_AM_UPPER_SNAKE_CASE"
        self.assertEqual("iAmUpperSnakeCase", snake_to_lower_camel(a_string))

    def test_can_transform_upper_camel_case_to_snake_case(self):
        a_string = "iAmLowerCamelCase"
        self.assertEqual("i_am_lower_camel_case", camel_to_lower_snake(a_string))
