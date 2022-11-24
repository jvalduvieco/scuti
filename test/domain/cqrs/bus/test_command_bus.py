from dataclasses import dataclass
from unittest import TestCase

from scuti.domain.cqrs.bus.exceptions import NoHandlerForEffect, AlreadyRegisteredEffect
from scuti.domain.cqrs.effects import Command
from scuti.infrastructure.domain.cqrs.bus.command_bus_facade import CommandBusFacade
from scuti.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus


@dataclass(frozen=True)
class _ACommand(Command):
    pass


@dataclass(frozen=True)
class _AnotherCommand(Command):
    pass


def _a_simple_handler(command: _ACommand) -> None:
    pass


class TestCommandBusFacade(TestCase):
    def test_can_register_command_handlers(self):
        a_command_bus = CommandBusFacade(LocalAsynchronousBus())

        self.assertIsNone(a_command_bus.subscribe(_ACommand, _a_simple_handler))

    def test_can_not_register_a_handler_for_a_command_twice(self):
        a_command_bus = CommandBusFacade(LocalAsynchronousBus())
        a_command_bus.subscribe(_ACommand, _a_simple_handler)
        with self.assertRaises(AlreadyRegisteredEffect):
            a_command_bus.subscribe(_ACommand, _a_simple_handler)

    def test_can_handle_commands(self):
        inner_bus = LocalAsynchronousBus()
        called_handlers = []

        def spying_command_handler(command: _ACommand) -> None:
            called_handlers.append(command)

        a_command_bus = CommandBusFacade(inner_bus)
        a_command_bus.subscribe(_ACommand, spying_command_handler)
        a_command_bus.handle(_ACommand())
        inner_bus.drain()
        self.assertEqual(1, called_handlers.__len__())

    def test_unhandled_commands_raise_an_exception(self):
        a_command_bus = CommandBusFacade(LocalAsynchronousBus())
        with self.assertRaises(NoHandlerForEffect):
            a_command_bus.handle(_ACommand())
