# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import polars as pl
import argparse
from pathlib import Path


def main(arrow_file: str) -> None:
    path = Path("data/arrow") / arrow_file
    if path.exists():
        print("Hello from 01_polars.py!")
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        users = pl.read_ipc(
            source=path,
            columns=["USER_ID", "ACTION"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(users)

        totals = users.group_by("USER_ID").agg(
            [
                pl.col("ACTION")
                .filter(pl.col("ACTION") == "start")
                .count()
                .alias("TOTAL_STARTS"),
                pl.col("ACTION")
                .filter(pl.col("ACTION") == "cancel")
                .count()
                .alias("TOTAL_CANCELS"),
                pl.col("ACTION")
                .filter(pl.col("ACTION") == "publish")
                .count()
                .alias("TOTAL_PUBLISHES"),
            ]
        )
        print(totals)

        rates = totals.select(
            pl.col("USER_ID"),
            pl.when(pl.col("TOTAL_STARTS") > 0)
            .then(pl.col("TOTAL_CANCELS") / pl.col("TOTAL_STARTS"))
            .otherwise(None)
            .alias("CANCEL_RATE"),
            pl.when(pl.col("TOTAL_STARTS") > 0)
            .then(pl.col("TOTAL_PUBLISHES") / pl.col("TOTAL_STARTS"))
            .otherwise(None)
            .alias("PUBLISH_RATE"),
        )
        print(rates)
        print("****LAZY MODE****")
        rates = (
            pl.scan_ipc(source=path)
            .group_by("USER_ID")
            .agg(
                [
                    pl.col("ACTION")
                    .filter(pl.col("ACTION") == "start")
                    .count()
                    .alias("TOTAL_STARTS"),
                    pl.col("ACTION")
                    .filter(pl.col("ACTION") == "cancel")
                    .count()
                    .alias("TOTAL_CANCELS"),
                    pl.col("ACTION")
                    .filter(pl.col("ACTION") == "publish")
                    .count()
                    .alias("TOTAL_PUBLISHES"),
                ]
            )
            .select(
                pl.col("USER_ID"),
                pl.when(pl.col("TOTAL_STARTS") > 0)
                .then(pl.col("TOTAL_CANCELS") / pl.col("TOTAL_STARTS"))
                .otherwise(None)
                .alias("CANCEL_RATE"),
                pl.when(pl.col("TOTAL_STARTS") > 0)
                .then(pl.col("TOTAL_PUBLISHES") / pl.col("TOTAL_STARTS"))
                .otherwise(None)
                .alias("PUBLISH_RATE"),
            )
        ).collect()
        print(rates)
    else:
        raise FileNotFoundError(f"Path {arrow_file} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    main(args.arrow_file)
