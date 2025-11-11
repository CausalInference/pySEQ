from typing import Optional, List
import sys
from dataclasses import field, asdict
import polars as pl
from .SEQopts import SEQopts
from .helpers import __colString
from .initialization import __outcome, __numerator, __denominator, __cense_numerator, __cense_denominator
from .expansion import __mapper, __binder, __dynamic, __randomSelection
from .weighting import __weight_prepare_data, __weight_model, __weight_predict, __weight_bind, __weight_cumprod
from .analysis import __outcome_predict, __survival_prepare_data, __survival_predict
from .plot import __survival_plot


class SEQuential:
    def __init__(
            self,
            data: pl.DataFrame,
            id_col: str,
            time_col: str,
            eligible_col: str,
            treatment_col: str,
            outcome_col: str,
            time_varying_cols: Optional[List[str]] = None,
            fixed_cols: Optional[List[str]] = None,
            method: str = "ITT",
            parameters: SEQopts = field(default_factory=SEQopts)
    ):
        self.data = data
        self.id_col = id_col
        self.time_col = time_col
        self.eligible_col = eligible_col
        self.treatment_col = treatment_col
        self.outcome_col = outcome_col
        self.time_varying_cols = time_varying_cols
        self.fixed_cols = fixed_cols
        self.method = method
        
        # Absorb parameters from SEQopts dataclass
        for name, value in asdict(parameters).items():
            setattr(self, name, value)
        
        # Create default covariates
        if self.covariates is None:
            self.covariates = __outcome(self)

        if self.weighted:
            if self.numerator is None:
                self.numerator = __numerator(self)

            if self.denominator is None:
                self.denominator = __denominator(self)

            if self.cense is not None:
                if self.cense_numerator is None:
                    self.cense_numerator = __cense_numerator()

                if self.cense_denominator is None:
                    self.cense_denominator = __cense_denominator()

    def expand(self):
        self.DT = __binder(__mapper(self.data), self.data, __colString([
            self.covariates, self.numerator, self.denominator, self.cense_numerator, self.cense_denominator
            ]), self.eligible_col, self.excused_colnames,
            self.baseline_indicator, self.squared_indicator)
        
        if self.method != "ITT":
            self.DT = __dynamic(self.DT)
        if self.selection_random:
            self.DT = __randomSelection(self.DT)

    def weight(self):
        if not self.weighted: 
            sys.exit("""No planned weighting initialized, 
                     consider adding weighted=True in your parameter dictionary""")
        # for level in treatment level do
        # data creation - subset data to where the baseline is level
        # modeling - model from the data and covariates
        # predition - predict on the data the odds for adherence 
        # anti-prediction - where there is no adherence, 1- prediction
        # next
        
            
    def outcome():
        pass

    def survival():
        pass

    def plot():
        pass
