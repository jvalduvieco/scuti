from abc import ABC
from dataclasses import dataclass, replace
from typing import Type, List, Tuple

from hamcrest import not_, instance_of, has_item
from injector import Scope, Module, SingletonScope
from plum import dispatch

from scuti.domain.cqrs.bus.state_management.commands import DeleteState
from scuti.domain.cqrs.bus.state_management.condition import condition
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from scuti.domain.cqrs.effects import Command, Query, Event
from scuti.domain.model.modules import DomainModule
from scuti.domain.model.repository.repository import Repository
from scuti.domain.testing.test_cases.domain_test_case import DomainTestCase
from scuti.infrastructure.domain.model.identifiable.uuid_id import UuidId
from scuti.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository

_BySubjectId = lambda e, r: r.by_id(e.subject_id)


@dataclass(frozen=True)
class _Subject:
    id: UuidId
    some_data: int


@dataclass(frozen=True)
class _Create(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class _Change(Command):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class _Changed(Event):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class _KillMe(Command):
    subject_id: UuidId


@dataclass(frozen=True)
class _Created(Event):
    subject_id: UuidId
    some_data: int


@dataclass(frozen=True)
class _AQuery(Query):
    subject_id: UuidId


class _SubjectRepository(Repository[_Subject, UuidId], ABC):
    pass


class _SubjectRepositoryInMemory(InMemoryRepository[_Subject, UuidId]):
    pass


class _AnEffectHandler:
    @dispatch
    def handle(self, a_command: _Create):
        return _Subject(a_command.subject_id, a_command.some_data), [
            _Created(a_command.subject_id, a_command.some_data)]

    @dispatch
    @condition(lambda e: e.some_data > 30)
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, a_command: _Change):
        next_state = replace(state, some_data=a_command.some_data)
        return next_state, [_Changed(subject_id=a_command.subject_id, some_data=next_state.some_data)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, a_command: _KillMe):
        return None, [DeleteState(id=a_command.subject_id)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, _: _AQuery):
        return {"result": state.some_data}


class _TestDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(_SubjectRepository, _SubjectRepositoryInMemory, SingletonScope)]

    def effect_handlers(self) -> List[Type | Tuple[Type, Type[Repository]]]:
        return [(_AnEffectHandler, _SubjectRepository)]


class TestStateOperations(DomainTestCase):
    modules = [_TestDomainModule]

    def test_state_can_be_eliminated(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            _Create(subject_id=subject_id, some_data=some_data),
            _KillMe(subject_id=subject_id)
        ])
        with self.assertRaises(KeyError):
            self.make_query(_AQuery(subject_id=subject_id))

    def test_effect_handling_is_not_made_if_condition_is_not_met(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            _Create(subject_id=subject_id, some_data=some_data),
            _Change(subject_id=subject_id, some_data=23)
        ])
        self.assertThatHandledEffects(not_(has_item(instance_of(_Changed))))

    def test_effect_handling_is_made_if_condition_is_met(self):
        subject_id = UuidId()
        some_data = 43
        self.feed_effects([
            _Create(subject_id=subject_id, some_data=some_data),
            _Change(subject_id=subject_id, some_data=46)
        ])
        self.assertThatHandledEffects(has_item(instance_of(_Changed)))
