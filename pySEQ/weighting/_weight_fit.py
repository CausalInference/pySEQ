import polars as pl
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

def _fit_LTFU(self, WDT: pl.DataFrame):
    if self.cense_colname is None:
        return
    else:
        fits = []
        for i in [self.cense_numerator, self.cense_denominator]:
            formula = f"{self.cense_colname}~{i}"
            model = smf.glm(
                formula,
                WDT,
                family=sm.families.Binomial()
            )
            model_fit = model.fit()
            fits.append(model_fit)
        
        self.cense_numerator = fits[0]
        self.cense_denominator = fits[1]

def _fit_numerator(self, WDT: pl.DataFrame):
    if self.weight_preexpansion and self.excused:
        return
    if self.method == "ITT":
        return
    
    formula = f"{self.treatment_col}~{self.numerator}"
    tx_bas = f"{self.treatment_col}{self.indicator_baseline}"
    fits = []
    for i in self.treatment_level:
        DT_subset = WDT[WDT[tx_bas].isin(i)]
        model = smf.mnlogit(
            formula,
            DT_subset
            )
        model_fit = model.fit()
        fits.append(model_fit)
        
    self.denominator_model = model_fit
        
def _fit_denominator(self, WDT):
    if self.method == "ITT":
        return
    
    formula = f"{self.treatment_col}~{self.denominator}"
    tx_bas = f"{self.treatment_col}{self.indicator_baseline}"
    fits = []
    for i in self.treatment_level:
        DT_subset = WDT[WDT[tx_bas].isin(i)]
        model = smf.mnlogit(
            formula,
            DT_subset
            )
        model_fit = model.fit()
        fits.append(model_fit)
        
    self.denominator_model = model_fit