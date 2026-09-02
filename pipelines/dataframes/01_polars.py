# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars>=1.44.1",
# ]
# ///
import polars 

def main() -> None:
    print("Hello from 01_polars.py!")
    polars.Config.set_tbl_width_chars(50)
    users = polars.read_ipc(source = "data/arrow/01_oracledb_users.arrow", columns = ["USER_ID", "ACTION"], use_pyarrow = False, memory_map = True)
    print(users)
    
    rates = (users.lazy()
                  .group_by('USER_ID')
    ).collect()
    
    """
                 .agg([pl.col('ACTION').filter(pl.col('ACTION')=='start').count().alias('STARTS'),
                       pl.col('ACTION').filter(pl.col('ACTION')=='cancel').count().alias('CANCELS'),
                       pl.col('ACTION').filter(pl.col('ACTION')=='publish').count().alias('PUBLISHES')
                       ])
    """
    print(rates)
    """
                  .select(pl.col('USER_ID'),
                          pl.when(pl.col('STARTS') > 0)
                            .then(pl.col('CANCELS') / pl.col('STARTS'))
                            .otherwise(None)
                            .alias('CANCEL_RATE'),
                          pl.when(pl.col('STARTS') > 0)
                            .then(pl.col('PUBLISHES') / pl.col('STARTS'))
                            .otherwise(None)
                            .alias('PUBLISH_RATE')
                   )
               )
    """


if __name__ == "__main__":
    main()
