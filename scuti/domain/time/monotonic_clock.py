from abc import ABC, abstractmethod

from scuti.domain.time.units import Millisecond


class MonotonicClock(ABC):
    @abstractmethod
    def now(self, after: Millisecond = 0) -> Millisecond:
        pass
