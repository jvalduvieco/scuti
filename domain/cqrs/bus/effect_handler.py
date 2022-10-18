from abc import ABC

from domain.cqrs.effects import Effect


class EffectHandler(ABC):
    def handle(self, effect: Effect):
        pass
