from abc import ABC, abstractmethod
from typing import Callable, Tuple

StatusCode = int
HandlerResult = Tuple[StatusCode, str]
RequestHandler = Callable[[...], HandlerResult]
HandlerRegisterer = Callable[[RequestHandler], None]


class RestServer(ABC):
    @abstractmethod
    def register_rest_endpoint(
            self, route: str, method: str, response_type: str = "application/json",
            *, json: bool = False, query_params: bool = False
    ) -> HandlerRegisterer:
        pass

    @abstractmethod
    def listen(self) -> None:
        pass
