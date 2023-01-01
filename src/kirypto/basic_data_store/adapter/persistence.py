import sqlite3
from json import dumps, loads
from pathlib import Path
from typing import Set
from uuid import UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import Item


class Sqlite3ItemPersistence(ItemPersistence):
    _database_file: str
    _item_insert_query: str
    _item_retrieve_all_query: str
    _item_retrieve_query: str
    _item_delete_query: str

    def __init__(self, *, database_file: str) -> None:
        self._database_file = database_file
        sqlite3_queries_dir = Path(__file__).parent.joinpath("sqlite3_queries")
        self._item_insert_query = sqlite3_queries_dir.joinpath("item_insert.sql").read_text()
        self._item_retrieve_all_query = sqlite3_queries_dir.joinpath("item_retrieve_all.sql").read_text()
        self._item_retrieve_query = sqlite3_queries_dir.joinpath("item_retrieve.sql").read_text()
        self._item_delete_query = sqlite3_queries_dir.joinpath("item_delete.sql").read_text()

    def save(self, item: Item) -> None:
        item_to_save = {
            **item,
            "value": dumps(item["value"])
        }
        with sqlite3.connect(self._database_file) as connection:
            connection.cursor().execute(self._item_insert_query, item_to_save)

    def retrieve_all(self) -> Set[UUID]:
        with sqlite3.connect(self._database_file) as connection:
            return {
                UUID(uuid)
                for uuid, in connection.cursor().execute(self._item_retrieve_all_query).fetchall()
            }

    def retrieve(self, id: UUID) -> Item:
        with sqlite3.connect(self._database_file) as connection:
            identifier, value = connection.cursor().execute(self._item_retrieve_query, {"id": str(id)}).fetchone()
            return Item(id=identifier, value=loads(value))

    def delete(self, id: UUID) -> None:
        with sqlite3.connect(self._database_file) as connection:
            connection.cursor().execute(self._item_delete_query, {"id": str(id)})
