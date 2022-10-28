from typing import List
from unittest import TestCase

from hamcrest import assert_that
from hamcrest.core.matcher import Matcher
from plum import dispatch

from common.testing_domain_module import TestingDomainModule
from mani.domain.cqrs.effect_store.effect_store import EffectStore
from mani.domain.cqrs.effects import Command, Event, Effect
from mani.domain.model.application.domain_application import DomainApplication
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


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
        assert_that(self.handled_effects(), something)

    @dispatch
    def __feed_effect(self, command: Command) -> None:
        self.app.command_bus.handle(command)

    @dispatch
    def __feed_effect(self, event: Event) -> None:
        self.app.event_bus.handle(event)
