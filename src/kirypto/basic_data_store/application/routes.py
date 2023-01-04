from http import HTTPStatus
from json import dumps
from logging import info
from typing import Any
from uuid import UUID

from kirypto.basic_data_store.application.facades import ItemFacade
from kirypto.basic_data_store.application.persistence import AuthPersistence
from kirypto.basic_data_store.application.rest import RestServer, HandlerResult
from kirypto.basic_data_store.domain.objects import Item


def register_item_routes(rest_server: RestServer, item_facade: ItemFacade, auth_persistence: AuthPersistence) -> None:
    @rest_server.register_rest_endpoint("/api/item", "post", json=True, auth_token=True)
    def post_item(body: Any, auth_token: str) -> HandlerResult:
        auth_token_name = auth_persistence.retrieve(auth_token)
        info(f"POST /api/item invoked with token '{auth_token_name}'")
        item = item_facade.create_item(body)
        info(f"Created new item: {item.id}")
        return HTTPStatus.CREATED, dumps(item)

    @rest_server.register_rest_endpoint("/api/items", "get", auth_token=True)
    def get_items(_auth_token: str) -> HandlerResult:
        info(f"GET /api/items invoked")
        ids = item_facade.get_item_ids()
        info(f"Returning {len(ids)} ids")
        return HTTPStatus.OK, dumps([str(id) for id in ids])

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "get", auth_token=True)
    def get_item_id(_auth_token: str, *, item_id: str) -> HandlerResult:
        info(f"GET /api/item/<item_id> invoked with id '{item_id}'")
        item = item_facade.get_item(UUID(item_id))
        info(f"Returning item: {item.id}")
        return HTTPStatus.OK, dumps(item)

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "put", json=True, auth_token=True)
    def get_item_id(body: Any, _auth_token: str, *, item_id: str) -> HandlerResult:
        info(f"PUT /api/item/<item_id> invoked with id '{item_id}'")
        item = Item(id=item_id, value=body)
        item_facade.update_item(item)
        info(f"Updated item: {item.id}")
        return HTTPStatus.OK, dumps(item)

    @rest_server.register_rest_endpoint("/api/item/<item_id>", "delete", auth_token=True)
    def delete_item_id(_auth_token: str, *, item_id: str) -> HandlerResult:
        info(f"DELETE /api/item/<item_id> invoked with id '{item_id}'")
        item_facade.delete(UUID(item_id))
        info(f"Removed item: {item_id}")
        return HTTPStatus.NO_CONTENT, ""
