import glob
import os
import pandas as pd
import ntpath
from unidecode import unidecode
import json
from yattag import Doc, indent

def create_html_from_sumstats(htmlpath, sumstats):
    outpath = os.path.join(htmlpath, 'scrape_and_parse_evaluate.html')
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('head'):
        doc.asis('<meta charset="utf-8">')
        doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
        doc.asis('<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">')
        with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
            pass
        with tag('script', src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"):
            pass
        with tag('html'):
            with tag('h1'):
                text('Evaluating the Scrape and Parse of All CCGs')
            with tag('body'):
                with tag('ul', id='grocery-list'):
                    line('li', 'Salt')
                    line('li', 'The number of raw rows is: ' + str(sumstats['rawrows']))
        result = indent(doc.getvalue(), indent_text = True)
        with open(outpath, "w") as file:
            file.write(result)


def merge_and_evaluate_scrape(cleanpath, mergepath, htmlpath, datasummarypath):
    json_path = os.path.join(datasummarypath, 'scrape_and_parse_summary.json')
    merged_df = merge_files(cleanpath, mergepath)
    print(list(merged_df))
#    merged_df, sumstats = evaluate_and_clean_merge(merged_df)
    with open(json_path, encoding='utf8', errors='ignore') as json_file:
        sumstats = json.load(json_file)
    create_html_from_sumstats(htmlpath, sumstats)
#    merged_df.to_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
#                     header=0, encoding='latin-1', sep='\t')
    with open(json_path, 'w') as outfile:
        json.dump(sumstats, outfile)


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
    sumstats = {}
    df = df.reset_index().drop('index', axis=1)
    print('\n** Evaluating the merged dataset and' +
          ' sequentially cleaning it!**')
    sumstats['rawrows'] = len(df)
    print('** We have ' + str(sumstats['rawrows']) +
          ' total rows of payments data to begin with.')
    sumstats['rawvalue'] = df['amount'].sum()
    print('** We have £' + str(round(sumstats['rawvalue'] / 1000000000, 2)) +
          'bn worth of data to begin with.')
    sumstats['rawuniqsup'] = len(df['supplier'].unique())
    print('** We have ' + str(sumstats['rawuniqsup']) +
          ' unique suppliers to begin with.')
    df['expensetype'] = df['expensetype'].astype(str)
    df['expensetype'] = df['expensetype'].str.lower()
    df['expensetype'] = df['expensetype'].str.strip()
    df['expensetype'] = df['expensearea'].astype(str)
    df['expensetype'] = df['expensearea'].str.lower()
    df['expensetype'] = df['expensearea'].str.strip()
    df['supplier'] = df['supplier'].astype(str)
    df['supplier'] = df['supplier'].str.strip()
    initial = df
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df[~pd.isnull(df['amount'])]
    df = df[df['amount'] >= 25000]
    sumstats['droppedbelow25krows'] = len(initial) - len(df)
    print('Dropped ' + str(sumstats['droppedbelow25krows']) +
          ' null, non-numeric and payment rows below £25k.')
    sumstats['droppedbelow25kvalue'] = (initial['amount'].sum() -
                                        df['amount'].sum())
    print('Dropped £' +
          str(round((sumstats['droppedbelow25kvalue'] / 1000000000), 2)) +
          'bn null, non-numeric and payments below £25k in total summed value.')
    initial = df
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
    sumstats['droppedbadsuprows'] = int(len(initial) - len(df))
    print('Dropped ' + str(sumstats['droppedbadsuprows']) +
          ' rows due to bad supplier or dates.')
    sumstats['droppedbadsupamount'] = (initial['amount'].sum() -
                                        df['amount'].sum())
    print('Dropped ' + str(sumstats['droppedbadsupamount']) +
          ' rows due to bad supplier or dates.')
    initial = df
    poss_redacts = ['redacted', 'redaction', 'xxxxxx', 'named individual',
                    'personal expense', 'name withheld', 'name removed']
    for column in ['supplier', 'expensetype', 'expensearea']:
        for term in poss_redacts:
            df = df[~df[column].str.contains(term, na=False)]
    sumstats['droppedredactrows'] = len(initial)-len(df)
    print('Dropped ' + str(sumstats['droppedredactrows']) +
          ' redacted payments.')
    sumstats['droppedredactvalue'] = (initial['amount'].sum() -
                                      df['amount'].sum())
    print('Dropped redacted payments worth £' +
          str(round(sumstats['droppedredactvalue'] / 1000000000, 2)) + 'bn.')
    sumstats['uniquesupredact'] = (len(initial['supplier'].unique()) -
                                   len(df['supplier'].unique()))
    print('We identified ' + str(sumstats['uniquesupredact']) +
          ' unique redacted supplier variations.')
    initial = df
    df = df[df['supplier'].str.lower() != 'various']
    sumstats['droppedvariousrows'] = len(initial) - len(df)
    print('Dropped ' + str(sumstats['droppedvariousrows']) +
          ' "various" payments.')
    sumstats['droppedvariousamount'] = (initial['amount'].sum() -
                                         df['amount'].sum())
    print('Dropped "various" payments worth £' +
          str(round(sumstats['droppedvariousamount'] / 1000000000, 2)) +
          'bn.')
    sumstats['uniquesupvarious'] = (len(initial['supplier'].unique()) -
                                    len(df['supplier'].unique()))
    print('We identified ' + str(sumstats['uniquesupvarious']) +
          ' unique "various" supplier strings.')
    cols_to_consider = ['amount', 'date', 'dept', 'expensearea',
                        'expensetype', 'transactionnumber', 'supplier']
    initial = df
    df = initial.drop_duplicates(subset=cols_to_consider, keep='first')
    df['supplier'] = df['supplier'].str.replace('\t', '')
    df['supplier'] = df['supplier'].str.replace('\n', '')
    df['supplier'] = df['supplier'].str.replace('\r', '')
    df['supplier_upper'] = df['supplier'].apply(
        lambda x: unidecode(x))
    df['supplier_upper'] = df['supplier_upper'].str.strip().str.upper()
    df['supplier_upper'] = df['supplier_upper'].str.replace(
        '\t', '')
    df['supplier_upper'] = df['supplier_upper'].str.replace(
        '\n', '')
    df['supplier_upper'] = df['supplier_upper'].str.replace(
        '\r', '')
    sumstats['dropduplicrows'] = len(initial) - len(df)
    print('Dropped ' + str(sumstats['dropduplicrows']) +
          ' potential duplicates')
    sumstats['dropduplicvalue'] = (initial['amount'].sum() -
                                   df['amount'].sum())
    print('Dropped duplicates worth £' +
          str(round(sumstats['dropduplicvalue'] / 1000000000, 2)) + 'bn.')
    sumstats['totalcleanrows'] = len(df)
    print('** We have ' + str(sumstats['totalcleanrows']) +
          ' total rows of data to finish with.')
    sumstats['totalcleanvalue'] = df['amount'].sum()
    print('** We have £' +
          str(round(sumstats['totalcleanvalue'] / 1000000000, 2)) +
          'bn worth of data to finish with.')
    sumstats['totalcleanuniqsup'] = len(df['supplier_upper'].unique())
    print('** We have ' + str(sumstats['totalcleanuniqsup']) +
          ' unique suppliers to finish with.')
    sumstats['totalcleanuniqdept'] = len(df['dept'].unique())
    print('** We merge from across ' + str(sumstats['totalcleanuniqdept']) +
          ' departments.')
    sumstats['totalcleanuniqfiles'] = len(df['file'].unique())
    print('** This data comes from: ' +
          str(sumstats['totalcleanuniqfiles']) + ' files.')
    return df, sumstats
