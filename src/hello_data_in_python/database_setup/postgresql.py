from pathlib import Path
import logging

import pyarrow.dataset as ds
import pyarrow as pa
from adbc_driver_manager import dbapi

logger = logging.getLogger(__name__)

from hello_data_in_python.utils import (
    dbapi_conn,
    dbapi_to_arrow,
    print_dbapi,
)

from .config import URI_POSTGRESQL


# ============================================================
# csv_path:
# params:
# ============================================================
def csv_path(dbs: str) -> Path:
    try:
        path = Path("data/csv") / dbs
        if not path.exists():
            path = Path("data") / dbs
        if not path.exists():
            path = Path(dbs)
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
        path = dbapi_to_arrow(conn, query, output_file)
        logger.info(f"Arrow File created -> {path}")
        return path


# ============================================================
# csv_to_postgresql:
# params:
# ============================================================
def csv_to_postgresql(
    conn: dbapi.Connection, path: Path, table_name: str, schema: pa.Schema, exists: bool
) -> None:
    dataset = ds.dataset(path, format="csv", schema = schema)
    logging.info(f"Schema:\n{dataset.schema}")
    reader = dataset.scanner().to_reader()
    try:
        with conn.cursor() as cursor:
            first = not exists
            for batch in reader:
                print(batch.schema)
                cursor.adbc_ingest(
                    table_name, batch, mode="create" if first else "append"
                )
                first = False
            conn.commit()
        logging.info(f"{path} ingested")
    except Exception as e:
        print(f"{e}")
        raise


# ============================================================
# print_postgresql:
# params:
# ============================================================
def print_postgresql(conn: dbapi.Connection, query: str) -> None:
    logger.info("Querying PostgreSQL")
    print(print_dbapi(conn, query))


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )
    print("Hello from postgresql.py!")
    postgresql_to_arrow("""Select 'Hello, World!'""", "hellow-postgresql")

    with (
        dbapi_conn(URI_POSTGRESQL, "postgresql") as conn,
        conn.cursor() as cursor,
    ):
        cursor.execute("""
            drop table if exists "hello"
        """)
        conn.commit()
        path = csv_path("hello")
        csv_to_postgresql(conn, path, "hello", False)
        print_postgresql(
            conn,
            """
            select * from "hello"
        """,
        )


if __name__ == "__main__":
    main()
