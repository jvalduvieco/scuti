from datetime import datetime

from scuti.domain.time.units import Second
from scuti.domain.time.wall_clock import WallClock


class RealWallClock(WallClock):
    def now(self, after: Second = 0) -> datetime:
        return datetime.now()
