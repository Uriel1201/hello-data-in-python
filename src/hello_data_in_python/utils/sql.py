from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import pyarrow as pa
from adbc_driver_manager import dbapi


@dataclass
class MyArrowTable:
    table: pa.Table
    alias: str


# ============================================================
# get_query:
# params:
# ============================================================
def get_query(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file '{filename}' does not exist.")


# ============================================================
# get_my_table:
# params:
# ============================================================
def get_my_table(arrow_file: Path) -> MyArrowTable:
    path_ = str(arrow_file)
    with pa.memory_map(path_, "rb") as source:
        return MyArrowTable(
            table=pa.ipc.open_file(source).read_all(),
            alias=arrow_file.stem,
        )


# ============================================================
# dbapi_conn:
# params:
# ============================================================
def dbapi_conn(uri: str, driver: str) -> dbapi.Connection:
    return dbapi.connect(
        driver=driver,
        db_kwargs={"uri": uri},
    )


# ============================================================
# dbapi_to_arrow:
# params:
# ============================================================
def dbapi_to_arrow(conn: dbapi.Connection, query: str, output_file: str) -> Path:
    try:
        with conn.cursor() as cursor:
            output_path = Path("data/arrow") / f"{output_file}.arrow"
            batches = cursor.execute(query).fetch_record_batch()
            with (
                pa.OSFile(str(output_path), "wb") as my_file,
                pa.ipc.new_file(my_file, batches.schema) as writer,
            ):
                for batch in batches:
                    writer.write_batch(batch)
            return output_path
    except Exception as e:
        print(f"DATABASE OPERATION FAILED: {e}")
        raise


# ============================================================
# print_dbapi:
# params:
# ============================================================
def print_dbapi(conn: dbapi.Connection, query: str) -> pd.DataFrame:
    with conn.cursor() as cursor:
        data = cursor.execute(query).fetchmany(10)
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(data, columns = columns)
