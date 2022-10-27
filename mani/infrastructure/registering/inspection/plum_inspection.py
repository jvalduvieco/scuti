from dataclasses import field, dataclass
from typing import List, Type, Callable, Dict, Protocol, cast, Any, Optional

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


@dataclass(frozen=True)
class InspectionResult:
    parameter_types: List[List[Type]]
    annotations: Optional[Dict[str, Any]] = field(default_factory=dict)


def inspect(a_plum_overloaded_callable: Callable, should_ignore_self: bool = False,
            annotations_to_retrieve: List[str] = None) -> Dict[int, InspectionResult]:
    result = {}
    annotations_to_retrieve = annotations_to_retrieve or []
    methods = cast(PlumWrapper, a_plum_overloaded_callable).methods
    for index, (parameters, (function, _return_type)) in enumerate(methods.items()):
        types = _plum_parameter_types(parameters)
        annotations = {annotation: getattr(function, annotation, None)
                       for annotation in annotations_to_retrieve if getattr(function, annotation, None) is not None}
        result[index] = InspectionResult(parameter_types=types[1:] if should_ignore_self else types,
                                         annotations=annotations)
    return result
