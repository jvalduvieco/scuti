from typing import Callable, Any

from mani.domain.cqrs.effects import Effect
from mani.domain.model.repository.repository import Repository

EffectToStateMapper = Callable[[Effect, Repository], Any]

_singleton_id = 0


def state_fetcher(mapper: EffectToStateMapper):
    def decorator(function):
        function._effect_to_state_mapper = mapper
        return function

    return decorator


All = lambda e, r: r.all()
Singleton = lambda e, r: r.by_id(_singleton_id)
ById = lambda e, r: r.by_id(e.id)
