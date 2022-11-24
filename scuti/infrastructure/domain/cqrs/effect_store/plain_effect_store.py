import collections
from typing import Optional

from scuti.domain.cqrs.effect_store.effect_store import EffectStore
from scuti.domain.cqrs.effects import Effect


class PlainEffectStore(EffectStore):
    def __init__(self, max_len: Optional[int] = None):
        self.__store = collections.deque(maxlen=max_len)

    def append(self, effect: Effect):
        self.__store.append(effect)

    def __iter__(self):
        yield from self.__store

    def __len__(self):
        return len(self.__store)

    def clear(self):
        self.__store.clear()
