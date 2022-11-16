from typing import List, Dict
from unittest import TestCase

from hamcrest import assert_that
from hamcrest.core.matcher import Matcher
from mani.domain.cqrs.bus.events import BusHandlerFailed
from mani.domain.cqrs.effect_store.effect_store import EffectStore
from mani.domain.cqrs.effects import Command, Event, Query, Effect
from mani.domain.model.application.domain_application import DomainApplication
from mani.domain.testing.testing_domain_module import TestingDomainModule
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.logging.get_logger import get_logger
from plum import dispatch

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
        self.__bus.drain()

    def reset_emitted_effects(self):
        self._handled_effects.clear()

    def handled_effects(self) -> List[Effect]:
        return list(self._handled_effects)

    def assertThatHandledEffects(self, something: Matcher):
        effects = self.handled_effects()
        errors = list(filter(lambda e: type(e) == BusHandlerFailed, effects))
        if errors:
            for index, error in enumerate(errors):
                print_error(error, index)
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


def print_error(e, index):
    prepared_stack_trace = e.stack_trace
    logger.error(f"### {index} ###")
    logger.error(f"{e.error} while processing {e.effect} in {prepared_stack_trace}")
    print_tb(e.stack_trace)


def print_tb(tb):
    local_vars = {}
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        line_no = tb.tb_lineno
        # Prepend desired color (e.g. RED) to line
        logger.error(f"\tFile {filename} line {line_no}, in {name}")

        local_vars = tb.tb_frame.f_locals
        tb = tb.tb_next
    logger.error(f"Local variables in top frame: \n\t{local_vars}")
