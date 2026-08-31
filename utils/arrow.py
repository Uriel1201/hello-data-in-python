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

