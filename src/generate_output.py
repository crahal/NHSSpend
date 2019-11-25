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
                                         'Transparency Score',
                                         'Number_csv', 'PC_csv',
                                         'Number_pdf', 'PC_pdf',
                                         'Number_xlsx', 'PC_xlsx',
                                         'Number_xls', 'PC_xls',
                                         'Number_ods', 'PC_ods'])
    for ccg in coverage_df.index:
        temp_df = df[df['dept']==ccg]
        coverage_df.at[ccg, 'Number_Payments'] = len(temp_df)
        coverage_df.at[ccg, 'Number_Files'] = len(temp_df['file'].unique())
        coverage_df.at[ccg, 'Number_csv'] = len(temp_df[(temp_df['file'].str.lower().str.endswith('.csv')) &
                                                       ~(temp_df['file'].str.lower().str.contains('.pdf'))]['file'].unique())
        coverage_df.at[ccg, 'PC_csv'] = (coverage_df.at[ccg, 'Number_csv']/coverage_df.at[ccg, 'Number_Files'])*100
        coverage_df.at[ccg, 'Number_pdf'] = len(temp_df[temp_df['file'].str.lower().str.contains('.pdf')]['file'].unique())
        coverage_df.at[ccg, 'PC_pdf'] = (coverage_df.at[ccg, 'Number_pdf']/coverage_df.at[ccg, 'Number_Files'])*100
        coverage_df.at[ccg, 'Number_xls'] = len(temp_df[temp_df['file'].str.lower().str.endswith('.xls')]['file'].unique())
        coverage_df.at[ccg, 'PC_xls'] = (coverage_df.at[ccg, 'Number_xls']/coverage_df.at[ccg, 'Number_Files'])*100
        coverage_df.at[ccg, 'Number_xlsx'] = len(temp_df[temp_df['file'].str.lower().str.endswith('.xlsx')]['file'].unique())
        coverage_df.at[ccg, 'PC_xlsx'] = (coverage_df.at[ccg, 'Number_xlsx']/coverage_df.at[ccg, 'Number_Files'])*100
        coverage_df.at[ccg, 'Number_ods'] = len(temp_df[temp_df['file'].str.lower().str.endswith('.ods')]['file'].unique())
        coverage_df.at[ccg, 'PC_ods'] = (coverage_df.at[ccg, 'Number_ods']/coverage_df.at[ccg, 'Number_Files'])*100
        coverage_df.at[ccg, 'Payment_Value'] = temp_df['amount'].sum()
        coverage_df.at[ccg, 'Transparency Score'] = transparency_score(random.randint(0, 120),
                                                                       random.randint(0, 450),
                                                                       random.randint(0, 100),
                                                                       random.randint(1, 5))
    coverage_df.to_csv(os.path.join(dashboard, 'coverage.csv'))
