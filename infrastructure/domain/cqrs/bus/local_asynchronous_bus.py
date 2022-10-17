import queue
import traceback
from typing import TypeVar, Type, Callable, Union, List, Generic
from domain.cqrs.bus.bus_handler_failed import BusHandlerFailed

HandledTypeBase = TypeVar('HandledTypeBase')
ASynchronousHandler = Callable[[HandledTypeBase], None]


class LocalAsynchronousBus(Generic[HandledTypeBase]):
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
                        self.__items.put(BusHandlerFailed(effect=item, error=e.__str__(), stack_trace=''.join(traceback.format_stack())))
            self.__items.task_done()

    def register(self, item_type: Type[HandledTypeBase], handler: ASynchronousHandler):
        if item_type in self.__handlers:
            self.__handlers[item_type] += [handler]
        else:
            self.__handlers[item_type] = [handler]

    def handle(self, items: Union[HandledTypeBase, List[HandledTypeBase]]):
        if isinstance(items, List):
            [self.__items.put(bus_item) for bus_item in items]
        else:
            self.__items.put(items)

    def handles(self, item_type: Type[HandledTypeBase]):
        return item_type in self.__handlers

    def is_empty(self):
        return self.__items.empty()
