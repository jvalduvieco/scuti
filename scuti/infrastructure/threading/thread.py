from abc import ABC, abstractmethod
from threading import Event, Thread as PythonThread

import pyprctl


class Thread(PythonThread, ABC):
    def __init__(self):
        super().__init__()
        self._should_stop = Event()

    @abstractmethod
    def get_name(self):
        pass

    def stop(self):
        self._should_stop.set()
        self.wants_to_stop()

    def should_stop(self) -> bool:
        return self._should_stop.is_set()

    def run(self):
        self.name = self.get_name()
        pyprctl.set_name(self.get_name())
        self.execute()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def wants_to_stop(self):
        pass
