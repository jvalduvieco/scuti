from typing import Type, TypeVar

from scuti.domain.model.identifiable.identifier import Identifier

T = TypeVar("T", bound=Identifier)


def _matches_same_type(self, other):
    return isinstance(other, self.__class__)


def _repr_same_type(self):
    return f"<matches any {self.__class__.__name__}>"


def _matches_descendants_of_identifier(self, other):
    return issubclass(other.__class__, Identifier)


def _repr_descendants_of_identifier(self):
    return "<matches any descendant of Identifier>"


def match_any_id(a_type: Type[T] = Identifier) -> T:
    class AnIdentifierToMatchAnything(Identifier):
        def serialize(self):
            return "An identifier to match anything"

    a_type = a_type if a_type != Identifier else AnIdentifierToMatchAnything
    a_type.__eq__ = _matches_descendants_of_identifier if a_type == AnIdentifierToMatchAnything else _matches_same_type
    a_type.__repr__ = _repr_descendants_of_identifier if a_type == AnIdentifierToMatchAnything else _repr_same_type
    a_type.__str__ = a_type.__repr__
    a_type.serialize = lambda self: ""
    result = a_type()
    return result
