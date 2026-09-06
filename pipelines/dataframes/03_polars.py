# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import argparse
from pathlib import Path

import polars as pl


def main(items: Path) -> None:
    print("Hello from 02_polars.py!")
    if items.exists() and (items.stem == "03_items"):
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        eager = pl.read_ipc(
            source=items,
            columns=["ITEM", "DATES"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(eager)
        
        print("****LAZY MODE****")
        lazy = pl.scan_ipc(source=items)
        
    else:
        raise PermissionError(f"Access denied {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    path = Path("data/arrow") / args.arrow_file
    main(path)
