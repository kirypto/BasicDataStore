from collections import defaultdict
from functools import wraps
from logging import info
from typing import Dict, Callable

from flask import Flask, Response, make_response, request
from waitress import serve

from kirypto.basic_data_store.application.rest import RestServer, HandlerRegisterer, RestMethod, RequestHandler, HandlerResult, with_error_response_on_raised_exceptions


class FlaskRestServer(RestServer):
    _is_listening: bool
    _routes: Dict[str, Dict[RestMethod, Callable]]
    _host: str
    _port: int

    def __init__(self, *, host: str, port: int) -> None:
        self._is_listening = False
        self._routes = defaultdict(dict)
        self._host = host
        self._port = port

    def register_rest_endpoint(
            self, route: str, method: str, response_type: str = "application/json",
            *, json: bool = False, query_params: bool = False
    ) -> HandlerRegisterer:
        if self._is_listening:
            raise ValueError("Cannot register, controller has already been finalized.")
        method = method.upper()
        if method in self._routes[route]:
            raise ValueError(f"Cannot register, method {method} already registered for {route}")

        def handler_registerer(handler_func: RequestHandler) -> None:
            def convert_to_flask_response(func: RequestHandler) -> Callable[[...], Response]:
                @wraps(func)
                def wrapper(*args, **kwargs) -> Response:
                    response: HandlerResult = func(*args, **kwargs)
                    status_code, contents = response
                    flask_response = make_response(contents, status_code)
                    flask_response.mimetype = response_type
                    return flask_response
                return wrapper

            @convert_to_flask_response
            @with_error_response_on_raised_exceptions
            @wraps(handler_func)
            def handler_wrapper(**kwargs) -> HandlerResult:
                args = []
                if json:
                    if request.get_json(silent=True) is None:
                        raise ValueError("A JSON body must be provided and the Content-Type header must be 'application/json'")
                    args.append(request.json)
                if query_params:
                    args.append(dict(request.args))

                return handler_func(*args, **kwargs)

            self._routes[route][method] = handler_wrapper
        return handler_registerer

    def listen(self) -> None:
        if self._is_listening:
            raise ValueError("Rest server is already listening.")

        self._is_listening = True
        print("######################  FLASK  ######################")
        flask_web_app = Flask(__name__)

        for route, method_handler_dict in self._routes.items():
            def route_handler(*args, **kwargs):
                request_url = request.url_rule.rule
                rest_method = request.method.upper()
                return self._routes[request_url][rest_method](*args, **kwargs)

            flask_web_app.add_url_rule(route, route, route_handler, methods=[method for method in method_handler_dict.keys()])

        # noinspection HttpUrlsUsage
        url = f"http://{self._host}:{self._port}" if self._host != "0.0.0.0" else f"http://localhost:{self._port}"
        info(f"Serving on {url}")
        serve(flask_web_app, host=self._host, port=self._port)
