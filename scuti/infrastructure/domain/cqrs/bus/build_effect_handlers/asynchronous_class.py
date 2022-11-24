from typing import Type, Callable, Optional

from injector import Injector

from scuti.domain.cqrs.bus.effect_handler import EffectHandler
from scuti.domain.cqrs.bus.state_management.condition import HandlerCondition
from scuti.domain.cqrs.effects import Effect


def build_asynchronous_class_effect_handler(a_handler: Type[EffectHandler], condition: Optional[HandlerCondition],
                                            injector: Injector) -> \
        Callable[[Effect], None]:
    def handler(effect: Effect) -> None:
        if condition is not None and not condition(effect):
            return
        handler_instance = injector.create_object(a_handler)
        handler_instance.handle(effect)

    return handler
