from typing import TypeVar, Callable, Type, Dict, Generic

from mani.domain.cqrs.bus.bus import Bus
from mani.domain.cqrs.bus.exceptions import AlreadyRegisteredEffect, NoHandlerForEffect
from mani.domain.cqrs.effects import Effect

HandledTypeBase = TypeVar('HandledTypeBase')
ResultType = TypeVar('ResultType')
SynchronousHandler = Callable[[HandledTypeBase], ResultType]


class LocalSynchronousBus(Generic[HandledTypeBase, ResultType], Bus):
    def __init__(self):
        self._handlers: Dict[Type[HandledTypeBase], SynchronousHandler] = {}

    def subscribe(self, effect_type: Type[HandledTypeBase], handler: SynchronousHandler) -> None:
        if effect_type in self._handlers:
            raise AlreadyRegisteredEffect(f"A handler for {effect_type} is already registered")
        self._handlers[effect_type] = handler

    def handle(self, an_effect: HandledTypeBase) -> ResultType:
        effect_type = type(an_effect)
        if effect_type in self._handlers:
            return self._handlers[effect_type](an_effect)
        else:
            raise NoHandlerForEffect(f"Could not find a handler for {effect_type}")

    def handled(self) -> Dict[str, Type[Effect]]:
        return {a_type.__name__: a_type for a_type in self._handlers.keys()}
