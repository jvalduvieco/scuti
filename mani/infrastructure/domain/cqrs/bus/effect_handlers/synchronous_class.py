from typing import Type, Callable, Dict

from injector import Injector

from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Effect


def build_synchronous_class_effect_handler(a_handler: Type[EffectHandler], injector: Injector) -> Callable[[Effect], Dict]:
    def handler(effect: Effect) -> Dict:
        handler_instance = injector.create_object(a_handler)
        return handler_instance.handle(effect)
    return handler
