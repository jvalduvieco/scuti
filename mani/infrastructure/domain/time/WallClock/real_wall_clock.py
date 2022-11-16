from datetime import datetime

from mani.domain.time.wall_clock import WallClock
from mani.domain.time.units import Second


class RealWallClock(WallClock):
    def now(self, after: Second = 0) -> datetime:
        return datetime.now()
