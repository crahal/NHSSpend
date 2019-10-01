import glob
import os
import pandas as pd
import ntpath
from unidecode import unidecode

def merge_and_evaluate_scrape(cleanpath, mergepath):
    merged_df = merge_files(cleanpath, mergepath)
    print(list(merged_df))
    merged_df = evaluate_and_clean_merge(merged_df)
    merged_df.to_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
                     header=0, encoding='latin-1', sep='\t')


def merge_files(cleanpath, mergepath):
    frame = pd.DataFrame()
    list_ = []
    for file_ in glob.glob(os.path.join(cleanpath, '*')):
        df = pd.read_csv(file_, index_col=None,
                         header=0, encoding='latin-1', engine='python',
                         dtype={'transactionnumber': str,
                                'amount': float,
                                'supplier': str,
                                'date': str,
                                'expensearea': str,
                                'expensetype': str,
                                'file': str})
        df['dept'] = ntpath.basename(file_)[:-4]
        list_.append(df)
    frame = pd.concat(list_, sort=False)
    frame.dropna(thresh=0.90 * len(df), axis=1, inplace=True)
    if pd.to_numeric(frame['date'], errors='coerce').notnull().all():
        frame['date'] = pd.to_datetime(frame['date'].apply(read_date),
                                       dayfirst=True,
                                       errors='coerce')
    else:
        df['date'] = pd.to_datetime(df['date'],
                                    dayfirst=True,
                                    errors='coerce')
    frame['transactionnumber'] = frame['transactionnumber'].str.replace('[^\w\s]', '')
    frame['transactionnumber'] = frame['transactionnumber'].str.strip("0")
    return frame


def evaluate_and_clean_merge(df):
    df = df.reset_index().drop('index', axis=1)
    print('\n** Evaluating the merged dataset and' +
          ' sequentially cleaning it!**')
    print('** We have ' + str(len(df)) +
          ' total rows of payments data to begin with.')
    print('** We have £' + str(round(df['amount'].sum() / 1000000000, 2)) +
          'bn worth of data to begin with.')
    print('** We have ' + str(len(df['supplier'].unique())) +
          ' unique suppliers to begin with.')
    df['expensetype'] = df['expensetype'].astype(str)
    df['expensetype'] = df['expensetype'].str.lower()
    df['expensetype'] = df['expensetype'].str.strip()
    df['expensetype'] = df['expensearea'].astype(str)
    df['expensetype'] = df['expensearea'].str.lower()
    df['expensetype'] = df['expensearea'].str.strip()
    df['supplier'] = df['supplier'].astype(str)
    df['supplier'] = df['supplier'].str.strip()
    initial = len(df)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df[~pd.isnull(df['amount'])]
    df = df[df['amount'] >= 25000]
    print('Dropped ' + str(initial - len(df)) +
          ' null, non-numeric and payments below £25k in value.')
    initial = len(df)
    df = df[~pd.isnull(df['supplier'])]
    df['supplier'] = df['supplier'].str.replace('\n', ' ').replace('\r', ' ')
    df['supplier'] = df['supplier'].str.strip()
    df = df[df['supplier'] != '']
    df = df[df['supplier'].str.len() > 3]
    df = df[(df['supplier'].notnull()) &
            (df['amount'].notnull())]
    df['date'] = df['date'].apply(pd.to_datetime,
                                  dayfirst=True,
                                  errors='coerce')
    df = df[~pd.isnull(df['date'])]
    print('Dropped ' + str(initial - len(df)) +
          ' rows due to bad supplier or dates.')
    initial = len(df)
    valuefull = df['amount'].sum()
    numsups = len(df['supplier'].unique())
    poss_redacts = ['redacted', 'redaction', 'xxxxxx', 'named individual',
                    'personal expense', 'name withheld', 'name removed']
    for column in ['supplier', 'expensetype', 'expensearea']:
        for term in poss_redacts:
            df = df[~df[column].str.contains(term, na=False)]
    print('Dropped ' + str(initial - len(df)) + ' redacted payments.')
    print('Dropped redacted payments worth £' +
          str(round((valuefull - df['amount'].sum()) / 1000000000, 2)) + 'bn.')
    print('We identified ' + str(numsups - len(df['supplier'].unique())) +
          ' unique redacted supplier variations.')
    initial = len(df)
    numsups = len(df['supplier'].unique())
    valuefull = df['amount'].sum()
    df = df[df['supplier'].str.lower() != 'various']
    print('Dropped ' + str(initial - len(df)) + ' "various" payments.')
    print('Dropped "various" payments worth £' +
          str(round((valuefull - df['amount'].sum()) / 1000000000, 2)) + 'bn.')
    print('We identified ' + str(numsups - len(df['supplier'].unique())) +
          ' unique "various" supplier strings.')
    cols_to_consider = ['amount', 'date', 'dept', 'expensearea',
                        'expensetype', 'transactionnumber', 'supplier']
    df_clean = df.drop_duplicates(subset=cols_to_consider, keep='first')
    df_clean['supplier'] = df_clean['supplier'].str.replace('\t', '')
    df_clean['supplier'] = df_clean['supplier'].str.replace('\n', '')
    df_clean['supplier'] = df_clean['supplier'].str.replace('\r', '')
    df_clean['supplier_upper'] = df_clean['supplier'].apply(
        lambda x: unidecode(x))
    df_clean['supplier_upper'] = df_clean['supplier_upper'].str.strip().str.upper()
    df_clean['supplier_upper'] = df_clean['supplier_upper'].str.replace(
        '\t', '')
    df_clean['supplier_upper'] = df_clean['supplier_upper'].str.replace(
        '\n', '')
    df_clean['supplier_upper'] = df_clean['supplier_upper'].str.replace(
        '\r', '')
    print('Dropped ' + str(len(df) - len(df_clean)) + ' potential duplicates')
    print('Dropped duplicates worth £' + str(round(df_clean['amount'].sum() /
                                                   1000000000, 2)) + 'bn.')
    print('** We have ' + str(len(df_clean)) +
          ' total rows of data to finish with.')
    print('** We have £' +
          str(round(df_clean['amount'].sum() / 1000000000, 2)) +
          'bn worth of data to finish with.')
    print('** We have ' + str(len(df_clean['supplier_upper'].unique())) +
          ' unique suppliers to finish with.')
    print('** We merge from across ' + str(len(df_clean['dept'].unique())) +
          ' departments.')
    print('** This data comes from: ' +
          str(len(df_clean['file'].unique())) + ' files.')
    return df_clean
