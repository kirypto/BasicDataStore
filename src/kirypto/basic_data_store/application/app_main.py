from json import dumps
from logging import warning
from random import choices
from string import ascii_letters
from uuid import uuid4

from kirypto.basic_data_store.application.factories import construct_item_persistence, construct_rest_server
from kirypto.basic_data_store.application.persistence import ItemPersistence
from kirypto.basic_data_store.application.rest import RestServer, HandlerResult
from kirypto.basic_data_store.application.routes import register_item_routes
from kirypto.basic_data_store.domain.objects import Item


class BasicDataStoreApp:
    _item_persistence: ItemPersistence
    _rest_server: RestServer

    def __init__(self, *, database_config: dict, rest_server_config: dict, **kwargs) -> None:
        if kwargs:
            warning(f"Received unwanted keyword arguments: {{{', '.join(kwargs.keys())}}}; ignoring.")

        self._item_persistence = construct_item_persistence(**database_config)
        self._rest_server = construct_rest_server(**rest_server_config)

    def run(self) -> None:
        item = Item(
            id=str(uuid4()),
            value=dumps({random_string(3): random_string(5)})
        )
        print(f"~~> Attempting to save new Item '{item}' to the database. (should fail: not implemented)")
        self._item_persistence.save(item)
        ids = self._item_persistence.retrieve_all()
        print(f"~~> Retrieved {len(ids)} ids: {ids}")
        first_id, *_ = ids
        retrieved_item = self._item_persistence.retrieve(first_id)
        print(f"~~> Retrieved item: {retrieved_item}")
        self._item_persistence.delete(retrieved_item.id)
        post_deletion_count = len(self._item_persistence.retrieve_all())
        print(f"~~> Deleted {retrieved_item.id}, now only {post_deletion_count} remain")

        @self._rest_server.register_rest_endpoint("/", "get", "text/html")
        def main_page_handler() -> HandlerResult:
            return 200, '<div style="background-color: #585454; width: 100%; height: 100%;"><h1>Hello, World!</h1></div>'

        register_item_routes(self._rest_server)

        self._rest_server.listen()


def random_string(count: int) -> str:
    return "".join(choices(ascii_letters, k=count))
