from typing import List, Dict
from unittest import TestCase

from hamcrest import assert_that
from hamcrest.core.matcher import Matcher
from plum import dispatch

from mani.domain.errors import ErrorEvent
from mani.domain.cqrs.effect_store.effect_store import EffectStore
from mani.domain.cqrs.effects import Command, Event, Query, Effect
from mani.domain.model.application.domain_application import DomainApplication
from mani.domain.testing.testing_domain_module import TestingDomainModule
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.logging.errors import print_traceback
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class DomainTestCase(TestCase):
    modules = []
    config = {}

    def __init__(self, something):
        super().__init__(something)

    def setUp(self) -> None:
        super().setUp()
        self.app = DomainApplication(domains=[TestingDomainModule] + self.modules, config=self.config)
        self.injector = self.app.injector()
        self.__bus = self.injector.get(AsynchronousBus)
        self._handled_effects = self.injector.get(EffectStore)

    def feed_effects(self, effects: List[Event | Command]) -> None:
        for effect in effects:
            self.__feed_effect(effect)
            self.drain_effects()

    def drain_effects(self) -> None:
        self.__bus.drain(block=False)

    def reset_emitted_effects(self):
        self._handled_effects.clear()

    def handled_effects(self) -> List[Effect]:
        return list(self._handled_effects)

    def assertThatHandledEffects(self, something: Matcher, expect_errors: bool = False):
        effects = self.handled_effects()
        errors = list(filter(lambda e: issubclass(e.__class__, ErrorEvent), effects))
        if errors and not expect_errors:
            for index, error in enumerate(errors):
                self.__print_error(error, index)
            raise AssertionError(f"Some error occurred: See description above")
        assert_that(effects, something)

    def make_query(self, a_query: Query) -> Dict:
        return self.app.query_bus.handle(a_query)

    @dispatch
    def __feed_effect(self, command: Command) -> None:
        self.app.command_bus.handle(command)

    @dispatch
    def __feed_effect(self, event: Event) -> None:
        self.app.event_bus.handle(event)

    def __print_error(self, e: ErrorEvent, index: int):
        prepared_stack_trace = e.stack_trace
        logger.error(f"### {index} ###")
        logger.error(
            f"{e.error}{f'while processing {e.effect}' if hasattr(e, 'effect') else ''} in {prepared_stack_trace}")
        print_traceback(logger, e.stack_trace)
