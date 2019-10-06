import pandas as pd
import os
import random

def transparency_score(num_files, days_last_trans, pc_pdfs, ease_scraping):
    return random.randint(1,100)
    ''' generating the transparency score for the ccg'''


def output_for_dashboard(mergepath, dashboard):
    generate_coverage_dashboard_dataset(mergepath, dashboard)


def generate_coverage_dashboard_dataset(mergepath, dashboard):
    df = pd.read_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
                     index_col=None, encoding='latin-1',
                     engine='python', sep = '\t',
                     dtype={'transactionnumber': str, 'amount': float,
                            'supplier': str, 'date': str, 'file': str,
                            'expensearea': str, 'expensetype': str})
    coverage_df = pd.DataFrame(index = df['dept'].unique(),
                               columns =['Number_Payments',
                                         'Payment_Value','Number_Files',
                                         'Transparency Score'])
    for ccg in coverage_df.index:
        temp_df = df[df['dept']==ccg]
        coverage_df.at[ccg, 'Number_Payments'] = len(temp_df)
        coverage_df.at[ccg, 'Number_Files'] = len(temp_df['file'].unique())
        coverage_df.at[ccg, 'Payment_Value'] = temp_df['amount'].sum()
        coverage_df.at[ccg, 'Transparency Score'] = transparency_score(random.randint(0, 120),
                                                                       random.randint(0, 450),
                                                                       random.randint(0, 100),
                                                                       random.randint(1, 5))
    coverage_df.to_csv(os.path.join(dashboard, 'coverage.csv'))
