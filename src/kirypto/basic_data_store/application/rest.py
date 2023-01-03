from abc import ABC, abstractmethod
from http import HTTPStatus
from json import dumps
from logging import exception
from typing import Callable, Tuple, Union

from kirypto.basic_data_store.domain.exceptions import AuthError

StatusCode = int
RestMethod = str
HandlerResult = Tuple[StatusCode, str]
RequestHandler = Callable[[...], HandlerResult]
HandlerRegisterer = Callable[[RequestHandler], None]


class RestServer(ABC):
    @abstractmethod
    def register_rest_endpoint(
            self, route: str, method: RestMethod, response_type: str = "application/json",
            *, json: bool = False, query_params: bool = False, auth_token: bool = False,
    ) -> HandlerRegisterer:
        pass

    @abstractmethod
    def listen(self) -> None:
        pass


def error_response(message: Union[str, BaseException], status_code: int) -> HandlerResult:
    return status_code, dumps({"error": str(message)})


def with_error_response_on_raised_exceptions(handler_function: RequestHandler) -> RequestHandler:
    def inner(*args, **kwargs) -> HandlerResult:
        try:
            return handler_function(*args, **kwargs)
        except NameError as e:
            exception(e, exc_info=e)
            return error_response(e, HTTPStatus.NOT_FOUND)
        except KeyError as e:
            exception(e, exc_info=e)
            return error_response(f"Missing key {e}", HTTPStatus.BAD_REQUEST)
        # except (JsonPatchTestFailed, JsonPatchConflict) as e:
        #     exception(e, exc_info=e)
        #     return error_response(e, HTTPStatus.PRECONDITION_FAILED)
        except NotImplementedError as e:
            exception(e, exc_info=e)
            return error_response(e, HTTPStatus.NOT_IMPLEMENTED)
        except AuthError as e:
            exception(e, exc_info=e)
            return error_response(e, HTTPStatus.FORBIDDEN)
        except BaseException as e:
            exception(e, exc_info=e)
            return error_response(e, HTTPStatus.INTERNAL_SERVER_ERROR)

    return inner
