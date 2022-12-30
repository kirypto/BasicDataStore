import sqlite3
from typing import Set
from uuid import UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import Item


class Sqlite3ItemPersistence(ItemPersistence):
    _database_file: str

    def __init__(self, *, database_file: str) -> None:
        self._database_file = database_file

    def save(self, item: Item) -> None:
        with sqlite3.connect(self._database_file) as connection:
            connection.cursor().execute(f"""
                    INSERT INTO items (identifier, value)
                    VALUES ('{item.id}', '{item.value}');
            """)

    def retrieve_all(self) -> Set[UUID]:
        with sqlite3.connect(self._database_file) as connection:
            results = connection.cursor().execute(f"""
                    SELECT identifier FROM items;
            """)
            return {
                UUID(uuid) for uuid, in results
            }

    def retrieve(self, id: UUID) -> Item:
        raise NotImplementedError(f"{ItemPersistence.__name__}.retrieve has not been implemented")

    def delete(self, id: UUID) -> None:
        raise NotImplementedError(f"{ItemPersistence.__name__}.delete has not been implemented")
