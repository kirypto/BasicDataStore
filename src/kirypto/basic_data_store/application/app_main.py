from logging import warning


class BasicDataStoreApp:
    def __init__(self, *, database_config: dict, **kwargs) -> None:
        if kwargs:
            warning(f"Received unwanted keyword arguments: {{{', '.join(kwargs.keys())}}}; ignoring.")

        print(database_config)

    def run(self) -> None:
        pass
