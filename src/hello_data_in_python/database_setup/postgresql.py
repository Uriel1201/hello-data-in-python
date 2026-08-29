from pathlib import Path

import pyarrow.dataset as ds
from adbc_driver_manager import dbapi

from hello_data_in_python.utils import dbapi_conn, dbapi_to_arrow, get_my_table

from .config import URI_POSTGRESQL


# ============================================================
# csv_path:
# params:
# ============================================================
def csv_path(dbs: str) -> str:
    try:
        path = Path("data/csv/") / dbs
        if not path.exists():
            path = Path("data/csv")
        if not path.exists():
            raise FileNotFoundError(f"folder not found: {path}")
        return path
    except Exception as e:
        print(f"OPERATION FAILED: {e}")
        raise


# ============================================================
# postgresql_to_arrow:
# params:
# ============================================================
def postgresql_to_arrow(query: str, output_file: str) -> Path:
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        return dbapi_to_arrow(conn, query, output_file)


# ============================================================
# csv_to_postgresql:
# params:
# ============================================================
def csv_to_postgresql(
    conn: dbapi.Connection, path: str, table_name: str, exists: bool
) -> None:
    dataset = ds.dataset(path, format="csv")
    reader = dataset.scanner().to_reader()
    try:
        with conn.cursor() as cursor:
            first = not exists
            for batch in reader:
                cursor.adbc_ingest(
                    table_name, batch, mode="create" if first else "append"
                )
                first = False
            conn.commit()
    except Exception as e:
        print(f"{e}")
        raise


def main() -> None:
    print("Hello from postgresql.py!")
    path = postgresql_to_arrow("""Select 'Hello, World!'""", "hellow-postgresql")
    table = get_my_table(path)
    print(
        f"Arrow File {path} Open\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
    )
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                drop table if exists "hello"
            """)
            conn.commit()
        path = csv_path("hello")
        csv_to_postgresql(conn, path, "hello", False)
        result = conn.execute("""
            select * from "hello"
        """)
        print(f"{path} successfully loaded in your database")


if __name__ == "__main__":
    main()
