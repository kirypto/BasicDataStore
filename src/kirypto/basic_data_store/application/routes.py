from http import HTTPStatus
from json import dumps
from logging import info
from typing import Any
from uuid import UUID

from kirypto.basic_data_store.application.facades import ItemFacade
from kirypto.basic_data_store.application.rest import RestServer, HandlerResult
from kirypto.basic_data_store.domain.objects import Item


def register_item_routes(rest_server: RestServer, item_facade: ItemFacade) -> None:
    @rest_server.register_rest_endpoint("/api/item", "post", json=True)
    def post_item(body: Any) -> HandlerResult:
        item = item_facade.create_item(body)
        info(f"POST /api/item invoked; created new item: {item.id}")
        return HTTPStatus.CREATED, dumps(item)

    @rest_server.register_rest_endpoint("/api/items", "get")
    def get_items() -> HandlerResult:
        ids = item_facade.get_item_ids()
        info(f"GET /api/items invoked; returning {len(ids)} ids")
        return HTTPStatus.OK, dumps([str(id) for id in ids])

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "get")
    def get_item_id(*, item_id: str) -> HandlerResult:
        item = item_facade.get_item(UUID(item_id))
        info(f"GET /api/item/<item_id> invoked; returning item: {item.id}")
        return HTTPStatus.OK, dumps(item)

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "put", json=True)
    def get_item_id(body: Any, *, item_id: str) -> HandlerResult:
        item = Item(id=item_id, value=body)
        item_facade.update_item(item)
        info(f"PUT /api/item/<item_id> invoked; updated item: {item.id}")
        return HTTPStatus.OK, dumps(item)
