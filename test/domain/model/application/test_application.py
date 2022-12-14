import unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import List, Tuple, Type
from unittest import skip

from injector import Binder, Module, Scope, SingletonScope, inject
from plum import dispatch

from scuti.domain.cqrs.bus.command_bus import CommandBus
from scuti.domain.cqrs.bus.event_bus import EventBus
from scuti.domain.cqrs.bus.exceptions import NoHandlerForEffect
from scuti.domain.cqrs.bus.query_bus import QueryBus
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from scuti.domain.cqrs.effects import Command, Event, Query
from scuti.domain.model.application.domain_application import DomainApplication
from scuti.domain.model.modules import DomainModule
from scuti.domain.model.repository.repository import Repository
from scuti.infrastructure.domain.model.identifiable.uuid_id import UuidId
from scuti.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository
from scuti.infrastructure.threading.thread import Thread


class TestApplication(unittest.TestCase):
    def test_can_create_an_application(self):
        config = {}
        domains = []
        app = DomainApplication(config=config, domains=domains)
        self.assertTrue(app)

    def test_can_access_command_bus(self):
        config = {}
        domains = []
        app = DomainApplication(config=config, domains=domains)
        self.assertTrue(issubclass(app.command_bus.__class__, CommandBus))

    def test_can_access_event_bus(self):
        config = {}
        domains = []
        app = DomainApplication(config=config, domains=domains)
        self.assertTrue(issubclass(app.event_bus.__class__, EventBus))

    def test_can_access_query_bus(self):
        config = {}
        domains = []
        app = DomainApplication(config=config, domains=domains)
        self.assertTrue(issubclass(app.query_bus.__class__, QueryBus))

    def test_can_register_domain_modules(self):
        class DummyDomainModule(DomainModule):
            pass

        config = {}
        domains = [DummyDomainModule]
        app = DomainApplication(config=config, domains=domains)
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
        app = DomainApplication(config=config, domains=domains)
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
        app = DomainApplication(config=config, domains=domains)
        self.assertEqual(SomethingConcrete, app.injector().get(SomethingAbstract).__class__)

    def test_domain_modules_can_define_a_list_of_initial_commands_that_are_executed_on_starting_application(self):
        @dataclass(frozen=True)
        class ACommand(Command):
            pass

        class DummyDomainModule(DomainModule):
            def init(self) -> List[Command]:
                return [ACommand()]

        config = {}
        domains = [DummyDomainModule]
        app = DomainApplication(config=config, domains=domains)
        with self.assertRaises(NoHandlerForEffect):
            app.start()
        app.stop()

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
        app = DomainApplication(config=config, domains=domains)
        app.start()
        # TODO Improve assertions
        app.command_bus.handle(ACommand())
        app.event_bus.handle(AnEvent())
        app.stop()
        self.assertEqual({"result": "query handled"}, app.query_bus.handle(AQuery()))

    def test_domain_modules_can_register_effect_handlers_with_external_state(self):
        BySubjectId = lambda e, r: r.by_id(e.subject_id)

        @dataclass(frozen=True)
        class Subject:
            id: UuidId
            some_data: int

        @dataclass(frozen=True)
        class Create(Command):
            subject_id: UuidId
            some_data: int

        @dataclass(frozen=True)
        class AQuery(Query):
            subject_id: UuidId

        @dataclass(frozen=True)
        class SubjectChanged(Event):
            subject_id: UuidId
            some_data: int

        class SubjectRepository(Repository[Subject, UuidId], ABC):
            pass

        class SubjectRepositoryInMemory(InMemoryRepository[Subject, UuidId]):
            pass

        class AnEffectHandler:
            @dispatch
            def handle(self, a_command: Create):
                return Subject(a_command.subject_id, a_command.some_data), []

            @dispatch
            @state_fetcher(BySubjectId)
            def handle(self, state: Subject, _: AQuery):
                return {"result": state.some_data}

            @dispatch
            @state_fetcher(BySubjectId)
            def handle(self, state: Subject, an_event: SubjectChanged):
                return replace(state, some_data=state.some_data + an_event.some_data), []

        class DummyDomainModule(DomainModule):
            def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
                return [(SubjectRepository, SubjectRepositoryInMemory, SingletonScope)]

            def effect_handlers(self) -> List[Type | Tuple[Type, Type[Repository]]]:
                return [(AnEffectHandler, SubjectRepository)]

        config = {}
        domains = [DummyDomainModule]
        app = DomainApplication(config=config, domains=domains)
        app.start()
        subject_id = UuidId()
        app.command_bus.handle(Create(subject_id=subject_id, some_data=23))
        app.event_bus.handle(SubjectChanged(subject_id=subject_id, some_data=44))
        # app.injector().get(AsynchronousBus).drain()
        app.stop()
        self.assertEqual({"result": 67}, app.query_bus.handle(AQuery(subject_id=subject_id)))

    def test_domain_modules_can_define_a_list_processes_that_are_executed_on_starting_application(self):
        @dataclass(frozen=True)
        class AnEvent(Event):
            a_prop: int

        class IDie(Thread):
            ran = False
            @inject
            def __init__(self, event_bus: EventBus):
                super().__init__()
                self.__event_bus = event_bus

            def get_name(self):
                return "IDie"

            def execute(self):
                IDie.ran = True

            def wants_to_stop(self):
                pass

        class DummyDomainModule(DomainModule):
            def processes(self) -> List[Type[Thread]]:
                return [
                    IDie
                ]

        config = {}
        domains = [DummyDomainModule]
        app = DomainApplication(config=config, domains=domains)
        called_event_handlers = []
        app.start()
        app.stop()
        self.assertEqual(True, IDie.ran)
