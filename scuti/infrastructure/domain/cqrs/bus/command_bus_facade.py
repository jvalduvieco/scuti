from typing import Type, Callable

from injector import inject

from scuti.domain.cqrs.bus.command_bus import CommandBus
from scuti.domain.cqrs.bus.exceptions import NoHandlerForEffect, AlreadyRegisteredEffect
from scuti.domain.cqrs.effects import Command
from scuti.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


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
