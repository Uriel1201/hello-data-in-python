import argparse
import logging
import pyarrow as pa
from hello_data_in_python.database_setup import postgresql as dbs
from hello_data_in_python.database_setup.config import URI_POSTGRESQL
from hello_data_in_python.utils import dbapi_conn

logger = logging.getLogger(__name__)


def str_to_bool(value):
    value = value.lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no"):
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def main(csv_path: str, exists: bool) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from ingest_potsgresql.py!")
    schema = pa.schema([
        pa.field("USER_ID", pa.int64()),
        pa.field("ACTION", pa.string()),
        pa.field("DATES", pa.timestamp("s", tz="UTC")),
    ])
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        path = dbs.csv_path(csv_path)
        dbs.csv_to_postgresql(conn, path, "USERS_01", schema, exists)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("exists", type = str_to_bool)
    args = parser.parse_args()
    main(args.csv_path, args.exists)
