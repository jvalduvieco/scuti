from dataclasses import fields
from typing import TypeVar, Type

from scuti.domain.cqrs.bus.state_management.dataclass import Dataclass

T = TypeVar("T")


def evolve(what: any, evolved: Type[T], **copy_new_properties) -> T:
    if not isinstance(what, Dataclass):
        raise RuntimeError("Can not evolve non dataclasses")
    copy_properties_name = list(map(lambda p: p.name, fields(evolved)))
    surviving_properties = {k: v for k, v in what.__dict__.items() if k in copy_properties_name}

    return evolved(**dict(surviving_properties, **copy_new_properties))
