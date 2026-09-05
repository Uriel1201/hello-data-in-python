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


def main(sql_file: str, output_file: str) -> None:
    print("hello from extract_oracledb.py")
    logging.basicConfig(level=logging.INFO)
    with dbs.get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        sql = get_query(f"oltp/{sql_file}")
        dbs.oracledb_to_arrow(conn, sql, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sql_file")
    parser.add_argument("output_file")
    args = parser.parse_args()
    main(args.sql_file, args.output_file)
