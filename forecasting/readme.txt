This script predicts 3 months of future spending based on 9 months of past purchases for customers of a fictitious company.

1.) The data:
    - customer_info.csv: demographic and miscellaneous data for each customer
    - customer_trans_log.csv: purchasing information for each customer

2.) Analysis is run using analysis.py and calls functions defined in plotters, predictors & readers.
    - plotters: just some visualization functions
    - predictors: the meat of the analysis functions
    - readers: I/O interface

3.) Output is in out.csv, with a dollar amount for the next three months.
