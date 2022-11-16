import datetime

from mani.domain.time.wall_clock import WallClock
from mani.domain.time.units import Second


class FakeWallClock(WallClock):
    def __init__(self, now: datetime):
        self.__now = now

    def now(self, after: Second = 0) -> datetime:
        return self.__now + datetime.timedelta(seconds=after)
