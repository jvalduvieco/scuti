from abc import ABC
from typing import Generic, TypeVar, Optional

from mani.domain.cqrs.effects import Effect

Item = TypeVar("Item")


class BusHook(Generic[Item], ABC):
    def on_handle(self, item: Item):
        pass

    def begin_processing(self, item: Item):
        pass

    def before_handler(self, item: Item, human_friendly_name: Optional[str]):
        pass

    def after_handler(self, item: Item, human_friendly_name: Optional[str]):
        pass

    def end_processing(self, item: Effect):
        pass
