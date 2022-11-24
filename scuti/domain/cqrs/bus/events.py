from dataclasses import dataclass

from scuti.domain.cqrs.effects import Effect
from scuti.domain.errors import ErrorEvent


@dataclass(frozen=True)
class BusHandlerFailed(ErrorEvent):
    effect: Effect

    @classmethod
    def from_effect_and_exception(cls, effect: Effect, exception: Exception):
        return BusHandlerFailed(effect=effect,
                                error=f"{exception.__class__.__name__}({exception.__str__()})",
                                stack_trace=exception.__traceback__)


@dataclass(frozen=True)
class InfrastructureError(ErrorEvent):
    pass

    @classmethod
    def from_exception(cls, e: Exception):
        return InfrastructureError(error=f"{e.__class__.__name__}({e.__str__()})",
                                   stack_trace=e.__traceback__)
