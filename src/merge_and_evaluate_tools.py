import glob
import os
import pandas as pd
import ntpath
from unidecode import unidecode
import json
from datetime import datetime
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
                text('Evaluating CCG Data')
            with tag('body'):
                with tag('ul', id='grocery-list'):
                    line('li', 'Number of raw rows: ' +
                               str(sumstats['rawrows']))
                    line('li', 'Value of raw data is: £' +
                               str(sumstats['rawvalue']) + 'bn')
                    line('li', 'Number of unique suppliers in raw data : ' +
                               str(sumstats['rawuniqsup']))
                    line('li', 'Number of rows below £25k dropped : ' +
                               str(sumstats['droppedbelow25krows']))
                    line('li', 'Value of rows below £25k dropped: £' +
                               str(sumstats['droppedbelow25kvalue']) + 'bn')
                    line('li', 'Number of bad supplier rows dropped: ' +
                               str(sumstats['droppedbadsuprows']))
                    line('li', 'Value of bad supplier rows dropped: £' +
                               str(sumstats['droppedbadsupamount'])+'bn')
                    line('li', 'Number of redacted rows dropped: ' +
                               str(sumstats['droppedredactrows']))
                    line('li', 'Value of redacted rows dropped: £' +
                               str(sumstats['droppedredactvalue']) +'m')
                    line('li', 'Number of unique suppliers redacted: ' +
                               str(sumstats['uniquesupredact']))
                    line('li', 'Number rows containing "various": ' +
                               str(sumstats['droppedvariousrows']))
                    line('li', 'Value of rows containing "various": £' +
                               str(sumstats['droppedvariousamount']))
                    line('li', 'Number of unique "various" suppliers: ' +
                               str(sumstats['uniquesupvarious']))
                    line('li', 'Number of potentially duplicated rows: ' +
                               str(sumstats['dropduplicrows']) + 'bn')
                    line('li', 'Value of potentially duplicated rows: £' +
                               str(sumstats['dropduplicvalue']))
                    line('li', 'Total number of cleaned rows of data: ' +
                               str(sumstats['totalcleanrows']))
                    line('li', 'Total value of cleaned rows of data: £' +
                               str(sumstats['totalcleanvalue']) + 'bn')
                    line('li', 'Total number of unique suppliers in clean data: ' +
                               str(sumstats['totalcleanuniqsup']))
                    line('li', 'Total number of ccgs in cleaned data: ' +
                               str(sumstats['totalcleanuniqdept']))
                    line('li', 'Total number of unique files in cleaned data: ' +
                               str(sumstats['totalcleanuniqfiles']))
        result = indent(doc.getvalue(), indent_text = True)
        with open(outpath, "w") as file:
            file.write(result)


def merge_and_evaluate_scrape(cleanpath, mergepath, htmlpath, datasummarypath, logpath):
    json_path = os.path.join(datasummarypath, 'scrape_and_parse_summary.json')
    merged_df = merge_files(cleanpath, mergepath)
    merged_df, sumstats = evaluate_and_clean_merge(merged_df, logpath)
    create_html_from_sumstats(htmlpath, sumstats)
    merged_df.to_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
                     encoding='latin-1', sep='\t')
    sup_count = pd.DataFrame(merged_df.groupby('supplier')['supplier'].
                count()).rename({'supplier': 'num_pay'}, axis=1)
    sup_value = pd.DataFrame(merged_df.groupby('supplier')['amount'].sum()).\
                rename({'amount': 'tot_pay_val'}, axis=1)
    sup_merge = pd.merge(sup_count, sup_value,
                         left_index=True, right_index=True)
    sup_merge = sup_merge.sort_values(by='num_pay', ascending=False)
    sup_merge.to_csv(os.path.join(mergepath, 'unique_unmatched_suppliers.tsv'),
                     encoding='latin-1', sep='\t')
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


def evaluate_and_clean_merge(df, logpath):
    sumstats = {}
    with open(os.path.join(logpath, 'eval_logs',
                           datetime.now().strftime('Eval_clean_%Y_%m_%d_%H_%M_%S') +\
                           '.txt'), 'a') as the_file:
        df = df.reset_index().drop('index', axis=1)
        the_file.write('** Evaluating the merged dataset and' +
              ' sequentially cleaning it!**\n')
        sumstats['rawrows'] = len(df)
        the_file.write('** We have ' + str(sumstats['rawrows']) +
                       ' total rows of payments data to begin with.\n')
        sumstats['rawvalue'] = round(df['amount'].sum() / 1000000000, 2)
        the_file.write('** We have £' + str(sumstats['rawvalue']) +
              'bn worth of data to begin with.\n')
        sumstats['rawuniqsup'] = len(df['supplier'].unique())
        the_file.write('** We have ' + str(sumstats['rawuniqsup']) +
                       ' unique suppliers to begin with.\n')
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
        the_file.write('Dropped ' + str(sumstats['droppedbelow25krows']) +
                       ' null, non-numeric and payment rows below £25k.\n')
        sumstats['droppedbelow25kvalue'] = round((initial['amount'].sum() -
                                                  df['amount'].sum()) /
                                                  1000000000, 2)
        the_file.write('Dropped £' +
              str(sumstats['droppedbelow25kvalue']) +
              'bn null, non-numeric and payments below £25k in total summed value.\n')
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
        the_file.write('Dropped ' + str(sumstats['droppedbadsuprows']) +
              ' rows due to bad supplier or dates.\n')
        sumstats['droppedbadsupamount'] = round((initial['amount'].sum() -
                                                 df['amount'].sum()) /
                                                 1000000000, 2)
        the_file.write('Dropped ' + str(sumstats['droppedbadsupamount']) +
                       ' rows due to bad supplier or dates.\n')
        initial = df
        poss_redacts = ['redacted', 'redaction', 'xxxxxx', 'named individual',
                        'personal expense', 'name withheld', 'name removed']
        for column in ['supplier', 'expensetype', 'expensearea']:
            for term in poss_redacts:
                df = df[~df[column].str.contains(term, na=False)]
        sumstats['droppedredactrows'] = len(initial)-len(df)
        the_file.write('Dropped ' + str(sumstats['droppedredactrows']) +
                       ' redacted payments.\n')
        sumstats['droppedredactvalue'] = round((initial['amount'].sum() -
                                               df['amount'].sum())/ 1000000, 2)
        the_file.write('Dropped redacted payments worth £' +
              str(sumstats['droppedredactvalue']) + 'm.\n')
        sumstats['uniquesupredact'] = (len(initial['supplier'].unique()) -
                                       len(df['supplier'].unique()))
        the_file.write('We identified ' + str(sumstats['uniquesupredact']) +
              ' unique redacted supplier variations.\n')
        initial = df
        df = df[df['supplier'].str.lower() != 'various']
        sumstats['droppedvariousrows'] = len(initial) - len(df)
        the_file.write('Dropped ' + str(sumstats['droppedvariousrows']) +
              ' "various" payments.\n')
        sumstats['droppedvariousamount'] = (initial['amount'].sum() -
                                             df['amount'].sum())
        the_file.write('Dropped "various" payments worth £' +
              str(round(sumstats['droppedvariousamount'] / 1000000, 2)) +
              'm.\n')
        sumstats['uniquesupvarious'] = (len(initial['supplier'].unique()) -
                                        len(df['supplier'].unique()))
        the_file.write('We identified ' + str(sumstats['uniquesupvarious']) +
                       ' unique "various" supplier strings.\n')
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
        the_file.write('Dropped ' + str(sumstats['dropduplicrows']) +
              ' potential duplicates\n')
        sumstats['dropduplicvalue'] = round((initial['amount'].sum() -
                                       df['amount'].sum())/ 1000000000, 2)
        the_file.write('Dropped duplicates worth £' +
              str(sumstats['dropduplicvalue']) + 'bn.\n')
        sumstats['totalcleanrows'] = len(df)
        the_file.write('** We have ' + str(sumstats['totalcleanrows']) +
              ' total rows of data to finish with.\n')
        sumstats['totalcleanvalue'] = round(df['amount'].sum()/ 1000000000, 2)
        the_file.write('** We have £' +
              str(sumstats['totalcleanvalue']) +
              'bn worth of data to finish with.\n')
        sumstats['totalcleanuniqsup'] = len(df['supplier_upper'].unique())
        the_file.write('** We have ' + str(sumstats['totalcleanuniqsup']) +
              ' unique suppliers to finish with.\n')
        sumstats['totalcleanuniqdept'] = len(df['dept'].unique())
        the_file.write('** We merge from across ' + str(sumstats['totalcleanuniqdept']) +
              ' departments.\n')
        sumstats['totalcleanuniqfiles'] = len(df['file'].unique())
        the_file.write('** This data comes from: ' +
              str(sumstats['totalcleanuniqfiles']) + ' files.\n')
    return df, sumstats
