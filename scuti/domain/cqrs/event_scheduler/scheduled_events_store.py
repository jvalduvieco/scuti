from abc import ABC, abstractmethod


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

    @abstractmethod
    def wait_for_next_expiration(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass
