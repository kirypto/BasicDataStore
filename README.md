# Basic Data Store

A sample rest data store using Flask and Sqlite3.

## Prerequesites

- Python3.9 or later installed and on the path.
- Sqlite3 installed and on the path.

## Installation

- Clone this project.
- Navigate to project root and run `pip install .` _(use the `-e` flag if you want changes to automatically
  be applied without needing to re-install)_.
- Using `sqlite3` command line, create a db file with the following tables:

```sqlite
create table main.auth
(
    token text not null,
    name  text not null
);

create table main.items
(
    identifier text not null,
    value      text not null
);
```

- Add an entry to `main.auth` with a randomly generated string `token` and a human friendly `name`. This `token`
  will be used in the `Authorization: Bearer {token}` header for requests made to the app, and the `name` is 
  then logged to identify which auth token was used.
- Create a config file somewhere with the following contents:

```yaml
---
persistence_config:
  item_config:
    class_path: kirypto.basic_data_store.adapter.persistence.Sqlite3ItemPersistence
    class_args:
      database_file: /path/to/the/db/created/above.db
  auth_config:
    class_path: kirypto.basic_data_store.adapter.persistence.Sqlite3AuthPersistence
    class_args:
      database_file: /path/to/the/db/created/above.db

rest_server_config:
  class_path: kirypto.basic_data_store.adapter.rest.FlaskRestServer
  class_args:
    host: "0.0.0.0"
    port: 5000

```

- Then run with `python -m kirypto.basic_data_store /path/to/config/created/above.yaml`