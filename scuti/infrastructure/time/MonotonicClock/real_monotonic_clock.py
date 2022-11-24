import time

from scuti.domain.time.monotonic_clock import MonotonicClock
from scuti.domain.time.units import Millisecond


class RealMonotonicClock(MonotonicClock):
    def now(self, after: Millisecond = 0) -> Millisecond:
        return Millisecond(int(time.monotonic() * 1000) + after)
