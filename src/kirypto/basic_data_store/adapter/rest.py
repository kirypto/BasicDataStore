from flask import Flask
from waitress import serve

from kirypto.basic_data_store.application.rest import RestServer, HandlerRegisterer


class FlaskRestServer(RestServer):
    def __init__(self) -> None:
        pass

    def register_rest_endpoint(
            self, route: str, method: str, response_type: str = "application/json",
            *, json: bool = False, query_params: bool = False
    ) -> HandlerRegisterer:
        pass

    def listen(self) -> None:
        print("######################  FLASK  ######################")
        flask_web_app = Flask(__name__)

        @flask_web_app.route("/")
        def main_page_handler():
            return '<div style="background-color: #585454; width: 100%; height: 100%;"><h1>Hello, World!</h1></div>'
        serve(flask_web_app, **{"host": "0.0.0.0", "port": 5000})
