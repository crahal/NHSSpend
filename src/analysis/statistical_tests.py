import os
import statsmodels.api as sm
from tabulate import tabulate

import warnings
import scipy.stats as stats
from permute.core import two_sample
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


def compare_three_dist(data1, data2, data3, alpha, info, reps=None):

#    if len(data2) != len(data1) or len(data3) != len(data1) or len(data2) != len(data3):
#        # Trim or pad arrays to have the same length
#        min_len = min(len(data1), len(data2), len(data3))
#        print('Data lengths unequal, shortening to ', min_len)
#        data1 = data1[:min_len]
#        data2 = data2[:min_len]
#        data3 = data3[:min_len]

    print('Performing distributional tests of equivilent for: ', info)
    try:
        stat, p_val = stats.kruskal(data1, data2, data3)
        print("KW Test Statistic:", np.round(stat, 4))
        print("KW P-value:", np.round(p_val, 4))
        if p_val < alpha:
            print("Reject KW null: Significant difference between groups.")
        else:
            print("Fail to reject KW null: No difference between groups.")
    except ValueError:
        print('Cant perform KW test')

    try:
        stat, crit_val, sig_level = stats.anderson_ksamp([data1, data2, data3])
        print("Anderson-Darling Test Statistic:", np.round(stat, 4))
        print("A-D Critical Values:", [np.round(x, 3) for x in crit_val])
        print("A-D Significance Level:", sig_level)
    except ValueError:
        print('Cant perform AD test')

    # Perform Kolmogorov-Smirnov tests between each pair of distributions
    ks_statistic12, ks_p_value12 = stats.ks_2samp(data1, data2)
    ks_statistic13, ks_p_value13 = stats.ks_2samp(data1, data3)
    ks_statistic23, ks_p_value23 = stats.ks_2samp(data2, data3)
    # Print the results
    print("K-S Stat/p-value for (data1, data2):", ks_statistic12, ks_p_value12)
    print("K-S Stat/p-value for (data1, data3):", ks_statistic13, ks_p_value13)
    print("K-S Stat/p-value for (data1, data2):", ks_statistic23, ks_p_value23)
    if reps != None:
        p_val, stat = two_sample(data1, data2, reps=reps)
        print("Permutation Test Statistic (data1, data2): ", np.round(stat, 4))
        print("Permutation Test P-value (data1, data2): ", np.round(p_val, 4))
        alpha = 0.05
        if p_val < alpha:
            print("Reject Permutation Test Null (data1, data2): " +
                  "Significant difference between groups.")
        else:
            print("Fail to reject Permutation Null: " +
                  "No significant difference between groups.")

        p_val, stat = two_sample(data1, data3, reps=reps)
        print("Permutation Test Statistic (data1, data3): ", np.round(stat, 4))
        print("Permutation Test P-value (data1, data3): ", np.round(p_val, 4))
        alpha = 0.05
        if p_val < alpha:
            print("Reject Permutation Test Null (data1, data3): " +
                  "Significant difference between groups.")
        else:
            print("Fail to reject Permutation Null (data1, data3): " +
                  "No significant difference between groups.")
        p_val, stat = two_sample(data2, data3, reps=reps)
        print("Permutation Test Statistic (data2, data3): ", np.round(stat, 4))
        print("Permutation Test P-value (data2, data3): ", np.round(p_val, 4))
        alpha = 0.05
        if p_val < alpha:
            print("Reject Permutation Test Null (data2, data3): " +
                  "Significant difference between groups.")
        else:
            print("Fail to reject Permutation Null (data2, data3): " +
                  "No significant difference between groups.")
    print('*' * 30)


def compare_two_dist(data1, data2, alpha, info, reps=None):
    print('Performing distributional tests of equivilent for: ', info)
    stat, p_val = stats.kruskal(data1, data2)
    print("KW Test Statistic:", np.round(stat, 4))
    print("KW P-value:", np.round(p_val, 4))
    if p_val < alpha:
        print("Reject KW null: Significant difference between groups.")
    else:
        print("Fail to reject KW null: No difference between groups.")

    stat, crit_val, sig_level = stats.anderson_ksamp([data1, data2])
    print("Anderson-Darling Test Statistic:", np.round(stat, 4))
    print("A-D Critical Values:", [np.round(x, 3) for x in crit_val])
    print("A-D Significance Level:", sig_level)
    ks_statistic12, ks_p_value12 = stats.ks_2samp(data1, data2)
    # Print the results
    print("K-S Stat/p-value for (data1, data2):", ks_statistic12, ks_p_value12)
    if reps != None:
        p_val, stat = two_sample(data1, data2, reps=reps)
        print("Permutation Test Statistic (data1, data2): ", np.round(stat, 4))
        print("Permutation Test P-value (data1, data2): ", np.round(p_val, 4))
        alpha = 0.05
        if p_val < alpha:
            print("Reject Permutation Test Null (data1, data2): " +
                  "Significant difference between groups.")
        else:
            print("Fail to reject Permutation Null: " +
                  "No significant difference between groups.")
    print('*' * 30)


def trimmer(data, lower_quant, upper_quant):
    data = data[(data["amount"] <
                 data["amount"].quantile(upper_quant)) &
                (data["amount"] >
                 data["amount"].quantile(lower_quant))]
    return data



def test_north_vs_south(trust_pay_df, pay_df_cc_trust, shape_path):
    support = pd.read_csv(os.path.join(shape_path, 'NUTS1', 'joined_points.csv'))
    df_all = trust_pay_df.groupby(['dept'])['amount'].sum().reset_index()
    df_cc = pay_df_cc_trust.groupby(['dept'])['amount'].sum().reset_index()
    df_cc['amount'] = df_cc['amount'] / df_all['amount']
    df = pd.merge(df_cc,
                  support[['nuts118nm', 'abrev']],
                  left_on='dept',
                  right_on='abrev')
    conditions = (
            (df['nuts118nm'] == 'East Midlands (England)') |
            (df['nuts118nm'] == 'West Midlands (England)') |
            (df['nuts118nm'] == 'North East (England)') |
            (df['nuts118nm'] == 'North West (England)') |
            (df['nuts118nm'] == 'Yorkshire and The Humber')
    )
    df['N_or_S'] = np.where(conditions, 'North', 'South')
    print('Value Counts')
    print(df['N_or_S'].value_counts())
    print('North mean:', df[df['N_or_S'] == 'North']['amount'].mean())
    print('South mean', df[df['N_or_S'] == 'South']['amount'].mean())
    statistic, p_value = mannwhitneyu(df[df['N_or_S'] == 'North']['amount'],
                                      df[df['N_or_S'] == 'South']['amount'])
    print(f"MW: U Statistic: {statistic}")
    print(f"MW: P-value: {p_value}")
    alpha = 0.05
    if p_value < alpha:
        print("Reject MW null: There is a significant difference between N/S.")
    else:
        print("Fail to reject MW null: There is no significant difference between N/S.")

def make_deterministic_ts_test(series, info, is_month, month=None):
    data = pd.DataFrame({'t': range(1, len(series)+1)})
    data.loc[:, 'y'] = series.to_list()
    data['constant'] = 1
    if is_month == 'No':
        model = sm.OLS(data['y'], data[['constant', 't']])
        results = model.fit()
        print(f'CCEW time series regression for {info}:')
        coefficients = results.params.tolist()
        p_values = results.pvalues.tolist()

        table = [
                ['Constant', coefficients[0], p_values[0]],
                ['t', coefficients[1], p_values[1]],
            ]
        headers = ['Variable', 'Coefficient', 'P-value']
    else:
        data['April_dummy'] = np.where(month=='04', 1, 0)
        model = sm.OLS(data['y'], data[['constant', 't', 'April_dummy']])
        results = model.fit()
        print(f'CCGs time series regression for {info}:')
        coefficients = results.params.tolist()
        p_values = results.pvalues.tolist()

        table = [
                ['Constant', coefficients[0], p_values[0]],
                ['t', coefficients[1], p_values[1]],
                ['April', coefficients[2], p_values[2]],
            ]
        headers = ['Variable', 'Coefficient', 'P-value']
    print(tabulate(table, headers, tablefmt='fancy_grid'))