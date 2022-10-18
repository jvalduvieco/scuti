from typing import TypeVar, Type, Callable

from injector import inject

from domain.cqrs.bus.exceptions import NoHandlerForEffect, AlreadyRegisteredEffect
from domain.cqrs.bus.command_bus import CommandBus
from domain.cqrs.effects import Command
from infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus

T = TypeVar('T', bound=Command)


class CommandBusFacade(CommandBus):
    @inject
    def __init__(self, bus: LocalAsynchronousBus):
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
