import argparse
import logging
from hello_data_in_python.database_setup import postgresql as dbs
from hello_data_in_python.database_setup.config import URI_POSTGRESQL
from hello_data_in_python.utils import dbapi_conn

logger = logging.getLogger(__name__)


def main() -> None:
    print("Hello from ingest_potsgresql.py!")
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        path = dbs.csv_path("01")
        dbs.csv_to_postgresql(conn, path, "USERS_01", False)       


if __name__ == "__main__":
    main()
