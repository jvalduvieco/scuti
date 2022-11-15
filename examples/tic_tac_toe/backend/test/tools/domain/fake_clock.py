from datetime import datetime

from domain.clock import Clock


class FakeClock(Clock):
    def __init__(self, now: datetime):
        self.__now = now

    def now(self):
        return self.__now
