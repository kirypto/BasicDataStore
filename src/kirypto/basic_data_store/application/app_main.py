from logging import warning
from random import choices
from string import ascii_letters

from kirypto.basic_data_store.application.facades import ItemFacade
from kirypto.basic_data_store.application.factories import construct_rest_server, construct_persistence
from kirypto.basic_data_store.application.persistence import ItemPersistence, AuthPersistence
from kirypto.basic_data_store.application.rest import RestServer, HandlerResult
from kirypto.basic_data_store.application.routes import register_item_routes


class BasicDataStoreApp:
    _item_persistence: ItemPersistence
    _auth_persistence: AuthPersistence
    _rest_server: RestServer
    _item_facade: ItemFacade

    def __init__(self, *, persistence_config: dict, rest_server_config: dict, **kwargs) -> None:
        if kwargs:
            warning(f"Received unwanted keyword arguments: {{{', '.join(kwargs.keys())}}}; ignoring.")

        self._item_persistence, self._auth_persistence = construct_persistence(**persistence_config)
        self._rest_server = construct_rest_server(**rest_server_config)

        self._item_facade = ItemFacade(self._item_persistence)

    def run(self) -> None:
        @self._rest_server.register_rest_endpoint("/", "get", "text/html")
        def main_page_handler() -> HandlerResult:
            return 200, """
            <body style="background-color: #242424">
                <div style="width: 100%; height: 100%; background-color: #424242; color: #d2d2d2">
                    <h1>Hello, Basic Data Store!</h1>
                    <h3>Available Routes:</h3>
                    <ul>
                        <li><pre>POST /api/item</pre> Creates a new item with a value equal to the request body.</li>
                        <li><pre>GET /api/items</pre> Returns the ids of all stored items.</li>
                        <li><pre>GET /api/item/{item_id}</pre> Returns the requested item.</li>
                        <li><pre>PUT /api/item/{item_id}</pre> Replaces the stored item's value with the provided request body.</li>
                        <li><pre>DELETE /api/item/{item_id}</pre> Removes the specified item.</li>
                    </ul>
                </div>
            </body>
            """

        register_item_routes(self._rest_server, self._item_facade, self._auth_persistence)

        self._rest_server.listen()


def random_string(count: int) -> str:
    return "".join(choices(ascii_letters, k=count))
