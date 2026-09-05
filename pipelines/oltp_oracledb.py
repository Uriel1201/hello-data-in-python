import argparse
import logging

from hello_data_in_python.database_setup import oracle as dbs
from hello_data_in_python.database_setup.config import (
    ODB_DSN,
    ODB_PASSWORD,
    ODB_USER,
)
from hello_data_in_python.utils import get_query

logger = logging.getLogger(__name__)


def main(sql_file: str) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from oltp_oracle.py!")
    with dbs.get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        sql = get_query(f"oltp/{sql_file}")
        dbs.print_oracle(conn, sql)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sql_file")
    args = parser.parse_args()
    main(args.sql_file)
