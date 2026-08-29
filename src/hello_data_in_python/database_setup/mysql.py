from pathlib import Path
import logging 

import pyarrow as pa
from adbc_driver_manager import dbapi

logger = logging.getLogger(__name__)

from hello_data_in_python.utils import (
    dbapi_conn,
    dbapi_to_arrow,
    print_dbapi,
)

from .config import URI_MYSQL


# ============================================================
# get_schema:
# params:
# ============================================================
def get_schema(arrow_schema: pa.lib.Schema, table_name: str) -> str:
    sql_fields = []
    for field in arrow_schema:
        var_type = field.metadata[b"sql.database_type_name"].decode("utf-8")
        if var_type == "VARCHAR":
            sql_fields.append(f"`{field.name}` {var_type}(15)")
    return (
        f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
        + "`EVENT_ID` BIGINT NOT NULL PRIMARY KEY,\n"
        + ",\n".join(sql_fields)
        + "\n)ENGINE=InnoDB"
    )


# ============================================================
# create_table:
# params:
# ============================================================
def create_table(
    conn: dbapi.Connection, arrow_schema: pa.lib.Schema, table_name: str
) -> None:
    schema = get_schema(arrow_schema, table_name)
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(schema)
        conn.commit()
    logger.info(f"MySQL table created -> {table_name}")


# ============================================================
# mysql_to_arrow:
# params:
# ============================================================
def mysql_to_arrow(query: str, output_file: str) -> Path:
    with dbapi_conn(URI_MYSQL, "mysql") as conn:
        path = dbapi_to_arrow(conn, query, output_file)
        logger.info(f"Arrow File created -> {path}")
        return path


# ============================================================
# arrow_to_mysql:
# params:
# ============================================================
def arrow_to_mysql(
    conn: dbapi.Connection, reader: pa.ipc.RecordBatchFileReader, table_name: str
) -> None:

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                    SELECT 
                        COALESCE (MAX(EVENT_ID),0)
                    FROM
                        `{table_name}`
                    """)
            last_event = cursor.fetchone()[0]
            num_of = reader.num_record_batches
            for i in range(num_of):
                batch = reader.get_batch(i)
                ids = pa.array(
                    range(last_event + 1, last_event + 1 + batch.num_rows),
                    type=pa.int64(),
                )
                last_event += batch.num_rows
                batch = batch.add_column(0, "EVENT_ID", ids)
                cursor.adbc_ingest(table_name, batch, mode="append")
                conn.commit()
        logger.info(f"{num_of} RecordBatches ingested into {table_name}")
    except Exception as e:
        print(f"{e}")
        raise

# ============================================================
# print_mysql:
# params:
# ============================================================
def print_mysql(conn: dbapi.Connection, query: str) -> None:
    logger.info("Querying MySQL")
    print(print_dbapi(conn, query))



def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )
    print("Hello from mysql.py!\n")
    path = mysql_to_arrow("SELECT 'Hello, World!' FROM DUAL", "hello-mysql")

    with (
        dbapi_conn(URI_MYSQL, "mysql") as conn,
        pa.memory_map(str(path), "rb") as source,
        pa.ipc.open_file(source) as reader,
    ):
        create_table(conn, reader.schema, "HELLO")
        arrow_to_mysql(conn, reader, "HELLO")
        print_mysql(conn, "SELECT * FROM `HELLO`")

if __name__ == "__main__":
    main()
