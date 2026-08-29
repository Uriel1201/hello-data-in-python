import logging
from pathlib import Path

from adbc_driver_manager import dbapi

logger = logging.getLogger(__name__)

from hello_data_in_python.utils import dbapi_conn, dbapi_to_arrow, print_dbapi


# ============================================================
# sqlite_uri:
# params:
# ============================================================
def sqlite_uri(dbs: str) -> str:
    try:
        path = Path("data/") / dbs
        if not path.exists():
            raise FileNotFoundError(f"Database not found: {path}")
        return f"file:{path}?mode=ro"
    except Exception as e:
        print(f"DATABASE OPERATION FAILED: {e}")
        raise


# ============================================================
# get_conn:
# params:
# ============================================================
def get_conn(dbs) -> dbapi.Connection:
    if dbs != ":memory:":
        dbs = sqlite_uri(dbs)
    logger.info(f"{dbs} connected")
    return dbapi_conn(dbs, "sqlite")


# ============================================================
# sqlite_to_arrow:
# params:
# ============================================================
def sqlite_to_arrow(database: str, query: str, output_file: str) -> Path:
    if database != ":memory:":
        database = sqlite_uri(database)
    with dbapi_conn(database, "sqlite") as conn:
        path = dbapi_to_arrow(conn, query, output_file)
        logger.info(f"Arrow File created -> {path}")
        return path


# ============================================================
# print_sqlite:
# params:
# ============================================================
def print_sqlite(dbs: str, query: str) -> None:
    with get_conn(dbs) as conn:
        logger.info(f"Querying {dbs}")
        print(print_dbapi(conn, query))

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )
    sql = """SELECT 'HELLO, WORLD!'"""
    sqlite_to_arrow(":memory:", sql, "hellow-sqlite")
    print_sqlite(":memory:", sql)


if __name__ == "__main__":
    main()
