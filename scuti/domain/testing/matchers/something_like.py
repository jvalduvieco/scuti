from typing import Type


class SomethingLike:
    def __init__(self, a_type: Type = None, **kwargs):
        self._a_type = a_type
        self._properties = kwargs

    def __eq__(self, other):
        if self._a_type is not None and not isinstance(other, self._a_type):
            return False
        for a_property, value in self._properties.items():
            try:
                if value != getattr(other, a_property):
                    return False
            except AttributeError:
                return False
        return True

    def __repr__(self):
        return f"{self.__class__.__name__} <{self._a_type.__name__}({', '.join([f'{a_property}={value}' for a_property, value in self._properties.items()])})>"
