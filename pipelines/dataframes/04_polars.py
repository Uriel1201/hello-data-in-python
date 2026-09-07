# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import argparse
from pathlib import Path

import polars as pl


def main(dates: Path) -> None:
    print("Hello from 03_polars.py!")
    if dates.exists() and (dates.stem == "04_dates"):
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        eager = pl.read_ipc(
            source=dates,
            columns=["ID", "ACTION_DATE"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(eager)
        positions = (
            eager
            .with_columns(
                pl.int_range(pl.len()).over("ID", order_by="ACTION_DATE", descending=True).alias("POSITION") + 1
            )
        )
        print(positions)
        last = positions.filter(pl.col("POSITION") == 1).select(pl.col("ID"), pl.col("ACTION_DATE").alias("LAST_ACTION"))
        print(last)
        second_last = positions.filter(pl.col("POSITION") == 2).select(pl.col("ID"), pl.col("ACTION_DATE").alias("SECOND_LAST_ACTION"))
        print(second_last)
        result= (last.join(second_last, on="ID", how = "left").with_columns((pl.col("LAST_ACTION") - pl.col("SECOND_LAST_ACTION")).dt.total_days().alias("DAYS_ELAPSED"))
                     .select(pl.col("ID"), pl.col("DAYS_ELAPSED"))
        )   
        print(result)

        print("****LAZY MODE****")
        lazy = (
            pl.scan_ipc(source=dates).with_columns(
                pl.int_range(pl.len()).over("ID", order_by="ACTION_DATE", descending=True).alias("POSITION") + 1
            )
        )
        result = (lazy.filter(pl.col("POSITION") == 1).select(pl.col("ID"), pl.col("ACTION_DATE").alias("LAST_ACTION")).join(lazy.filter(pl.col("POSITION") == 2).select(pl.col("ID"), pl.col("ACTION_DATE").alias("SECOND_LAST_ACTION")), on="ID", how = "left").with_columns((pl.col("LAST_ACTION") - pl.col("SECOND_LAST_ACTION")).dt.total_days().alias("DAYS_ELAPSED"))
                     .select(pl.col("ID"), pl.col("DAYS_ELAPSED"))
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
