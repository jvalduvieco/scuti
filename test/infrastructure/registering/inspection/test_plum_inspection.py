import unittest
from typing import Union

from plum import dispatch

from mani.infrastructure.registering.inspection.plum_inspection import inspect, InspectionResult
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

        self.assertEqual({
            0: InspectionResult(parameter_types=[[int]], annotations={}),
            1: InspectionResult(parameter_types=[[str]], annotations={})
        },
            inspect(a_function_with_one_parameter))

    def test_multiple_parameter_function_should_return_a_map_with_one_item_per_overload_with_a_list_of_parameter_types(
            self):
        @dispatch
        def a_function_with_more_parameters(parameter: int, another_parameter: str) -> None:
            pass

        @dispatch
        def a_function_with_more_parameters(another_parameter: str, parameter: int) -> None:
            pass

        self.assertEqual({
            0: InspectionResult(parameter_types=[[int], [str]], annotations={}),
            1: InspectionResult(parameter_types=[[str], [int]], annotations={})
        },
            inspect(a_function_with_more_parameters))

    def test_when_inspecting_union_parameter_types_are_returned_ordered_alphabetically(self):
        @dispatch
        def a_function_with_unions(a_parameter: int, a_union: Union[int, str]) -> None:
            pass

        self.assertEqual({
            0: InspectionResult(parameter_types=[[int], [int, str]], annotations={})
        },
            inspect(a_function_with_unions))

    def test_can_inspect_a_plum_overloaded_method(self):
        self.assertEqual({
            0: InspectionResult(parameter_types=[[ACreationalCommand]], annotations={}),
            1: InspectionResult(parameter_types=[[SomeState], [ANiceCommand]], annotations={}),
            2: InspectionResult(parameter_types=[[SomeState], [ANiceEvent]], annotations={}),
            3: InspectionResult(parameter_types=[[SomeState], [ANotSoNiceCommand, AStinkyCommand]], annotations={})
        },
            inspect(ANicePlumHandler.handle, should_ignore_self=True))

    def test_annotations_before_dispatch_annotation_are_ignored_by_inspect(self):
        def annotate(a_value: int):
            def decorator(function):
                function._nice_annotation = a_value
                return function

            return decorator

        @dispatch
        @annotate(42)
        def something(parameter: int, another_parameter: str) -> None:
            pass

        @annotate(55)
        @dispatch
        def something(another_parameter: str, parameter: float) -> None:
            pass

        self.assertEqual({
            0: InspectionResult(parameter_types=[[int], [str]], annotations={"_nice_annotation": 42}),
            1: InspectionResult(parameter_types=[[str], [float]], annotations={})
        },
            inspect(something, annotations_to_retrieve=["_nice_annotation"]))
