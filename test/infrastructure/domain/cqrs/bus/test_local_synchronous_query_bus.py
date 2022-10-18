from dataclasses import dataclass
from typing import Dict
from unittest import TestCase

from parameterized import parameterized

from domain.cqrs.bus.exceptions import AlreadyRegisteredEffect, NoHandlerForEffect
from domain.cqrs.effects import Query
from domain.cqrs.bus.query_bus import QueryBus
from domain.cqrs.bus.query_handler import QueryHandler
from infrastructure.domain.cqrs.bus.local_synchronous_query_bus import LocalSynchronousQueryBus


def a_simple_handler(_: Query) -> Dict:
    return {}


class HandlerCalled(ValueError):
    pass


def a_handler_that_raises_an_exception(_):
    raise HandlerCalled()


def a_handler_that_fails(_):
    raise ValueError()


@dataclass(frozen=True)
class AQuery(Query):
    a_property: str


def build_simple_query_handler(query_type, handler_service_type):
    def query_handler(query: query_type):
        service = handler_service_type()
        return service.handle(query)

    return {"effect_type": query_type, "handler": query_handler}


class AQueryHandler(QueryHandler):
    def handle(self, _) -> Dict:
        return {"result": "test"}


class TestLocalSynchronousQueryBus(TestCase):
    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_register_a_handler_for_a_query(self, query_bus: QueryBus):
        query_bus.subscribe(AQuery, a_simple_handler)

    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_handle_a_query(self, query_bus: QueryBus):
        query_bus.subscribe(**build_simple_query_handler(AQuery, AQueryHandler))
        query_result = query_bus.handle(AQuery(a_property="Test"))
        self.assertEqual({"result": "test"}, query_result)

    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_not_let_register_two_handlers_for_a_query(self, query_bus: QueryBus):
        query_bus.subscribe(AQuery, a_simple_handler)

        with self.assertRaises(AlreadyRegisteredEffect):
            query_bus.subscribe(AQuery, a_simple_handler)

    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_handle_a_registered_query(self, query_bus: QueryBus):
        query_bus.subscribe(AQuery, a_handler_that_raises_an_exception)

        with self.assertRaises(HandlerCalled):
            query_bus.handle(AQuery(a_property="Test"))

    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_bubble_up_exceptions(self, query_bus: QueryBus):
        query_bus.subscribe(AQuery, a_handler_that_fails)

        with self.assertRaises(ValueError):
            query_bus.handle(AQuery(a_property="Test"))

    @parameterized.expand([
        [LocalSynchronousQueryBus()]
    ])
    def test_should_raise_an_exception_for_an_unregistered_query(self, query_bus: QueryBus):
        with self.assertRaises(NoHandlerForEffect):
            query_bus.handle(AQuery(a_property="Test"))
