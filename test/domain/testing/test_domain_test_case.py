from abc import ABC
from dataclasses import dataclass, replace
from typing import List, Type, Tuple

from hamcrest import contains_exactly
from injector import Module, Scope, SingletonScope
from plum import dispatch

from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from scuti.domain.cqrs.effects import Command, Query, Event
from scuti.domain.model.modules import DomainModule
from scuti.domain.model.repository.repository import Repository
from scuti.domain.testing.matchers.any_id import match_any_id
from scuti.domain.testing.matchers.something_like import SomethingLike
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
class _AQuery(Query):
    subject_id: UuidId


@dataclass(frozen=True)
class _SubjectChanged(Event):
    subject_id: UuidId
    some_data: int


class _SubjectRepository(Repository[_Subject, UuidId], ABC):
    pass


class _SubjectRepositoryInMemory(InMemoryRepository[_Subject, UuidId]):
    pass


@dataclass(frozen=True)
class _SubjectCreated(Event):
    subject_id: UuidId
    some_data: int


class _AnEffectHandler:
    @dispatch
    def handle(self, a_command: _Create):
        return _Subject(a_command.subject_id, a_command.some_data), [
            _SubjectCreated(a_command.subject_id, some_data=23)]

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, _: _AQuery):
        return {"result": state.some_data}

    @dispatch
    @state_fetcher(_BySubjectId)
    def handle(self, state: _Subject, an_event: _SubjectChanged):
        return replace(state, some_data=state.some_data + an_event.some_data), []


class _DummyDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(_SubjectRepository, _SubjectRepositoryInMemory, SingletonScope)]

    def effect_handlers(self) -> List[Type | Tuple[Type, Type[Repository]]]:
        return [(_AnEffectHandler, _SubjectRepository)]


class TestDomainTestCase(DomainTestCase):
    modules = [_DummyDomainModule]

    def test_domain_modules_can_register_effect_handlers_with_external_state(self):
        subject_id = UuidId()
        self.feed_effects([_Create(subject_id=subject_id, some_data=23),
                           _SubjectChanged(subject_id=subject_id, some_data=44)])

        self.assertThatHandledEffects(
            contains_exactly(
                _Create(subject_id=subject_id, some_data=23),
                _SubjectCreated(subject_id=subject_id, some_data=23),
                SomethingLike(_SubjectChanged, subject_id=match_any_id(), some_data=44)
            ))
