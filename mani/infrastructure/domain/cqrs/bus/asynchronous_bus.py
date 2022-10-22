from abc import ABC, abstractmethod

from mani.domain.cqrs.bus.bus import Bus


class AsynchronousBus(ABC, Bus):
    @abstractmethod
    def drain(self, should_block):
        pass

    @abstractmethod
    def handles(self, item_type):
        pass

    @abstractmethod
    def is_empty(self):
        pass
