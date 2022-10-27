from typing import Type, Callable

from injector import Injector

from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Effect


def build_asynchronous_class_effect_handler(a_handler: Type[EffectHandler], injector: Injector) -> \
        Callable[[Effect], None]:
    def handler(effect: Effect) -> None:
        handler_instance = injector.create_object(a_handler)
        handler_instance.handle(effect)

    return handler
