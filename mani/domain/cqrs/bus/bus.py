from abc import abstractmethod


class Bus:
    @abstractmethod
    def subscribe(self, item_type, handler):
        pass

    @abstractmethod
    def handle(self, items):
        pass
