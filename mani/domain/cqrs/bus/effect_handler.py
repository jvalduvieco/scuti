from abc import ABC

from mani.domain.cqrs.effects import Effect


class EffectHandler(ABC):
    def handle(self, effect: Effect):
        pass
