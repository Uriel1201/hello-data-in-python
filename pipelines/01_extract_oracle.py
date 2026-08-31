import argparse
from hello_data_in_python.database_setup import oracle as dbs
from hello_data_in_python.database_setup.config import (
    ODB_DSN,
    ODB_PASSWORD,
    ODB_USER,
)
from hello_data_in_python.utils import get_query


def main(sql_file: str) -> None:
    with dbs.get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        sql = get_query(f"oltp/{sql_file}")
        dbs.oracledb_to_arrow(conn, sql, "01_oracle")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sql_file")
    args = parser.parse_args()
    main(args.sql_file)
