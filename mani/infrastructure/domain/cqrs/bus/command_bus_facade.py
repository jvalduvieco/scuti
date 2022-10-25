from typing import TypeVar, Type, Callable

from injector import inject

from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.exceptions import NoHandlerForEffect, AlreadyRegisteredEffect
from mani.domain.cqrs.effects import Command
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class CommandBusFacade(CommandBus):
    @inject
    def __init__(self, bus: AsynchronousBus):
        self.__bus = bus

    def subscribe(self, effect_type: Type[Command], handler: Callable[[Command], None]):
        if self.__bus.handles(effect_type):
            raise AlreadyRegisteredEffect(effect_type)
        else:
            self.__bus.subscribe(effect_type, handler)

    def handle(self, command: Command):
        if not self.__bus.handles(type(command)):
            raise NoHandlerForEffect(command)
        self.__bus.handle(command)
