import logging
from dataclasses import dataclass
from pathlib import Path

import duckdb as duck
import pyarrow as pa

logger = logging.getLogger(__name__)


@dataclass
class MyArrowTable:
    table: pa.Table
    alias: str


# ============================================================
# get_my_table:
# params:
# ============================================================
def get_my_table(arrow_file: Path) -> MyArrowTable:
    path_ = str(arrow_file)
    if arrow_file.exists():
        with pa.memory_map(path_, "rb") as source:
            logger.info(f"IPC file:{arrow_file} read")
            return MyArrowTable(
                table = pa.ipc.open_file(source).read_all(),
                alias = arrow_file.stem,
            )
    else:
        raise FileNotFoundError(f"Path {arrow_file} does not exist")


# ============================================================
# print_duck:
# params:
# ============================================================
def my_duck_table(table: MyArrowTable, sql: Path) -> pa.Table:
    try:
        with open(sql, "r", encoding="utf-8") as file:
            logger.info(f"Querying table {table.alias}")
            query = file.read().format(table = table.alias)
            duck.register(table.alias, table.table)
            return duck.sql(query).to_arrow_table()
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file '{sql}' does not exist.")
