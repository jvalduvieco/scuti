from typing import Type, Callable, Dict, Optional

from injector import Injector

from scuti.domain.cqrs.bus.effect_handler import EffectHandler
from scuti.domain.cqrs.bus.state_management.condition import HandlerCondition
from scuti.domain.cqrs.effects import Effect


def build_synchronous_class_effect_handler(a_handler: Type[EffectHandler], condition: Optional[HandlerCondition],
                                           injector: Injector) -> Callable[[Effect], Dict]:
    if condition is not None:
        raise ValueError(
            f"synchronous_class_effect_handler do not support conditions {a_handler.__name__}")

    def handler(effect: Effect) -> Dict:
        handler_instance = injector.create_object(a_handler)
        return handler_instance.handle(effect)

    return handler
