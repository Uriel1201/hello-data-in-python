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
        print("****LAZY MODE****")
        lazy = pl.scan_ipc(source=transactions)
        result = (
            lazy.select("USER_ID")
            .unique()
            .join(
                lazy.with_columns(
                    pl.int_range(pl.len())
                    .over("USER_ID", order_by="TRANSACTION_DATE")
                    .alias("POSITION")
                    + 1
                )
                .filter(pl.col("POSITION") == 2)
                .select(
                    pl.col("USER_ID"), pl.col("TRANSACTION_DATE").alias("DATE_AS_SUPER")
                ),
                on="USER_ID",
                how="left",
            )
        ).collect()
        print(result)
    else:
        raise PermissionError(f"Access denied {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    path = Path("data/arrow") / args.arrow_file
    main(path)
