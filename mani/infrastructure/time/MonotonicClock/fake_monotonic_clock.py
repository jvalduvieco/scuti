from mani.domain.time.monotonic_clock import MonotonicClock
from mani.domain.time.units import Millisecond


class FakeMonotonicClock(MonotonicClock):
    def __init__(self, current_time: Millisecond = 0):
        self.__current: Millisecond = current_time

    def now(self, after: Millisecond = 0) -> Millisecond:
        return Millisecond(self.__current + after)
