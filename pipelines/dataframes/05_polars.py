# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import argparse
from pathlib import Path

import polars as pl


def main(transactions: Path) -> None:
    print("Hello from 05_polars.py!")
    if transactions.exists() and (transactions.stem == "05_transactions"):
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        eager = pl.read_ipc(
            source=transactions,
            columns=["USER_ID", "TRANSACTION_DATE"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(eager)
        
        print("****LAZY MODE****")
        lazy = pl.scan_ipc(source=transactions)
    else:
        raise PermissionError(f"Access denied {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    path = Path("data/arrow") / args.arrow_file
    main(path)
