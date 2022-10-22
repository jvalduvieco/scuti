import unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, List, Tuple

from injector import Module, Scope, SingletonScope, Binder
from plum import dispatch

from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.exceptions import NoHandlerForEffect
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.effects import Command, Query, Event
from mani.domain.model.application import Application
from mani.domain.model.modules import DomainModule


class TestApplication(unittest.TestCase):
    def test_can_create_an_application(self):
        config = {}
        domains = []
        app = Application(config=config, domains=domains)
        self.assertTrue(app)

    def test_can_access_command_bus(self):
        config = {}
        domains = []
        app = Application(config=config, domains=domains)
        self.assertTrue(issubclass(app.command_bus.__class__, CommandBus))

    def test_can_access_event_bus(self):
        config = {}
        domains = []
        app = Application(config=config, domains=domains)
        self.assertTrue(issubclass(app.event_bus.__class__, EventBus))

    def test_can_access_query_bus(self):
        config = {}
        domains = []
        app = Application(config=config, domains=domains)
        self.assertTrue(issubclass(app.query_bus.__class__, QueryBus))

    def test_can_register_domain_modules(self):
        class DummyDomainModule(DomainModule):
            pass

        config = {}
        domains = [DummyDomainModule]
        app = Application(config=config, domains=domains)
        self.assertEqual("This is an app running these domains: CQRSDomainModule, DummyDomainModule", str(app))

    def test_domain_modules_can_add_bindings_using_tuples(self):
        class SomethingAbstract(ABC):
            @abstractmethod
            def do(self):
                pass

        class SomethingConcrete(SomethingAbstract):
            def do(self):
                pass

        class DummyDomainModule(DomainModule):
            def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
                return [(SomethingAbstract, SomethingConcrete, SingletonScope)]

        config = {}
        domains = [DummyDomainModule]
        app = Application(config=config, domains=domains)
        self.assertEqual(SomethingConcrete, app.injector().get(SomethingAbstract).__class__)

    def test_domain_modules_can_add_bindings_using_injector_modules(self):
        class SomethingAbstract(ABC):
            @abstractmethod
            def do(self):
                pass

        class SomethingConcrete(SomethingAbstract):
            def do(self):
                pass

        class AnInjectorModule(Module):
            def configure(self, binder: Binder):
                binder.bind(SomethingAbstract, SomethingConcrete, SingletonScope)

        class DummyDomainModule(DomainModule):
            def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
                return [AnInjectorModule]

        config = {}
        domains = [DummyDomainModule]
        app = Application(config=config, domains=domains)
        self.assertEqual(SomethingConcrete, app.injector().get(SomethingAbstract).__class__)

    def test_domain_modules_can_define_a_list_of_initial_commands_that_are_executed_on_starting_application(self):
        @dataclass(frozen=True)
        class ACommand(Command):
            pass

        class DummyDomainModule(DomainModule):
            def init_commands(self) -> List[Command]:
                return [ACommand()]

        config = {}
        domains = [DummyDomainModule]
        app = Application(config=config, domains=domains)
        with self.assertRaises(NoHandlerForEffect):
            app.start()

    def test_domain_modules_can_register_effect_handlers(self):
        @dataclass(frozen=True)
        class ACommand(Command):
            pass

        @dataclass(frozen=True)
        class AQuery(Query):
            pass

        @dataclass(frozen=True)
        class AnEvent(Event):
            pass

        class AnEffectHandler:
            @dispatch
            def handle(self, a_command: ACommand):
                pass

            @dispatch
            def handle(self, a_query: AQuery):
                return {"result": "query handled"}

            @dispatch
            def handle(self, an_event: AnEvent):
                pass

        class DummyDomainModule(DomainModule):
            def effect_handlers(self) -> List[Type]:
                return [AnEffectHandler]

        config = {}
        domains = [DummyDomainModule]
        app = Application(config=config, domains=domains)
        app.start()
        # TODO Improve assertions
        app.command_bus.handle(ACommand())
        app.event_bus.handle([AnEvent()])
        self.assertEqual({"result": "query handled"}, app.query_bus.handle(AQuery()))
