from datetime import datetime

from domain.clock import Clock


class RealClock(Clock):
    def now(self):
        return datetime.now()
