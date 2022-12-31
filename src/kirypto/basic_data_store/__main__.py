from logging import basicConfig, INFO
from pathlib import Path
from typing import Dict, Any
from argparse import ArgumentParser

from ruamel.yaml import YAML

from kirypto.basic_data_store.application.app_main import BasicDataStoreApp


def _main() -> None:
    basicConfig(level=INFO)
    kwargs = _parse_args()
    app_args = kwargs.pop("config")
    try:
        app = BasicDataStoreApp(**app_args)
    except TypeError as e:
        raise TypeError(f"Failed to construct app, invalid configuration: {e}")
    app.run()


def _parse_args() -> Dict[str, Any]:
    parser = ArgumentParser(description="Basic Data Store Application")
    parser.add_argument("config", type=yaml_config, help="Config for the application.")
    args = parser.parse_args()
    return {
        key: val
        for key, val in vars(args).items()
        if val is not None
    }


def yaml_config(config_file: str) -> dict:
    config: dict = YAML(typ="safe").load(Path(config_file))
    return config


if __name__ == "__main__":
    _main()
