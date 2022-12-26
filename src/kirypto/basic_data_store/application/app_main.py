from logging import warning

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
        item = Item(id="abad1dea-0000-0000-0000-000000000000", value="Value")
        print(f"Attempting to save Item '{item}' to the database. (should fail: not implemented)")
        try:
            self._item_persistence.save(item)
        except NotImplementedError as e:
            print(f"~~> Got expected NIE: {e}")
