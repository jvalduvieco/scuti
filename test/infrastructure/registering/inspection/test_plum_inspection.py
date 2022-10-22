import unittest
from typing import Union

from plum import dispatch

from mani.infrastructure.registering.inspection.plum_inspection import inspect
from test.infrastructure.registering.inspection.fixtures import ANicePlumHandler, ACreationalCommand, SomeState, \
    ANiceCommand, ANiceEvent, \
    ANotSoNiceCommand, AStinkyCommand


class TestPlumInspection(unittest.TestCase):
    def test_one_parameter_function_should_return_a_map_with_one_item_per_overload_with_a_list_of_parameter_types(self):
        @dispatch
        def a_function_with_one_parameter(parameter: int) -> None:
            pass

        @dispatch
        def a_function_with_one_parameter(parameter: str) -> None:
            pass

        self.assertEqual({0: [[int]], 1: [[str]]}, inspect(a_function_with_one_parameter))

    def test_multiple_parameter_function_should_return_a_map_with_one_item_per_overload_with_a_list_of_parameter_types(
            self):
        @dispatch
        def a_function_with_more_parameters(parameter: int, another_parameter: str) -> None:
            pass

        @dispatch
        def a_function_with_more_parameters(another_parameter: str, parameter: int) -> None:
            pass

        self.assertEqual({0: [[int], [str]], 1: [[str], [int]]}, inspect(a_function_with_more_parameters))

    def test_when_inspecting_union_parameter_types_are_returned_ordered_alphabetically(self):
        @dispatch
        def a_function_with_unions(a_parameter: int, a_union: Union[int, str]) -> None:
            pass

        self.assertEqual({0: [[int], [int, str]]}, inspect(a_function_with_unions))

    def test_can_inspect_a_plum_overloaded_method(self):
        self.assertEqual({0: [[ACreationalCommand]],
                          1: [[SomeState], [ANiceCommand]],
                          2: [[SomeState], [ANiceEvent]],
                          3: [[SomeState], [ANotSoNiceCommand, AStinkyCommand]]},
                         inspect(ANicePlumHandler.handle, should_ignore_self=True))
