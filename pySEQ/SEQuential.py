from typing import Optional, List
import sys
from dataclasses import asdict
from collections import Counter
import polars as pl
import numpy as np
from scipy.stats import sem, t

from .SEQopts import SEQopts
from .helpers import _colString, bootstrap_loop
from .initialization import _outcome, _numerator, _denominator, _cense_numerator, _cense_denominator
from .expansion import _mapper, _binder, _dynamic, _randomSelection
from .weighting import _weight_prepare_data, _weight_model, _weight_predict, _weight_bind, _weight_cumprod
from .analysis import _outcome_fit, _get_predictions, _calculate_risk, _calculate_survival
from .plot import _survival_plot


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
            parameters: Optional[SEQopts] = None
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
        
        if parameters is None:
            parameters = SEQopts()
            
        # Absorb parameters from SEQopts dataclass
        for name, value in asdict(parameters).items():
            setattr(self, name, value)
        
        # Create default covariates
        if self.covariates is None:
            self.covariates = _outcome(self)

        if self.weighted:
            if self.numerator is None:
                self.numerator = _numerator(self)

            if self.denominator is None:
                self.denominator = _denominator(self)

            if self.cense is not None:
                if self.cense_numerator is None:
                    self.cense_numerator = _cense_numerator()

                if self.cense_denominator is None:
                    self.cense_denominator = _cense_denominator()

    def expand(self):
        kept = [self.cense_colname, self.cense_eligible_colname,
                self.compevent_colname, 
                self.subgroup_colname,
                self.weight_eligible_colnames]
        
        self.data = self.data.with_columns(
            pl.when(pl.col(self.treatment_col).is_in(self.treatment_level))
            .then(self.eligible_col)
            .otherwise(0)
            .alias(self.eligible_col)
        )
        
        self.DT = _binder(_mapper(self.data, self.id_col, self.time_col), self.data,
                          self.id_col, self.time_col, self.eligible_col, self.outcome_col,
                          _colString([self.covariates, 
                                      self.numerator, self.denominator, 
                                      self.cense_numerator, self.cense_denominator]).union(kept), 
                          self.indicator_baseline, self.indicator_squared)
        
        if self.method != "ITT":
            self.DT = _dynamic(self.DT)
        if self.selection_random:
            self.DT = _randomSelection(self.DT)

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
        
    def bootstrap(self, **kwargs):
        allowed = {"bootstrap_nboot", "bootstrap_sample", 
                   "bootstrap_CI", "bootstrap_method"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown argument: {key}")
        
        rng = np.random.RandomState(self.seed) if self.seed is not None else np.random
        UIDs = self.DT.select(pl.col(self.id_col)).unique().to_series().to_list()
        NIDs = len(UIDs)
        
        self._boot_samples = []
        for _ in range(self.bootstrap_nboot):
            sampled_IDs = rng.choice(UIDs, size=int(self.bootstrap_sample * NIDs), replace=True)
            id_counts = Counter(sampled_IDs)
            self._boot_samples.append(id_counts)
        return self
    
    @bootstrap_loop      
    def fit(self):
        if self.weighted and "weight" not in self.DT:
            print("It seems like you have not weighted your data yet, consider running the weight() method first.")
        return _outcome_fit(self.DT,
                            self.outcome_col,
                            self.covariates,
                            self.weighted,
                            "weight")
    def survival(self):
         # some checking if km_curves were setup in settings here:
        risk = _calculate_risk(self)
        
        return risk
  
    def hazard(self):
        pass
        
    def plot(self):
        pass
