from pathlib import Path

from hello_data_in_python.utils import dbapi_conn, dbapi_to_arrow, get_my_table


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
# postgresql_to_arrow:
# params:
# ============================================================
def sqlite_to_arrow(database: str, query: str, output_file: str) -> Path:
    if database == ":memory:":
        with dbapi_conn(database, "sqlite") as conn:
            return dbapi_to_arrow(conn, query, output_file)
    else:
        uri = sqlite_uri(database)
        with dbapi_conn(uri, "sqlite") as conn:
            return dbapi_to_arrow(conn, query, output_file)


def main() -> None:
    print("Hello from sqlite.py!")
    path = sqlite_to_arrow(":memory:", """SELECT 'HELLO, WORLD!'""", "hellow-sqlite")
    table = get_my_table(path)
    print(
        f"Arrow File {path} Open\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
    )


if __name__ == "__main__":
    main()
