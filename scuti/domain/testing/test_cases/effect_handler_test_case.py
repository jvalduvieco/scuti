from typing import List, Any
from unittest import TestCase

from scuti.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from scuti.domain.cqrs.effects import Effect
from scuti.infrastructure.tools.list import filter_none


class EffectHandlerTestCase(TestCase):
    def feed_effects(self, into: ManagedStateEffectHandler, effects: List[Effect], initial_state: Any = "None"):
        current_state = initial_state
        emitted_effects = []
        for effect in effects:
            if current_state != "None":
                state, effects = into.handle(current_state, effect)
            else:
                state, effects = into.handle(effect)
            current_state = state
            emitted_effects += filter_none(effects)
        return current_state, emitted_effects
