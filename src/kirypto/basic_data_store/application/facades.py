from typing import Set
from uuid import uuid4, UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import JSONObject, Item


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
