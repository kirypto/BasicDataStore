from logging import warning
from uuid import uuid4

from kirypto.basic_data_store.application.factories import construct_item_persistence
from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.domain.objects import Item


class BasicDataStoreApp:
    _item_persistence: ItemPersistence

    def __init__(self, *, database_config: dict, **kwargs) -> None:
        if kwargs:
            warning(f"Received unwanted keyword arguments: {{{', '.join(kwargs.keys())}}}; ignoring.")

        self._item_persistence = construct_item_persistence(**database_config)

    def run(self) -> None:
        item = Item(id=str(uuid4()), value="Value")
        print(f"Attempting to save Item '{item}' to the database. (should fail: not implemented)")
        self._item_persistence.save(item)
        try:
            ids = self._item_persistence.retrieve_all()
            print(f"~~> Retrieved ids: {ids}")
        except NotImplementedError as e:
            print(f"~~> Got expected NIE: {e}")
