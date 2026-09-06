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
    print("Hello from 02_polars.py!")
    if transactions.exists():
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        eager = pl.read_ipc(
            source=transactions,
            columns=["SENDER", "RECEIVER", "AMOUNT"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(eager)
        senders = eager.group_by(pl.col("SENDER").alias("user_id")).agg(
            pl.col("AMOUNT").sum().alias("sended_amount")
        )
        print(senders)
        receivers = eager.group_by(pl.col("RECEIVER").alias("user_id")).agg(
            pl.col("AMOUNT").sum().alias("received_amount")
        )
        print(receivers)
        net_changes = senders.join(
            receivers, on="user_id", how="full", coalesce=True
        ).fill_null(0)
        print(net_changes)

        print("****LAZY MODE****")
        lazy = pl.scan_ipc(source=transactions)
        net_changes = (
            lazy.group_by(pl.col("SENDER").alias("user_id"))
            .agg(pl.col("AMOUNT").sum().alias("sended_amount"))
            .join(
                lazy.group_by(pl.col("RECEIVER").alias("user_id")).agg(
                    pl.col("AMOUNT").sum().alias("received_amount")
                ),
                on="user_id",
                how="full",
                coalesce=True,
            )
            .fill_null(0)
            .select(
                pl.col("user_id"),
                (pl.col("received_amount") - pl.col("sended_amount")).alias(
                    "net_changes"
                ),
            )
        ).collect()
        print(net_changes)
    else:
        raise FileNotFoundError(f"Path {transactions} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    path = Path("data/arrow") / args.arrow_file
    main(path)
