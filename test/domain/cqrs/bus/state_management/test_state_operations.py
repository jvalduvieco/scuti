from abc import ABC
from dataclasses import dataclass
from typing import Type, List, Tuple

from injector import Scope, Module, SingletonScope
from plum import dispatch

from mani.domain.cqrs.bus.state_management.commands import DeleteState
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from mani.domain.cqrs.effects import Command, Query, Event
from mani.domain.model.modules import DomainModule
from mani.domain.model.repository.repository import Repository
from mani.domain.testing.test_cases.domain_test_case import DomainTestCase
from mani.infrastructure.domain.model.identifiable.uuid_id import UuidId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository

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
class _Changed(Command):
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
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, a_command: _Change):
        return None, [DeleteState(id=a_command.subject_id)]

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
