from abc import ABC
from typing import List, Callable, Union, Type, Tuple

from domain.cqrs.effects import Command, Query
from domain.cqrs.bus.query_handler import QueryHandler


class CommandHandler:
    pass


class DomainModule(ABC):
    def bindings(self) -> List[Callable[[Binder], None]]:
        return []

    def sagas(self) -> List[Type]:
        return []

    def command_handlers(self) -> List[Union[Type[CommandHandler], Tuple[Type[CommandHandler], Type]]]:
        return []

    def event_handlers(self) -> List[Union[Type, Tuple[Type, Type]]]:
        return []

    def query_handlers(self) -> List[Tuple[List[Type[Query]], Type[QueryHandler]]]:
        return []

    def projections(self) -> List[Type]:
        return []

    def init_commands(self) -> List[Command]:
        return []
