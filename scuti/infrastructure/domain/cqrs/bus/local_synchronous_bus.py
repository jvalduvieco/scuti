from typing import Any, Callable, Dict, Type

from injector import inject
from plum import dispatch

from scuti.domain.cqrs.bus.exceptions import AlreadyRegisteredEffect, NoHandlerForEffect
from scuti.domain.cqrs.effects import Effect

SynchronousEffectHandler = Callable[[Effect], Dict[str, Any]]


class LocalSynchronousBus:
    @inject
    def __init__(self):
        self._handlers: Dict[Type[Effect], SynchronousEffectHandler] = {}

    def subscribe(self, effect_type: Type[Effect], handler: SynchronousEffectHandler) -> None:
        if effect_type in self._handlers:
            raise AlreadyRegisteredEffect(f"A handler for {effect_type} is already registered")
        self._handlers[effect_type] = handler

    @dispatch
    def handle(self, effect: Effect) -> Dict:
        effect_type = type(effect)
        if effect_type in self._handlers:
            return self._handlers[effect_type](effect)
        else:
            raise NoHandlerForEffect(f"Could not find a handler for {effect_type}")

    def handles(self, item_type: Type[Effect]) -> bool:
        return item_type in self._handlers.keys()
