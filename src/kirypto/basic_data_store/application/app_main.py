from json import dumps, loads
from logging import warning

from kirypto.basic_data_store.domain.objects import Item


class BasicDataStoreApp:
    def __init__(self, *, database_config: dict, **kwargs) -> None:
        if kwargs:
            warning(f"Received unwanted keyword arguments: {{{', '.join(kwargs.keys())}}}; ignoring.")

        print(database_config)
        print(f"Constructing valid {Item.__name__}...")
        item = Item(id="abad1dea-0000-0000-0000-000000000000", value="Value")
        print(f"Done: {item}")
        print(f"Constructing INVALID {Item.__name__}...")
        try:
            invalid = Item(id="abad1dea-0000-0000-0000-000000000000")
            print(f"SHOULD NOT SEE THIS! Somehow constructed: {invalid}")
        except TypeError as e:
            print(f"Failed as expected. Error: {e}")
        print("As JSON:")
        item_as_json = dumps(item)
        print(item_as_json)
        print("From JSON:")
        print(loads(item_as_json))
        print("From JSON (as Item):")
        print(Item(loads(item_as_json)))


    def run(self) -> None:
        pass
