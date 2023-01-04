from functools import wraps
from typing import Set, Callable
from uuid import uuid4, UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence, AuthPersistence
from kirypto.basic_data_store.domain.objects import JSONObject, Item, AuthTokenName


class ItemFacade:
    _item_persistence: ItemPersistence

    def __init__(self, item_persistence: ItemPersistence) -> None:
        self._item_persistence = item_persistence

    def create_item(self, value: JSONObject) -> Item:
        item = Item(id=(str(uuid4())), value=value)
        self._item_persistence.create(item)
        return item

    def get_item_ids(self) -> Set[UUID]:
        return self._item_persistence.retrieve_all()

    def get_item(self, id: UUID) -> Item:
        return self._item_persistence.retrieve(id)

    def update_item(self, item: Item) -> None:
        self._item_persistence.update(item)

    def delete(self, id: UUID) -> None:
        self._item_persistence.delete(id)


class AuthFacade:
    _auth_persistence: AuthPersistence

    def __init__(self, auth_persistence: AuthPersistence) -> None:
        self._auth_persistence = auth_persistence

    def translate_auth_param(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            *other_args, auth_token = args
            auth_token_name: AuthTokenName = self._auth_persistence.retrieve(auth_token)
            return function(*other_args, auth_token_name, **kwargs)

        return wrapper
