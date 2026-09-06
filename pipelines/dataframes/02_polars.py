# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import polars as pl
from pathlib import Path
import argparse

def main(transactions: Path) -> None:
    print("Hello from 02_polars.py!")
    if transactions.exists():
        pl.Config.set_tbl_width_chars(60)
        print("****EAGER MODE****")
        transactions = pl.read_ipc(
            source=transactions,
            columns=["SENDER", "RECEIVER", "AMOUNT"],
            n_rows=10,
            use_pyarrow=False,
            memory_map=True,
        )
        print(transactions)
        senders = transactions.group_by(pl.col("SENDER").alias("user_id")).agg(pl.col("AMOUNT").sum().alias("sended_amount"))
        print(senders)
        receivers = transactions.group_by(pl.col("RECEIVER").alias("user_id")).agg(pl.col("AMOUNT").sum().alias("received_amount"))
        print(receivers)
        net_changes = senders.join(receivers, on="user_id", how="full", coalesce=True).fill_null(0)
        print(net_changes)
    else:
        raise FileNotFoundError(f"Path {arrow_file} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arrow_file")
    args = parser.parse_args()
    path = Path("data/arrow") / args.arrow_file
    main(path)
