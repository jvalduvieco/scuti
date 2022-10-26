import unittest
from abc import ABC
from dataclasses import dataclass, replace
from typing import Tuple, List

from injector import Injector, SingletonScope
from plum import dispatch

from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher, Singleton, All
from mani.domain.cqrs.effects import Command, Effect
from mani.domain.model.identifiable.identifiable_entity import IdentifiableEntity
from mani.domain.model.repository.repository import Repository
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.domain.cqrs.bus.command_bus_facade import CommandBusFacade
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.state_managing_effect_handler import \
    build_asynchronous_state_managing_class_effect_handler
from mani.infrastructure.domain.cqrs.bus.event_bus_facade import EventBusFacade
from mani.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus
from mani.infrastructure.domain.cqrs.bus.local_synchronous_query_bus import LocalSynchronousQueryBus
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


@dataclass(frozen=True)
class Create(Command):
    subject_id: UuidId
    some_data: int
    operation_id: UuidId


@dataclass(frozen=True)
class Modify(Command):
    subject_id: UuidId
    some_data: int
    operation_id: UuidId


@dataclass(frozen=True)
class Subject(IdentifiableEntity):
    id: UuidId
    some_data: int


class AStateManagingEffectHandler(EffectHandler):
    @dispatch
    def handle(self, an_effect: Create) -> Tuple[Subject, List[Effect]]:
        return Subject(id=an_effect.subject_id, some_data=an_effect.some_data), []

    @dispatch
    @state_fetcher(lambda e, r: r.by_id(e.subject_id))
    def handle(self, state: Subject, an_effect: Modify) -> Tuple[Subject, List[Effect]]:
        return replace(state, some_data=state.some_data + an_effect.some_data), []


class SubjectRepository(Repository[Subject, UuidId], ABC):
    pass


class SubjectRepositoryInMemory(InMemoryRepository[Subject, UuidId]):
    pass


class TestStateManagingEffectHandlers(unittest.TestCase):
    def setUp(self):
        self.bus = bus = LocalAsynchronousBus()
        self.command_bus = command_bus = CommandBusFacade(bus)
        self.event_bus = event_bus = EventBusFacade(bus)
        self.query_bus = query_bus = LocalSynchronousQueryBus()
        self.injector = injector = Injector()
        injector.binder.bind(SubjectRepository, SubjectRepositoryInMemory, SingletonScope)
        injector.binder.bind(AsynchronousBus, bus, SingletonScope)
        injector.binder.bind(CommandBus, command_bus, SingletonScope)
        injector.binder.bind(EventBus, event_bus, SingletonScope)
        injector.binder.bind(QueryBus, query_bus, SingletonScope)

    def test_an_effect_can_create_a_new_state(self):
        a_repository = self.injector.get(SubjectRepository)

        self.command_bus.subscribe(Create,
                                   build_asynchronous_state_managing_class_effect_handler(
                                       a_handler=AStateManagingEffectHandler,
                                       repository_type=SubjectRepository,
                                       state_mapper=None,
                                       injector=self.injector))

        a_create_subject_command = Create(subject_id=UuidId(), some_data=3, operation_id=UuidId())
        self.command_bus.handle(a_create_subject_command)
        self.bus.drain()
        self.assertEqual(Subject(a_create_subject_command.subject_id, a_create_subject_command.some_data),
                         a_repository.by_id(a_create_subject_command.subject_id))

    def test_a_handler_can_retrieve_previous_state_before_calling_a_handler_based_on_an_annotation(self):
        a_repository = self.injector.get(SubjectRepository)

        self.command_bus.subscribe(Create,
                                   build_asynchronous_state_managing_class_effect_handler(
                                       a_handler=AStateManagingEffectHandler,
                                       repository_type=SubjectRepository,
                                       state_mapper=None,
                                       injector=self.injector))
        self.command_bus.subscribe(Modify,
                                   build_asynchronous_state_managing_class_effect_handler(
                                       a_handler=AStateManagingEffectHandler,
                                       repository_type=SubjectRepository,
                                       state_mapper=lambda e, r: r.by_id(e.subject_id),
                                       injector=self.injector))
        subject_id = UuidId()
        a_create_subject_command = Create(subject_id=subject_id, some_data=3, operation_id=UuidId())
        a_modify_subject_command = Modify(subject_id=subject_id, some_data=39, operation_id=UuidId())
        self.command_bus.handle(a_create_subject_command)
        self.command_bus.handle(a_modify_subject_command)
        self.bus.drain()
        self.assertEqual(Subject(a_create_subject_command.subject_id, 42),
                         a_repository.by_id(a_create_subject_command.subject_id))

    def test_exists_an_all_annotation(self):
        a_repository = self.injector.get(SubjectRepository)

        self.command_bus.subscribe(Create,
                                   build_asynchronous_state_managing_class_effect_handler(
                                       a_handler=AStateManagingEffectHandler,
                                       repository_type=SubjectRepository,
                                       state_mapper=None,
                                       injector=self.injector))
        self.command_bus.subscribe(Modify,
                                   build_asynchronous_state_managing_class_effect_handler(
                                       a_handler=AStateManagingEffectHandler,
                                       repository_type=SubjectRepository,
                                       state_mapper=All,
                                       injector=self.injector))
        subject_id = UuidId()
        a_create_subject_command = Create(subject_id=subject_id, some_data=3, operation_id=UuidId())
        a_modify_subject_command = Modify(subject_id=subject_id, some_data=39, operation_id=UuidId())
        self.command_bus.handle(a_create_subject_command)
        self.command_bus.handle(a_modify_subject_command)
        self.bus.drain()
        self.assertEqual(Subject(a_create_subject_command.subject_id, 42),
                         a_repository.by_id(a_create_subject_command.subject_id))

