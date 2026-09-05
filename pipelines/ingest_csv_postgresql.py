import argparse
import logging
from hello_data_in_python.database_setup import postgresql as dbs
from hello_data_in_python.database_setup.config import URI_POSTGRESQL
from hello_data_in_python.utils import dbapi_conn
import utils

logger = logging.getLogger(__name__)


def main(csv_path: str, postgres: str, exists: bool) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from ingest_csv_potsgresql.py!")
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        path = dbs.csv_path(csv_path)
        dbs.csv_to_postgresql(conn, path, postgres, exists)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("postgres")
    parser.add_argument("exists", type = utils.str_to_bool)
    args = parser.parse_args()
    main(args.csv_path, args.postgres, args.exists)
