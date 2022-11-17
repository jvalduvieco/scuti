from abc import ABC


class Effect(ABC):
    pass


class Event(Effect):
    pass


class Command(Effect):
    pass


class Query(Effect):
    pass


class FrameworkCommand(Effect):
    pass
