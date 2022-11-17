from datetime import datetime

from mani.domain.time.units import Second
from mani.domain.time.wall_clock import WallClock


class RealWallClock(WallClock):
    def now(self, after: Second = 0) -> datetime:
        return datetime.now()
