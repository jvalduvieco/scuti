from abc import ABC, abstractmethod

from mani.domain.cqrs.effects import Effect


class EffectHandler(ABC):
    @abstractmethod
    def handle(self, effect: Effect):
        pass
