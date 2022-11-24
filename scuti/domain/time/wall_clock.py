from abc import abstractmethod, ABC
from datetime import datetime

from scuti.domain.time.units import Second


class WallClock(ABC):
    @abstractmethod
    def now(self, after: Second = 0) -> datetime:
        pass
