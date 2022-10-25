import queue
import traceback
from typing import Type, Callable, List, Dict

from mani.domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from mani.domain.cqrs.effects import Effect
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class LocalAsynchronousBus(AsynchronousBus):
    def __init__(self):
        self.__handlers = {}
        self.__items = queue.Queue()

    def drain(self, should_block: bool = False) -> None:
        while not self.is_empty() or should_block:
            item = self.__items.get()
            current_item_type = type(item)
            if current_item_type in self.__handlers:
                for handler in self.__handlers[current_item_type]:
                    try:
                        handler(item)
                    except Exception as e:
                        self.__items.put(BusHandlerFailed(effect=item, error=e.__str__(),
                                                          stack_trace=''.join(traceback.format_stack())))
            self.__items.task_done()

    def subscribe(self, item_type: Type[Effect], handler: Callable[[Effect], None]):
        if item_type in self.__handlers:
            self.__handlers[item_type] += [handler]
        else:
            self.__handlers[item_type] = [handler]

    def handle(self, items: Effect | List[Effect]):
        if isinstance(items, List):
            [self.__items.put(bus_item) for bus_item in items]
        else:
            self.__items.put(items)

    def handles(self, item_type: Type[Effect]):
        return item_type in self.__handlers

    def handled(self) -> Dict[str, Type[Effect]]:
        return {a_type.__name__: a_type for a_type in self.__handlers.keys()}

    def is_empty(self):
        return self.__items.empty()
