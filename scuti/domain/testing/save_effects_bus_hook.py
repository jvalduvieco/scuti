from injector import inject

from scuti.domain.cqrs.bus.hooks.bus_hook import BusHook
from scuti.domain.cqrs.effect_store.effect_store import EffectStore
from scuti.domain.cqrs.effects import Effect


class SaveEffectsBusHook(BusHook):
    @inject
    def __init__(self, effect_store: EffectStore):
        self._effect_store = effect_store

    def on_handle(self, effect: Effect):
        self._effect_store.append(effect)
