# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb>=1.5.5",
#     "pyarrow>=25.0.1",
# ]
# ///
import argparse
import logging
from pathlib import Path

from utils import olap

logger = logging.getLogger(__name__)


def main(arrow_file: str, sql: str) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from 01_olap_arrow.py!")
    path = Path("data/arrow") / arrow_file
    my_table = olap.get_my_table(path)
    sql = Path("olap") / sql
    print(olap.my_duck_table(my_table, sql))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    parser.add_argument("sql")
    args = parser.parse_args()
    main(args.arrow_file, args.sql)
