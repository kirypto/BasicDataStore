from typing import Dict, Any
from uuid import UUID


def _validate_domain_object(domain_object: Any, *, expected_member_types_by_name: Dict[str, type]) -> None:
    for property_name, expected_type in expected_member_types_by_name.items():
        try:
            if not hasattr(domain_object, property_name):
                raise TypeError(f"Missing argument '{property_name}' for {domain_object.__class__}")
            actual = getattr(domain_object, property_name)
            if not isinstance(actual, expected_type):
                raise ValueError(f"Argument '{property_name}' must be {expected_type}, was {type(actual)}")
        except KeyError:
            raise TypeError(f"Missing argument '{property_name}' for {domain_object.__class__}")


class Item(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        _validate_domain_object(self, expected_member_types_by_name=dict(
            id=UUID,
            value=str,
        ))

    @property
    def id(self) -> UUID:
        return UUID(self["id"])

    @property
    def value(self) -> str:
        return self["value"]
