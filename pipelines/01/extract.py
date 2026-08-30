from hello_data_in_python import database_setup as dbs
from hello_data_in_python.database_setup.config import (
    ODB_DSN,
    ODB_PASSWORD,
    ODB_USER,
)
from hello_data_in_python.utils import get_query


def main() -> None:
    with dbs.oracle.get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        sql = get_query("SQL/OLTP/01_oracledb.sql")
        dbs.oracle.oracledb_to_arrow(conn, sql, "01_oracle")


if __name__ == "__main__":
    main()
