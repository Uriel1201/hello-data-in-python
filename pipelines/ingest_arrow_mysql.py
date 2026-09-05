import argparse
import logging
from pathlib import Path

import pyarrow as pa

from hello_data_in_python.database_setup import mysql as dbs
from hello_data_in_python.database_setup.config import URI_MYSQL
from hello_data_in_python.utils import dbapi_conn

logger = logging.getLogger(__name__)


def main(file: str, table_name: str) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from ingest_arrow_mysql.py!")
    path = Path("data/arrow") / file
    if path.exists():
        with (
            dbapi_conn(URI_MYSQL, "mysql") as conn,
            pa.memory_map(str(path), "rb") as source,
            pa.ipc.open_file(source) as reader,
        ):
            dbs.create_table(conn, reader.schema, table_name)
            dbs.arrow_to_mysql(conn, reader, table_name)

    else:
        raise FileNotFoundError(f"Path {path} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("table_name")
    args = parser.parse_args()
    main(args.file, args.table_name)
