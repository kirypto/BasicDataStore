from typing import Set
from uuid import UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import Item


class Sqlite3ItemPersistence(ItemPersistence):
    _database_file: str

    def __init__(self, *, database_file: str) -> None:
        self._database_file = database_file

    def save(self, item: Item) -> None:
        raise NotImplementedError(f"{ItemPersistence.__name__}.save has not been implemented")

    def retrieve_all(self) -> Set[UUID]:
        raise NotImplementedError(f"{ItemPersistence.__name__}.save has not been implemented")

    def retrieve(self, id: UUID) -> Item:
        raise NotImplementedError(f"{ItemPersistence.__name__}.retrieve has not been implemented")

    def delete(self, id: UUID) -> None:
        raise NotImplementedError(f"{ItemPersistence.__name__}.delete has not been implemented")
