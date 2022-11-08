import queue
import traceback
from typing import Type, Callable, List, Dict, Optional

from mani.domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from mani.domain.cqrs.bus.hooks.bus_hook import BusHook
from mani.domain.cqrs.effects import Effect
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class LocalAsynchronousBus(AsynchronousBus):
    def __init__(self):
        self.__bus_hooks: List[BusHook] = []
        self.__handlers = {}
        self.__items = queue.Queue()

    def drain(self, should_block: bool = False) -> None:
        while not self.is_empty() or should_block:
            item = self.__items.get()
            current_item_type = type(item)
            [hook.begin_processing(item) for hook in self.__bus_hooks]
            if current_item_type in self.__handlers:
                for (handler, human_friendly_name) in self.__handlers[current_item_type]:
                    try:
                        [hook.before_handler(item, human_friendly_name) for hook in self.__bus_hooks]
                        handler(item)
                        [hook.after_handler(item, human_friendly_name) for hook in self.__bus_hooks]
                    except Exception as e:
                        self.__items.put(BusHandlerFailed(effect=item, error=e.__str__(),
                                                          stack_trace=''.join(traceback.format_exc())))
            [hook.end_processing(item) for hook in self.__bus_hooks]
            self.__items.task_done()

    def subscribe(self,
                  item_type: Type[Effect], handler: Callable[[Effect], None],
                  human_friendly_name: Optional[str] = None):
        if item_type in self.__handlers:
            self.__handlers[item_type] += [(handler, human_friendly_name)]
        else:
            self.__handlers[item_type] = [(handler, human_friendly_name)]

    def handle(self, item: Effect):
        [hook.on_handle(item) for hook in self.__bus_hooks]
        self.__items.put(item)

    def handles(self, item_type: Type[Effect]):
        return item_type in self.__handlers

    def handled(self) -> Dict[str, Type[Effect]]:
        return {a_type.__name__: a_type for a_type in self.__handlers.keys()}

    def is_empty(self):
        return self.__items.empty()

    def register_hook(self, hook: BusHook):
        self.__bus_hooks.append(hook)
