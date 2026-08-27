from pathlib import Path

from hello_data_in_python.utils import dbapi_conn, dbapi_to_arrow, get_my_table

from .config import URI_POSTGRESQL

# ============================================================
# postgresql_to_arrow:
# params:
# ============================================================
def postgresql_to_arrow(query: str, output_file: str) -> Path:
    with dbapi_conn(URI_POSTGRESQL, "postgresql") as conn:
        return dbapi_to_arrow(conn, query, output_file)


def main() -> None:
    print("Hello from postgresql.py!")
    path = postgresql_to_arrow("""Select 'Hello, World!'""", "hellow-postgresql")
    table = get_my_table(path)
    print(
        f"Arrow File {path} Open\nTABLE:\n{table.alias}\nSCHEMA:\n{table.table.schema}"
    )


if __name__ == "__main__":
    main()
