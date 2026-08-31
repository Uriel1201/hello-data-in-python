from pathlib import Path
import logging 

import oracledb as odb
import pyarrow as pa
import pandas as pd

from .config import (
    ODB_DSN,
    ODB_PASSWORD,
    ODB_USER,
)

logger = logging.getLogger(__name__)


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
        logger.info(f"Arrow File created -> {output_path}")
        return output_path
    except Exception as e:
        print(f"DATABASE OPERATION FAILED: {e}")
        raise

def print_oracle(conn: odb.Connection, query: str) -> None:
    logger.info(f"Querying Oracle")
    with conn.cursor() as cursor:
        cursor.execute(query)
        num_rows = 20
        while True:
            rows = cursor.fetchmany(size=num_rows)
            if not rows:
                break
            columns = [column[0] for column in cursor.description]
            print(pd.DataFrame(rows, columns=columns))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    with get_conn(ODB_USER, ODB_PASSWORD, ODB_DSN) as conn:
        print("Hello from oracle.py!\n")
        sql = """SELECT 'Hello, World!' FROM dual"""
        oracledb_to_arrow(conn, sql, "hello_oracle")
        print_oracle(conn, sql)

if __name__ == "__main__":
    main()
