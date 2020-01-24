import glob
import os
import numpy as np
import pandas as pd
import ntpath
from unidecode import unidecode
import json
from datetime import datetime
from yattag import Doc, indent
from reconciliation import normalizer
from Levenshtein import distance


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
        result = indent(doc.getvalue(), indent_text=True)
        with open(outpath, "w") as file:
            file.write(result)


def merge_eval_scrape(cleanpath, mergepath, htmlpath,
                      datasummarypath, logpath):
    json_path = os.path.join(datasummarypath, 'scrape_and_parse_summary.json')
    merged_df = merge_files(cleanpath, mergepath)
    merged_df, sumstats = evaluate_and_clean_merge(merged_df, logpath)
    create_html_from_sumstats(htmlpath, sumstats)
    merged_df.to_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
                     encoding='latin-1', sep='\t')
    sup_count = pd.DataFrame(merged_df.groupby('supplier')['supplier'].
                             count()).rename({'supplier': 'num_pay'}, axis=1)
    sup_value = pd.DataFrame(merged_df.groupby('supplier')['amount'].
                             sum()).rename({'amount': 'tot_pay_val'}, axis=1)
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
    frame['transactionnumber'] = frame['transactionnumber'].str.\
        replace('[^\w\s]', '')
    frame['transactionnumber'] = frame['transactionnumber'].str.strip("0")
    return frame


def evaluate_and_clean_merge(df, logpath):
    sumstats = {}
    with open(os.path.join(logpath, 'eval_logs', 'clean',
                           datetime.now().strftime('Eval_clean_%Y_%m_%d') +
                           '.txt'), 'w') as the_file:
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
        the_file.write('Dropped £' + str(sumstats['droppedbelow25kvalue']) +
                       'bn null, non-numeric, <£25k, total summed value.\n')
        initial = df
        df = df[~pd.isnull(df['supplier'])]
        df['supplier'] = df['supplier'].str.replace('\n', ' ')
        df['supplier'] = df['supplier'].str.replace('\r', ' ')
        df['supplier'] = df['supplier'].str.replace('\t', ' ')
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
                                               df['amount'].sum()) /
                                               1000000, 2)
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
                       str(round(sumstats['droppedvariousamount'] /
                                 1000000, 2)) + 'm.\n')
        sumstats['uniquesupvarious'] = (len(initial['supplier'].unique()) -
                                        len(df['supplier'].unique()))
        the_file.write('We identified ' + str(sumstats['uniquesupvarious']) +
                       ' unique "various" supplier strings.\n')
        initial = df
        df['supplier'] = df['supplier'].str.replace('\t', '')
        df['supplier'] = df['supplier'].str.replace('\n', '')
        df['supplier'] = df['supplier'].str.replace('\r', '')
        df['supplier'] = df['supplier'].apply(
            lambda x: unidecode(x))
        df['supplier'] = df['supplier'].str.strip().str.upper()
        cols_to_consider = ['amount', 'date', 'dept', 'expensearea',
                            'expensetype', 'transactionnumber', 'supplier']
        df = df.drop_duplicates(subset=cols_to_consider, keep='first')
        sumstats['dropduplicrows'] = len(initial) - len(df)
        the_file.write('Dropped ' + str(sumstats['dropduplicrows']) +
                       ' potential duplicates\n')
        sumstats['suppliers_are_numbers'] = \
            len(df[df.supplier.str.isnumeric()])
        df = df[~df.supplier.str.isnumeric()]
        the_file.write('Dropped ' + str(sumstats['suppliers_are_numbers']) +
                       ' suppliers who have numbers in the name column.\n')
        sumstats['dropduplicvalue'] = round((initial['amount'].sum() -
                                             df['amount'].sum()) /
                                            1000000000, 2)
        the_file.write('Dropped duplicates worth £' +
                       str(sumstats['dropduplicvalue']) + 'bn.\n')
        sumstats['totalcleanrows'] = len(df)
        the_file.write('** We have ' + str(sumstats['totalcleanrows']) +
                       ' total rows of data to finish with.\n')
        sumstats['totalcleanvalue'] = round(df['amount'].sum() /
                                            1000000000, 2)
        the_file.write('** We have £' + str(sumstats['totalcleanvalue']) +
                       'bn worth of data to finish with.\n')
        sumstats['totalcleanuniqsup'] = len(df['supplier'].unique())
        the_file.write('** We have ' + str(sumstats['totalcleanuniqsup']) +
                       ' unique suppliers to finish with.\n')
        sumstats['totalcleanuniqdept'] = len(df['dept'].unique())
        the_file.write('** We merge from across ' +
                       str(sumstats['totalcleanuniqdept']) +
                       ' departments.\n')
        sumstats['totalcleanuniqfiles'] = len(df['file'].unique())
        the_file.write('** This data comes from: ' +
                       str(sumstats['totalcleanuniqfiles']) + ' files.\n')
    return df, sumstats


def dist_func(x, y):
    try:
        query_dist = distance(x, y)
    except TypeError:
        query_dist = np.nan
    return query_dist


def build_reconciled_df(recon_path, norm_path):
    raw = pd.read_csv(os.path.join(recon_path, 'general_matches.csv'),
                      dtype={'query_string': str})
    norm = pd.read_csv(os.path.join(recon_path, 'general_norm_matches.csv'),
                       dtype={'query_string_n': str})
    norm.columns = [str(col) + '_n' for col in norm.columns]
    norm_df = pd.read_csv(norm_path, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    raw['query_string_n'] = raw['query_string'].apply(lambda x:
                                                      normalizer(x, norm_dict))
    recon = pd.merge(raw, norm, how='left', on='query_string_n')
    for column in range(0, 5):
        lev = 'match_' + str(column) + '_lev'
        lev_n = 'match_' + str(column) + '_n_lev'
        recon[lev] = recon.apply(lambda x: dist_func(x['query_string'],
                                 x['match_' + str(column)]), axis=1)
        recon[lev_n] = recon.apply(lambda x: dist_func(x['query_string_n'],
                                                       x['match_' +
                                                         str(column) +
                                                         '_n']), axis=1)
    return recon.sort_values(by='match_0_n_lev', ascending=True)


def clean_recon(recon_df, ch_set, cc_set, nhs_set, max_len=3):
    recon_df['match_type'] = 'No Type'
    for index, row in recon_df.iterrows():
        typelist = ''
        if (row['query_string_n'].startswith('DR ')) or \
           (row['query_string_n'].startswith('DRS ')):
            recon_df.at[index, 'verif_match'] = 'Named Doctor'
            typelist = typelist + 'Named Doctor: '
        elif (row['query_string_n'].startswith('MR ')) or \
             (row['query_string_n'].startswith('MRS ')) or \
             (row['query_string_n'].startswith('MISS ')):
            recon_df.at[index, 'verif_match'] = 'Named Person'
            typelist = typelist + 'Named Person: '
        if len(row['query_string_n']) < max_len:
            recon_df.at[index, 'verif_match'] = 'No Match'
        if isinstance(row['match_0_n'], float):
            recon_df.at[index, 'verif_match'] = 'No Match'
        if (recon_df.at[index, 'verif_match'] in ch_set):
            typelist = typelist + 'Companies House: '
        if (recon_df.at[index, 'verif_match'] in cc_set):
            typelist = typelist + 'Charity Commission: '
        if (recon_df.at[index, 'verif_match'] in nhs_set):
            typelist = typelist + 'NHS Digital: '
        if typelist.endswith(': '):
            typelist = typelist[:-2].strip()
        elif typelist == '':
            typelist = 'No Match'
        recon_df.at[index, 'match_type'] = typelist
    return recon_df


def merge_matches_with_payments(clean_matches, raw_payments, mergepath):
    merged_df = pd.merge(raw_payments, clean_matches, how='left',
                         left_on='supplier', right_on='query_string')
    merged_df.to_csv(os.path.join(mergepath, 'merged_with_recon.tsv'),
                     sep='\t')
    return merged_df


def evaluate_recon(clean_matches, logpath, filename):
    sumstats = {}
    filename = datetime.now().strftime(filename + '_%Y_%m_%d') + '.txt'
    filepath = os.path.join(logpath, 'eval_logs', 'recon', filename)
    with open(os.path.join(filepath), 'w') as the_file:
        the_file.write('** Evaluating the reconciliation!**\n\n')
        sumstats['num_supps'] = len(clean_matches)
        the_file.write(str(sumstats['num_supps']) + ' entities to reconcile\n')
        sumstats['num_drs'] = \
            len(clean_matches[clean_matches['verif_match'] ==
                'Named Doctor'])
        sumstats['num_namedpeople'] = \
            len(clean_matches[clean_matches['verif_match'] ==
                'Named Person'])
        the_file.write(str(sumstats['num_drs']) + ' named people who arent doctors\n')
        sumstats['no_match'] = \
            len(clean_matches[clean_matches['verif_match'].isnull()])
        the_file.write(str(sumstats['no_match']) + ' have no match\n\n')
        the_file.write('Traversing the Levenshtein Distances!\n\n')
        for dist in range(0, 20):
            the_file.write('Matches with Levenshtein distance ' +
                           str(dist) + ' or less:\n')
            temp_df = clean_matches[clean_matches['clean_lev'] <= dist]
            temp_df = temp_df[temp_df['verif_match'] != 'Named Doctor']
            temp_df = temp_df[temp_df['verif_match'] != 'Named Person']
            sumstats['leven_' + str(dist) + '_matches'] = len(temp_df)
            the_file.write('Matches with: ' +
                           str(sumstats['leven_' + str(dist) + '_matches']) +
                           '\n')
            sumstats['leven_' + str(dist) + '_nhs'] = \
                len(temp_df[temp_df['match_type'].str.contains('NHS')])
            the_file.write('Matches to NHS Digital: ' +
                           str(sumstats['leven_' + str(dist) + '_nhs']) + '\n')
            sumstats['leven_' + str(dist) + '_ch'] = \
                len(temp_df[temp_df['match_type'].str.contains('Companies')])
            the_file.write('Matches to Companies House: ' +
                           str(sumstats['leven_' + str(dist) + '_ch']) + '\n')
            sumstats['leven_' + str(dist) + '_cc'] = \
                len(temp_df[temp_df['match_type'].str.contains('Charity')])
            the_file.write('Matches to Charity Commission: ' +
                           str(sumstats['leven_' + str(dist) + '_cc']) + '\n')
            the_file.write('\n')


def gen_df_for_verification(verif_df, recon_path):
    unverif_df = verif_df[verif_df['verif_match'].isnull()]
    unverified = len(unverif_df)
    print(f'{unverified} unverified rows in suppliers dataset')
    unverif_df =  unverif_df.drop_duplicates(subset=['query_string_n'])
    unverified = len(unverif_df)
    print(f'{unverified} unverified normalized entries in suppliers dataset')
    save = ['query_string_n', 'match_0_n', 'match_0_n_lev',
            'match_1_n', 'match_1_n_lev', 'match_2_n', 'match_2_n_lev',
            'match_3_n', 'match_3_n_lev', 'match_4_n', 'match_4_n_lev']
    unverif_df[save].to_csv(os.path.join(recon_path, 'recon_unverified.tsv'),
                            sep='\t', index=False)


def merge_eval_recon(recon_path, norm_path, data_path, mergepath, logpath):
    recon_short = build_reconciled_df(recon_path, norm_path)
    ch_df = pd.read_csv(os.path.join(data_path, 'data_ch', 'ch_uniq_norm.csv'))
    ch_set = set(ch_df['name_norm'].tolist())
    ch_set = set(filter(lambda x: x == x, ch_set))
    cc_df = pd.read_csv(os.path.join(data_path, 'data_cc', 'cc_uniq_norm.csv'))
    cc_set = set(cc_df['name_norm'].tolist())
    cc_set = set(filter(lambda x: x == x, cc_set))
    nhs_df = pd.read_csv(os.path.join(data_path, 'data_nhsdigital',
                                      'nhs_uniq_norm.csv'))
    nhs_set = set(nhs_df['name_norm'].tolist())
    nhs_set = set(filter(lambda x: x == x, nhs_set))
    verif_df = pd.read_csv(os.path.join(data_path, 'data_support',
                                        'verif_df.csv'), sep=',')
    diffs = len(verif_df) - len(verif_df['query_string_n'].unique())
    if diffs > 0:
        print(f'Danger! There are {diffs} duplicates in our manual verification file!')
    verif_df = pd.merge(recon_short, verif_df, how='left',
                        left_on='query_string_n', right_on='query_string_n')
    verif_df = clean_recon(verif_df, ch_set, cc_set, nhs_set)
    verif_df['clean_lev'] = verif_df.\
        apply(lambda x: dist_func(x['query_string_n'], x['verif_match']),
              axis=1)
    verif_df['clean_lev'] = np.where(verif_df['verif_match'] == 'Named Doctor',
                                     np.nan, verif_df['clean_lev'])
    verif_df['clean_lev'] = np.where(verif_df['verif_match'] == 'Named Person',
                                     np.nan, verif_df['clean_lev'])
    verif_df['clean_lev'] = np.where(verif_df['verif_match'] == 'No Match',
                                     np.nan, verif_df['clean_lev'])
    verif_df.to_csv(os.path.join(recon_path, 'recon_verified.tsv'),
                    sep='\t', index=False)
    evaluate_recon(verif_df, logpath, 'manual_verification')
    totalrows = len(verif_df)
    print(f'{totalrows} total rows of supplier data to match.')
    totalmatched = len(verif_df[verif_df['verif_match'].notnull()])
    print(f'{totalmatched} rows of matched supplier data.')
    gen_df_for_verification(verif_df, recon_path)
    raw_payments = pd.read_csv(os.path.join(mergepath,
                                            'merged_clean_spending.tsv'),
                               index_col=None, encoding='latin-1', sep='\t',
                               engine='python', error_bad_lines=False,
                               dtype={'transactionnumber': str, 'date': str,
                                      'amount': float, 'supplier': str,
                                      'file': str, 'expensearea': str,
                                      'expensetype': str})
    merge_matches_with_payments(verif_df[['query_string',
                                          'query_string_n',
                                          'verif_match',
                                          'match_type']],
                                raw_payments, mergepath)
