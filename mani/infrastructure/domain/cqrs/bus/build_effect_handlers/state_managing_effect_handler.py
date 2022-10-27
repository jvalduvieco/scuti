from typing import Type, Optional, Callable, Iterable

from injector import Injector

from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import EffectToStateMapper
from mani.domain.cqrs.effects import Effect, Command, Event
from mani.domain.model.repository.repository import Repository


def build_asynchronous_state_managing_class_effect_handler(a_handler: Type[EffectHandler],
                                                           repository_type: Type[Repository],
                                                           state_mapper: Optional[EffectToStateMapper],
                                                           injector: Injector) -> Callable[[Effect], None]:
    command_bus = injector.get(CommandBus)
    event_bus = injector.get(EventBus)

    def handler(effect: Effect) -> None:
        handler_instance = injector.create_object(a_handler)
        repository = injector.get(repository_type)
        if state_mapper is not None:
            states = state_mapper(effect, repository)
            if not isinstance(states, Iterable):
                states = [states]

            for previous_state in states:
                state, effects = handler_instance.handle(previous_state, effect)
                if state is not None:
                    repository.save(state)
                [command_bus.handle(effect) for effect in effects if isinstance(effect, Command)]
                [event_bus.handle(effect) for effect in effects if isinstance(effect, Event)]
        else:
            state, effects = handler_instance.handle(effect)

            if state is not None:
                repository.save(state)
            [command_bus.handle(effect) for effect in effects if isinstance(effect, Command)]
            [event_bus.handle(effect) for effect in effects if isinstance(effect, Event)]

    return handler
