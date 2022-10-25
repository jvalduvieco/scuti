from typing import List, Type, Callable, Dict, Protocol, cast

import plum
from plum import Signature


class PlumWrapper(Protocol):
    methods: Dict


def _resolve_inner_types(plum_type: plum.Type) -> List[Type]:
    result = list(plum_type.get_types())
    result.sort(key=lambda x: str(x))
    return result


def _plum_parameter_types(signature: Signature) -> List[List[Type]]:
    return [_resolve_inner_types(parameter) for parameter in signature.types]


def inspect(a_plum_overloaded_callable: Callable, should_ignore_self: bool = False) -> Dict:
    result = {}
    methods = cast(PlumWrapper, a_plum_overloaded_callable).methods
    for index, (parameters, _return_type) in enumerate(methods.items()):
        types = _plum_parameter_types(parameters)
        result[index] = types[1:] if should_ignore_self else types
    return result
