# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb>=1.5.5",
#     "pyarrow>=25.0.1",
# ]
# ///
import argparse
from pathlib import Path
from utils import olap
import duckdb as duck


# ============================================================
# print_duck_query:
# params:
# ============================================================
def print_duck(table: olap.MyArrowTable, query: str) -> None:

    duck.register(table.alias, table.table)
    duck.sql(query).show()


def main(sql_file: str) -> None:
    print("Hello from 01_olap_arrow.py!")
    path = Path("data/arrow/01_oracle.arrow")
    my_table = olap.get_my_table(path)
    query = olap.get_query(f"olap/{sql_file}", "01_oracle")
    print(query)
    print_duck(my_table, query)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sql_file")
    args = parser.parse_args()
    main(args.sql_file)
