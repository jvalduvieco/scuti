from dataclasses import dataclass
from types import TracebackType

from mani.domain.cqrs.effects import Event, Effect


@dataclass(frozen=True)
class EffectErrors(Event):
    pass


@dataclass(frozen=True)
class BusHandlerFailed(EffectErrors):
    effect: Effect
    error: str
    stack_trace: TracebackType | None

    @classmethod
    def from_effect_and_exception(cls, effect: Effect, exception: Exception):
        return BusHandlerFailed(effect=effect,
                                error=f"{exception.__class__.__name__}({exception.__str__()})",
                                stack_trace=exception.__traceback__)


@dataclass(frozen=True)
class InfrastructureError(EffectErrors):
    error: str
    stack_trace: TracebackType | None

    @classmethod
    def from_exception(cls, e: Exception):
        return InfrastructureError(error=f"{e.__class__.__name__}({e.__str__()})",
                                   stack_trace=e.__traceback__)
