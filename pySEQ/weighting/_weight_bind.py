import polars as pl

def _weight_bind(self, WDT):
    if self.weight_preexpansion:
        if self.excused:       
            WDT = self.DT.join(
                WDT.rename({self.time_col: "period"}),
                on=[self.id_col, "period"],
                how="left"
                ).with_columns([
                    pl.when((pl.col("trial") == 0) & (pl.col("period") == 0))
                    .then(pl.lit(1.))
                    .when((pl.col("denominator") < 1e-15) | (pl.col(self.outcome_col).is_null()))
                    .then(pl.lit(1.))
                    .otherwise(pl.col("denominator"))
                    .alias("denominator")
                    ]).with_columns([
                        pl.when((pl.col("numerator") / pl.col("denominator")).is_null())
                        .then(pl.lit(1.))
                        .otherwise(pl.col("numerator") / pl.col("denominator"))
                        .alias("wt")
                        ]) \
                            .sort([self.id_col, "trial", "followup"]) \
                                .with_columns([
                                    pl.col("wt").cum_prod().over([self.id_col, "trial"]).alias("weight")
                                    ])
        else:
            WDT = self.DT.join(WDT.rename({self.time_col: "period"}),
                            on = [self.id_col, "period"],
                            how = "left") \
                                .with_columns(
                                    **{
                                        col: pl.when(pl.col("trial") == pl.col("trial").min().over(self.id_col))
                                        .then(1.0)
                                        .otherwise(pl.col(col))
                                        for col in ["numerator", "denominator"]
                                        }
                                ).with_columns([
                                    (pl.col("numerator") / pl.col("denominator")).alias("wt"),
                                    pl.when(pl.col("wt").is_null())
                                    .then(pl.lit(1.))
                                    .otherwise(pl.col("wt"))
                                    .alias("wt")
                                ]).sort([self.id_col, "trial", "followup"]) \
                                    .with_columns([
                                        pl.col("wt")
                                        .cum_prod()
                                        .over([self.id_col, "trial"])
                                        .alias("weight")
                                    ])
    else:
        WDT = self.DT.join(WDT,
                           on = [])
    
    self.DT = WDT