from abc import ABC, abstractmethod

from mani.domain.time.units import Millisecond


class MonotonicClock(ABC):
    @abstractmethod
    def now(self, after: Millisecond = 0) -> Millisecond:
        pass
