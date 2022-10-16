from dataclasses import dataclass
from typing import Tuple, List, Union

from plum import dispatch


@dataclass(frozen=True)
class Effect:
    pass


@dataclass(frozen=True)
class Event(Effect):
    pass


@dataclass(frozen=True)
class Command(Effect):
    pass


@dataclass(frozen=True)
class ANiceEvent(Event):
    pass


@dataclass(frozen=True)
class ACreationalCommand(Command):
    pass


@dataclass(frozen=True)
class ANiceCommand(Command):
    pass


@dataclass(frozen=True)
class AStinkyCommand(Command):
    pass


@dataclass(frozen=True)
class ANotSoNiceCommand(Command):
    pass


@dataclass(frozen=True)
class SomeState:
    pass


class ANicePlumHandler:
    def __init__(self, _some_dependency: int = 3, _another_dependency: str = "poo"):
        pass

    @dispatch
    def handle(self, command: ACreationalCommand) -> Tuple[SomeState, List[Effect]]:
        return SomeState(), []

    @dispatch
    def handle(self, state: SomeState, command: ANiceCommand) -> Tuple[SomeState, List[Effect]]:
        return state, []

    @dispatch
    def handle(self, state: SomeState, event: ANiceEvent) -> Tuple[SomeState, List[Effect]]:
        return state, []

    @dispatch
    def handle(self, state: SomeState, command: Union[AStinkyCommand, ANotSoNiceCommand]) -> Tuple[
        SomeState, List[Effect]]:
        return state, []
