from abc import abstractmethod, ABC


class ScheduledEventsStore(ABC):
    @abstractmethod
    def schedule(self, after, event, key):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def expired(self, now):
        pass

    @abstractmethod
    def remove(self, key):
        pass
