import argparse
import logging
from pathlib import Path

from hello_data_in_python.utils import olap

logger = logging.getLogger(__name__)


def main(arrow_file: str, sql: str) -> None:
    logging.basicConfig(level=logging.INFO)
    print("Hello from olap_arrow.py!")
    path = Path("data/arrow") / arrow_file
    my_table = olap.get_my_table(path)
    sql = Path("olap") / sql
    df = olap.my_duck_table(my_table, sql).to_pandas()
    print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    parser.add_argument("sql")
    args = parser.parse_args()
    main(args.arrow_file, args.sql)
