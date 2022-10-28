from typing import Type

from mani.domain.model.identifiable.identifier import Identifier


class AnyId:
    def __init__(self, an_id_type: Type[Identifier] = None):
        self.__an_id_type = Identifier if an_id_type is None else an_id_type

    def __eq__(self, other):
        return isinstance(other, self.__an_id_type)

    def __repr__(self):
        return f"{self.__class__.__name__} <{self.__an_id_type .__name__}>"
