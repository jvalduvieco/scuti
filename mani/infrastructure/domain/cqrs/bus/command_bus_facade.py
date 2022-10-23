from typing import TypeVar, Type, Callable, List, Dict

from injector import inject

from mani.domain.cqrs.bus.bus import Bus
from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.exceptions import NoHandlerForEffect, AlreadyRegisteredEffect
from mani.domain.cqrs.effects import Command, Effect
from mani.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus

T = TypeVar('T', bound=Command)


class CommandBusFacade(CommandBus):
    @inject
    def __init__(self, bus: Bus):
        self.__bus = bus

    def subscribe(self, effect_type: Type[T], handler: Callable[[T], None]):
        if self.__bus.handles(effect_type):
            raise AlreadyRegisteredEffect(effect_type)
        else:
            self.__bus.subscribe(effect_type, handler)

    def handle(self, command: Command):
        if not self.__bus.handles(type(command)):
            raise NoHandlerForEffect(command)
        self.__bus.handle(command)

    def handled(self) -> Dict[str, Type[Effect]]:
        return self.__bus.handled()

    def handles(self, item_type: Type[Effect]):
        return self.__bus.handles(item_type)
