from abc import ABCMeta, abstractmethod


class Clock(metaclass=ABCMeta):
    @abstractmethod
    def now(self):
        pass
