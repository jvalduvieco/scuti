import abc


class Effect(abc.ABC):
    pass


class Event(Effect):
    pass


class Command(Effect):
    pass


class Query(Effect):
    pass
