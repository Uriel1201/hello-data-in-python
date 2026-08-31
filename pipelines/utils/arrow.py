from dataclasses import dataclass
from pathlib import Path
import pyarrow as pa

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
    with pa.memory_map(path_, "rb") as source:
        return MyArrowTable(
            table=pa.ipc.open_file(source).read_all(),
            alias=arrow_file.stem,
        )
