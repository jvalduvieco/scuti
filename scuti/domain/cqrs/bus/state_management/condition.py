from typing import Callable

from scuti.domain.cqrs.effects import Effect

HandlerCondition = Callable[[Effect], bool]
condition_property = "_condition"


def condition(a_condition: Callable[[Effect], bool]):
    def decorator(function):
        setattr(function, condition_property, a_condition)
        return function

    return decorator
