import queue
from typing import Type, Callable, List, Dict, Optional

from mani.domain.cqrs.bus.events import BusHandlerFailed
from mani.domain.cqrs.bus.hooks.bus_hook import BusHook
from mani.domain.cqrs.effects import Effect
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class LocalAsynchronousBus(AsynchronousBus):
    def __init__(self):
        self.__bus_hooks: List[BusHook] = []
        self.__handlers = {}
        self.__items = queue.Queue()

    def drain(self, block: bool = True) -> None:
        while item := self.__get_item(block):
            current_item_type = type(item)
            [hook.begin_processing(item) for hook in self.__bus_hooks]
            if current_item_type in self.__handlers:
                for (handler, human_friendly_name) in self.__handlers[current_item_type]:
                    try:
                        [hook.before_handler(item, human_friendly_name) for hook in self.__bus_hooks]
                        handler(item)
                        [hook.after_handler(item, human_friendly_name) for hook in self.__bus_hooks]
                    except Exception as e:
                        self.handle(BusHandlerFailed.from_effect_and_exception(effect=item, exception=e))
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

    def __get_item(self, block: bool):
        try:
            return self.__items.get(block=block, timeout=0.5)
        except queue.Empty:
            pass
        return None
