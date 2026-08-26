from pathlib import Path
import oracledb as odb
import pyarrow as pa
from hello_data_in_python.utils import get_my_table
from .config import (
    ODB_DSN,
    ODB_USER,
    ODB_PASSWORD,
)


# ============================================================
# get_conn:
# params:
# ============================================================
def get_conn(user: str, password: str, dsn: str) -> odb.Connection:
    return odb.connect(user=user, password=password, dsn=dsn)


# ============================================================
# oracledb_to_arrow:
# params:
# ============================================================
def oracledb_to_arrow(conn: odb.Connection, query: str, output_file: str) -> Path:
    try:
        odf = conn.fetch_df_batches(statement=query, size=10000)
        first_df = next(odf)
        batch = pa.RecordBatch.from_arrays(
            first_df.column_arrays(), names=first_df.column_names()
        )
        output_path = Path("data/arrow") / f"{output_file}.arrow"
        with (
            pa.OSFile(str(output_path), "wb") as my_file,
            pa.ipc.new_file(my_file, batch.schema) as writer,
        ):
            writer.write(batch)
            for df in odf:
                batches = pa.RecordBatch.from_arrays(
                    df.column_arrays(), names=df.column_names()
                )
                writer.write_batch(batches)
        return output_path
    except Exception as e:
        print(f"DATABASE OPERATION FAILED: {e}")
        raise


def main() -> None:
    with get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        print("Hello from oracle.py!")
        print(type(conn))
        sql = """SELECT 'Hello, World!' FROM dual"""
        path = oracledb_to_arrow(conn, sql, "hello_oracle")
        table = get_my_table(path)
        print(
            f"***Arrow File Open***\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
        )


if __name__ == "__main__":
    main()
