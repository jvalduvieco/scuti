from typing import Type, Optional, Callable, Iterable

from injector import Injector

from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import EffectToStateMapper
from mani.domain.cqrs.effects import Effect
from mani.domain.model.repository.repository import Repository


def build_synchronous_state_managing_class_effect_handler(a_handler: Type[EffectHandler],
                                                           repository_type: Type[Repository],
                                                           state_mapper: Optional[EffectToStateMapper],
                                                           injector: Injector) -> Callable[[Effect], None]:
    def handler(effect: Effect) -> None:
        handler_instance = injector.create_object(a_handler)
        repository = injector.get(repository_type)
        if state_mapper is not None:
            state = state_mapper(effect, repository)
            if isinstance(state, Iterable):
                raise RuntimeError(
                    "Synchronous effect handlers can manage only one state, check your @state_fetcher annotation")

            return handler_instance.handle(state, effect)
        else:
            return handler_instance.handle(effect)

    return handler
