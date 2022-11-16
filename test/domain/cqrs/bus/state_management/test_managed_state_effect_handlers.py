from abc import ABC
from dataclasses import dataclass, replace, field
from typing import Type, List, Tuple, Dict

from hamcrest import has_item, instance_of
from injector import Scope, Module, SingletonScope
from plum import dispatch, NotFoundLookupError

from mani.domain.cqrs.bus.events import BusHandlerFailed
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from mani.domain.cqrs.bus.state_management.evolve import evolve
from mani.domain.cqrs.effects import Command, Query, Event
from mani.domain.model.modules import DomainModule
from mani.domain.model.repository.repository import Repository
from mani.domain.testing.test_cases.domain_test_case import DomainTestCase
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository

_BySubjectId = lambda e, r: r.by_id(e.subject_id)


@dataclass(frozen=True)
class Subject:
    id: UuidId
    some_data: int


@dataclass(frozen=True)
class EvolvedSubject(Subject):
    more_data: int


@dataclass(frozen=True)
class IndependentSubject:
    id: UuidId
    more_data: int


@dataclass(frozen=True)
class Create(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class Created(Event):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class AQuery(Query):
    subject_id: UuidId


@dataclass(frozen=True)
class AnotherQuery(Query):
    subject_id: UuidId


@dataclass(frozen=True)
class Change(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class AnotherChange(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class ChangeIndependent(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class SubjectChanged(Event):
    subject_id: UuidId
    data: int


@dataclass(frozen=True)
class Evolve(Command):
    subject_id: UuidId
    to: Type
    new_props: Dict = field(default_factory=dict)


@dataclass(frozen=True)
class SubjectEvolved(Event):
    subject_id: UuidId


class SubjectRepository(Repository[Subject, UuidId], ABC):
    pass


class SubjectRepositoryInMemory(InMemoryRepository[Subject, UuidId]):
    pass


class AnEffectHandler:
    @dispatch
    def handle(self, a_command: Create):
        return Subject(a_command.subject_id, a_command.some_data), [Created(a_command.subject_id, a_command.some_data)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: Subject, _: AQuery):
        return {"result": state.some_data}

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: EvolvedSubject | IndependentSubject, _: AnotherQuery):
        return {"result": state.more_data}

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: Subject, command: Change):
        next_state = replace(state, some_data=state.some_data + command.some_data)
        return next_state, [SubjectChanged(next_state.id, data=next_state.some_data)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: Subject, command: AnotherChange):
        next_state = replace(state, some_data=state.some_data + command.some_data)
        return next_state, [SubjectChanged(next_state.id, data=next_state.some_data)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: Subject, command: Evolve):
        next_state = evolve(state, command.to, **command.new_props)
        return next_state, [SubjectEvolved(next_state.id)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: EvolvedSubject, command: Change):
        next_state = replace(state, some_data=state.some_data - command.some_data)
        return next_state, [SubjectChanged(next_state.id, data=next_state.some_data)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: IndependentSubject, command: ChangeIndependent):
        next_state = replace(state, more_data=command.some_data * 3)
        return next_state, [SubjectChanged(next_state.id, data=next_state.more_data)]


class _TestDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(SubjectRepository, SubjectRepositoryInMemory, SingletonScope)]

    def effect_handlers(self) -> List[Type | Tuple[Type, Type[Repository]]]:
        return [(AnEffectHandler, SubjectRepository)]


class TestManagedStateEffectHandlers(DomainTestCase):
    modules = [_TestDomainModule]

    def test_can_create_a_new_state(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data)
        ])
        self.assertThatHandledEffects(has_item(Created(subject_id=subject_id, some_data=some_data)))

    def test_can_receive_effects_that_manipulate_previous_state(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data),
            Change(subject_id=subject_id, some_data=32)
        ])
        self.assertThatHandledEffects(has_item(SubjectChanged(subject_id=subject_id, data=some_data + 32)))

    def test_can_change_the_type_of_the_state(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data),
            Evolve(subject_id=subject_id, to=EvolvedSubject, new_props={"more_data": 33})
        ])
        self.assertThatHandledEffects(has_item(SubjectEvolved(subject_id=subject_id)))

    def test_effects_can_change_semantics_depending_on_state_type(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data),
            Evolve(subject_id=subject_id, to=EvolvedSubject, new_props={"more_data": 33}),
            Change(subject_id=subject_id, some_data=32)
        ])
        self.assertThatHandledEffects(has_item(SubjectChanged(subject_id=subject_id, data=some_data - 32)))

    def test_handlers_can_be_inherited_from_ancestor_state_evolutions(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data),
            Evolve(subject_id=subject_id, to=EvolvedSubject, new_props={"more_data": 33}),
            AnotherChange(subject_id=subject_id, some_data=32)
        ])
        self.assertThatHandledEffects(has_item(SubjectChanged(subject_id=subject_id, data=some_data + 32)))

    def test_effects_are_not_be_handled_on_a_given_state_evolution(self):
        subject_id = UuidId()
        self.feed_effects([
            Create(subject_id=subject_id, some_data=43),
            Evolve(subject_id=subject_id, to=IndependentSubject, new_props={"more_data": 2}),
            Change(subject_id=subject_id, some_data=23)
        ])
        self.assertThatHandledEffects(has_item(instance_of(BusHandlerFailed)), expect_errors=True)

    def test_effects_are_handled_on_a_given_state_evolution(self):
        subject_id = UuidId()
        self.feed_effects([
            Create(subject_id=subject_id, some_data=43),
            Evolve(subject_id=subject_id, to=IndependentSubject, new_props={"more_data": 2}),
            ChangeIndependent(subject_id=subject_id, some_data=23)
        ])
        self.assertThatHandledEffects(has_item(SubjectChanged(subject_id=subject_id, data=69)))

    def test_queries_can_be_performed(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            Create(subject_id=subject_id, some_data=some_data)
        ])
        self.assertEqual({"result": some_data}, self.make_query(AQuery(subject_id=subject_id)))

    def test_queries_can_fail_is_not_in_proper_evolution_stage(self):
        subject_id = UuidId()
        self.feed_effects([
            Create(subject_id=subject_id, some_data=42),
            Evolve(subject_id=subject_id, to=IndependentSubject, new_props={"more_data": 2}),
        ])
        with self.assertRaises(NotFoundLookupError):
            self.make_query(AQuery(subject_id=subject_id))

    def test_unions_are_supported_as_state_types(self):
        subject_id = UuidId()
        self.feed_effects([
            Create(subject_id=subject_id, some_data=43),
            Evolve(subject_id=subject_id, to=IndependentSubject, new_props={"more_data": 2}),
        ])
        self.assertEqual({"result": 2}, self.make_query(AnotherQuery(subject_id=subject_id)))
