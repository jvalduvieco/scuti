from dataclasses import dataclass
from typing import Tuple, List, Union

from plum import dispatch


@dataclass(frozen=True)
class _Effect:
    pass


@dataclass(frozen=True)
class _Event(_Effect):
    pass


@dataclass(frozen=True)
class _Command(_Effect):
    pass


@dataclass(frozen=True)
class ANiceEvent(_Event):
    pass


@dataclass(frozen=True)
class ACreationalCommand(_Command):
    pass


@dataclass(frozen=True)
class ANiceCommand(_Command):
    pass


@dataclass(frozen=True)
class AStinkyCommand(_Command):
    pass


@dataclass(frozen=True)
class ANotSoNiceCommand(_Command):
    pass


@dataclass(frozen=True)
class SomeState:
    pass


class ANicePlumHandler:
    def __init__(self, _some_dependency: int = 3, _another_dependency: str = "poo"):
        pass

    @dispatch
    def handle(self, command: ACreationalCommand) -> Tuple[SomeState, List[_Effect]]:
        return SomeState(), []

    @dispatch
    def handle(self, state: SomeState, command: ANiceCommand) -> Tuple[SomeState, List[_Effect]]:
        return state, []

    @dispatch
    def handle(self, state: SomeState, event: ANiceEvent) -> Tuple[SomeState, List[_Effect]]:
        return state, []

    @dispatch
    def handle(self, state: SomeState, command: Union[AStinkyCommand, ANotSoNiceCommand]) -> Tuple[
        SomeState, List[_Effect]]:
        return state, []
