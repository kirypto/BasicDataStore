from importlib import import_module
from typing import TypeVar, Type

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.application.rest import RestServer

_TClass = TypeVar("_TClass")


def construct_item_persistence(*, class_path: str, class_args: dict) -> ItemPersistence:
    return _load_class(class_path, class_args, ItemPersistence)


def construct_rest_server(*, class_path: str, class_args: dict) -> RestServer:
    return _load_class(class_path, class_args, RestServer)


def _load_class(class_path: str, class_args: dict, expected_type: Type[_TClass]) -> _TClass:
    module_name, class_name = class_path.rsplit(".", 1)
    module = import_module(module_name)
    object_class = getattr(module, class_name)

    loaded: _TClass = object_class(**class_args)
    if not isinstance(loaded, expected_type):
        raise ValueError(f"{class_path} did not result in a(n) {expected_type} object.")

    return loaded
