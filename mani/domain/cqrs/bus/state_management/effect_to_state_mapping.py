from typing import Callable, Any

from mani.domain.cqrs.effects import Effect
from mani.domain.model.repository.repository import Repository

EffectToStateMapper = Callable[[Effect, Repository], Any]

effect_to_state_mapper_property = "_effect_to_state_mapper"


def state_fetcher(mapper: EffectToStateMapper):
    def decorator(function):
        setattr(function, effect_to_state_mapper_property, mapper)
        return function

    return decorator


All = lambda e, r: r.all()
Singleton = lambda e, s: s.get()
ById = lambda e, r: r.by_id(e.id)
