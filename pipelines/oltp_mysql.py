import argparse
import logging

from hello_data_in_python.database_setup.mysql import print_mysql
from hello_data_in_python.database_setup.config import URI_MYSQL
from hello_data_in_python.utils import (
    dbapi_conn,
    get_query,
)

logger = logging.getLogger(__name__)


def main(sql_file: str) -> None:
    print("Hello from oltp_mysql.py!")
    logging.basicConfig(level=logging.INFO)
    with dbapi_conn(URI_MYSQL, "mysql") as conn:
        sql = get_query(f"oltp/{sql_file}")
        print_mysql(conn, sql)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sql_file")
    args = parser.parse_args()
    main(args.sql_file)
