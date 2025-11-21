from pySEQ import SEQuential, SEQopts
from pySEQ.data import load_data

def test_ITT_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "ITT",
        parameters=SEQopts()
    )
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]['Coef.'].to_list()
    assert matrix == [-6.828506035553367, 0.12717241010543864, 0.1893500309004178, 
                      0.03371515698762837, -0.00014691202235021713, 0.044566165558946304, 
                      0.000578777043905276, 0.0032906669395291782, -0.013392420492057825, 
                      0.20072409918428197]

def test_PreE_dose_response_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "dose-response",
        parameters=SEQopts(weighted=True,
                           weight_preexpansion=True)
    )
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]['Coef.'].to_list()
    assert matrix == [-4.842735939069144, 0.14286755770151904, 0.055221018477671927, 
                      -0.000581657931537684, -0.008484541900408258, 0.00021073328759912806, 
                      0.010537967151467553, 0.0007772316818101141]
    return

def test_PostE_dose_response_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "dose-response",
        parameters=SEQopts(weighted=True)
    )
    
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]['Coef.'].to_list()
    assert matrix == [-6.378405714539087, 0.17837811837341735, 0.04468084245849907, 
                      -0.0002872109540598882, -0.00016802503876320882, -1.646518424567451e-05, 
                      0.037968809158708365, 0.0006587394643894709, 0.002530895897349477, 
                      -0.039757502333589004, 0.16383943829099348]

def test_PreE_censoring_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "censoring",
        parameters=SEQopts(weighted=True,
                           weight_preexpansion=True)
    )
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]['Coef.'].to_list()
    assert matrix == [-4.661102616366661, 0.06322831388844205, 0.5000738277717721, 
                      0.007974580521778882, 0.0005337038990034418, -0.011577561000157839, 
                      0.0010459271332870575]

def test_PostE_censoring_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "censoring",
        parameters=SEQopts(weighted=True)
    )
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]["Coef."].to_list()
    assert matrix == [-7.5529979759196735, 0.09676401101585402, 
                      0.47314996909212975, 0.009424470533477088, 
                      0.0005314170238427201, 0.041113888641022785, 
                      0.0007102010905924148, 0.003667143725614389, 
                      0.007220844654484469, 0.3009824885910414]

def test_PreE_censoring_excused_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "censoring",
        parameters=SEQopts(weighted=True,
                           weight_preexpansion=True,
                           excused=True,
                           excused_colnames=["excusedZero", "excusedOne"])
    )
    s.expand()
    s.fit()
    matrix = s.outcome_model[0].summary2().tables[1]['Coef.'].to_list()
    assert matrix == [-4.785472683278245, 0.36610312911034926, 0.029561364724039044, 
                      -0.00020039125274747224, 0.021971717586055102, 0.0004172559228901589]

def test_PostE_censoring_excused_coefs():
    data = load_data("SEQdata")
    
    s = SEQuential(
        data,
        id_col="ID",
        time_col="time",
        eligible_col="eligible",
        treatment_col="tx_init",
        outcome_col="outcome",
        time_varying_cols=["N", "L", "P"],
        fixed_cols=["sex"],
        method = "censoring",
        parameters=SEQopts(weighted=True,
                           excused=True,
                           excused_colnames=["excusedZero", "excusedOne"])
    )
    s.expand()
    s.fit()
    print(s.weight_stats)
    print(s.numerator_model[0].summary())
    print(s.numerator_model[1].summary())
    print(s.denominator_model[0].summary())
    print(s.denominator_model[1].summary())
    matrix = s.outcome_model[0].summary()
    return print(matrix)
test_PostE_censoring_excused_coefs()