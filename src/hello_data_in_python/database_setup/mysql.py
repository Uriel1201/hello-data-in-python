from pathlib import Path

import pyarrow as pa
from adbc_driver_manager import dbapi

from hello_data_in_python.utils import (
    dbapi_conn,
    dbapi_to_arrow,
    get_my_table,
)

from .config import URI_MYSQL


# ============================================================
# get_mysql_schema:
# params:
# ============================================================
def get_mysql_schema(arrow_schema: pa.lib.Schema, table_name: str) -> str:
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
    schema = get_mysql_schema(arrow_schema, table_name)
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(schema)
        conn.commit()


# ============================================================
# mysql_to_arrow:
# params:
# ============================================================
def mysql_to_arrow(query: str, output_file: str) -> Path:
    with dbapi_conn(URI_MYSQL, "mysql") as conn:
        return dbapi_to_arrow(conn, query, output_file)


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
                        {table_name}
                    """)
            last_event = cursor.fetchone()[0]
            for i in range(reader.num_record_batches):
                batch = reader.get_batch(i)
                ids = pa.array(
                    range(last_event + 1, last_event + 1 + batch.num_rows),
                    type=pa.int64(),
                )
                last_event += batch.num_rows
                batch = batch.add_column(0, "EVENT_ID", ids)
                cursor.adbc_ingest(table_name, batch, mode="append")
                conn.commit()
    except Exception as e:
        print(f"{e}")
        raise


def main() -> None:
    print("Hello from mysql.py!\n")
    path = mysql_to_arrow("SELECT 'Hello, World!' FROM DUAL", "hello-mysql")
    table = get_my_table(path)

    print(
        f"Arrow File {path} Open\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
    )
    print(f"VALUES:\n{table.table.slice(0, 1)}")

    with (
        dbapi_conn(URI_MYSQL, "mysql") as conn,
        pa.memory_map(str(path), "rb") as source,
        pa.ipc.open_file(source) as reader,
    ):
        create_table(conn, reader.schema, "HELLO")
        arrow_to_mysql(conn, reader, "HELLO")

    path = mysql_to_arrow("SELECT * FROM HELLO", "hello-key-mysql")
    table = get_my_table(path)
    print(
        f"\nArrow File {path} Open\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
    )
    print(f"VALUES:\n{table.table.slice(0, 1)}")


if __name__ == "__main__":
    main()
