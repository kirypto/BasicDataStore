from http import HTTPStatus
from json import dumps
from logging import warning, info
from typing import Any

from kirypto.basic_data_store.application.rest import RestServer, HandlerResult
from kirypto.basic_data_store.application.facades import ItemFacade


def register_item_routes(rest_server: RestServer, item_facade: ItemFacade) -> None:
    @rest_server.register_rest_endpoint("/api/item", "post", json=True)
    def post_item(body: Any) -> HandlerResult:
        item = item_facade.create_item(body)
        info(f"Created new item {item.id}")
        return HTTPStatus.CREATED, dumps(item)

    @rest_server.register_rest_endpoint("/api/items", "get")
    def get_items() -> HandlerResult:
        warning(f"GET /api/items not yet implemented")
        return HTTPStatus.NOT_IMPLEMENTED, "Not Yet Implemented"

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "get")
    def get_item_id(*, item_id: str) -> HandlerResult:
        warning(f"GET /api/item/<item_id> not yet implemented")
        return HTTPStatus.NOT_IMPLEMENTED, "Not Yet Implemented"

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "put", json=True)
    def get_item_id(body: Any, *, item_id: str) -> HandlerResult:
        warning(f"PUT /api/item/<item_id> not yet implemented")
        return HTTPStatus.NOT_IMPLEMENTED, "Not Yet Implemented"
