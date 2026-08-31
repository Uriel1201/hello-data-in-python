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
