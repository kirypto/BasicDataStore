import sqlite3
from pathlib import Path

from ruamel.yaml import YAML


def _main(*, database_file: str) -> None:
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    # Need to create table 'tbl1' on the side
    for row in cursor.execute("SELECT * FROM tbl1;"):
        print(row)


if __name__ == "__main__":
    import sys

    config_file = sys.argv[1]
    config: dict = YAML(typ="safe").load(Path(config_file))
    _main(**config)
