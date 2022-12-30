import sqlite3
from pathlib import Path
from typing import Set
from uuid import UUID

from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import Item


class Sqlite3ItemPersistence(ItemPersistence):
    _database_file: str
    _item_insert_query: str

    def __init__(self, *, database_file: str) -> None:
        self._database_file = database_file
        sqlite3_queries_dir = Path(__file__).parent.joinpath("sqlite3_queries")
        self._item_insert_query = sqlite3_queries_dir.joinpath("item_insert.sql").read_text()

    def save(self, item: Item) -> None:
        with sqlite3.connect(self._database_file) as connection:
            connection.cursor().execute(self._item_insert_query, item)

    def retrieve_all(self) -> Set[UUID]:
        with sqlite3.connect(self._database_file) as connection:
            results = connection.cursor().execute(f"""
                    SELECT identifier FROM items;
            """).fetchall()
            return {
                UUID(uuid) for uuid, in results
            }

    def retrieve(self, id: UUID) -> Item:
        with sqlite3.connect(self._database_file) as connection:
            results = connection.cursor().execute(f"""
                    SELECT * FROM items
                    WHERE identifier = '{str(id)}';
            """).fetchone()
            identifier, value = results
            return Item(id=identifier, value=value)

    def delete(self, id: UUID) -> None:
        with sqlite3.connect(self._database_file) as connection:
            connection.cursor().execute(f"""
                    DELETE FROM items
                    WHERE identifier = '{str(id)}';
            """)
