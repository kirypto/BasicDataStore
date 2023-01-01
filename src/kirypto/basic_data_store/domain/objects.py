from typing import Dict, Any, Union, Set
from uuid import UUID


def _validate_domain_object(domain_object: Any, *, expected_member_types_by_name: Dict[str, Set[type]]) -> None:
    for property_name, expected_types in expected_member_types_by_name.items():
        try:
            if not hasattr(domain_object, property_name):
                raise TypeError(f"Missing argument '{property_name}' for {domain_object.__class__}")
            actual = getattr(domain_object, property_name)
            if not any({isinstance(actual, expected_type) for expected_type in expected_types}):
                raise ValueError(f"Argument '{property_name}' must be one of {expected_types}, was {type(actual)}")
        except KeyError:
            raise TypeError(f"Missing argument '{property_name}' for {domain_object.__class__}")


JSONObject = Union[str, int, float, list, dict]


class Item(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        _validate_domain_object(self, expected_member_types_by_name=dict(
            id={UUID},
            value={str, int, float, list, dict},
        ))

    @property
    def id(self) -> UUID:
        return UUID(self["id"])

    @property
    def value(self) -> JSONObject:
        return self["value"]
