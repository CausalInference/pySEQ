import polars as pl

def __mapper(data, id_col, time_col, parameters):
    """
    Internal function to create the expanded map to bind data to.

    """
    DT = (
        data.with_columns([
            pl.count().over(id_col).alias("group_count"),
            pl.col(id_col).cum_count().over(id_col).alias("trial")

        ])
        .with_columns([
            pl.struct([pl.col(time_col), pl.col("group_count")])
            .apply(lambda s: list(range(s[time_col], s["group_count"])))
            .alias("period")
        ])
        .explode("period")
        .with_columns([
            pl.cum_count().over([id_col, "trial"]).alias("followup")
        ])
        .filter((pl.col("followup") >= parameters["followup_min"]) &
                (pl.col("followup") <= parameters["followup_max"]))
    )
    return DT