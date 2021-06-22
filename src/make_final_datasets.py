import pandas as pd
import os
import numpy as np
from reconciliation import normalizer


def build_in_audit(df, audit_df):
    def get_audit_matchtype(row):
        """ Harmonize the matchtypes in the audit file"""
        if (row['isCharity'] == '1 charity') and (row['isCompany'] == '1 company') and (
                row['isNHS'] == '1 NHS or assoc'):
            match_type = 'Companies House: Charity Commission: NHS Digital'
        elif (row['isCharity'] == '1 charity') and (row['isCompany'] == '1 company') and (
                row['isNHS'] != '1 NHS or assoc'):
            match_type = 'Companies House: Charity Commission'
        elif (row['isCharity'] != '1 charity') and (row['isCompany'] == '1 company') and (
                row['isNHS'] == '1 NHS or assoc'):
            match_type = 'Companies House: NHS Digital'
        elif (row['isCharity'] == '1 charity') and (row['isCompany'] != '1 company') and (
                row['isNHS'] == '1 NHS or assoc'):
            match_type = 'Charity Commission: NHS Digital'
        elif (row['isCharity'] == '1 charity') and (row['isCompany'] != '1 company') and (
                row['isNHS'] != '1 NHS or assoc'):
            match_type = 'Charity Commission'
        elif (row['isCharity'] != '1 charity') and (row['isCompany'] == '1 company') and (
                row['isNHS'] != '1 NHS or assoc'):
            match_type = 'Companies House'
        elif (row['isCharity'] != '1 charity') and (row['isCompany'] != '1 company') and (
                row['isNHS'] == '1 NHS or assoc'):
            match_type = 'NHS Digital'
        else:
            match_type = 'No Match'
        return match_type

    df['audit_type'] = '1'
    df['CHnotes'] = np.nan
    df['CCnotes'] = np.nan
    df['isCIC'] = np.nan
    audit_df['charityregno'] = audit_df['charityregno'].astype(str)
    audit_df['companynumber'] = audit_df['companynumber'].astype(str)

    for index, row in audit_df.iterrows():
        if ((row['isCharity'] == '1 charity') and (row['isCompany'] == '1 company')):
            df['CharityName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         row['charregname_n'], df['CharityName'])
            df['CharityRegNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          row['charityregno'], df['CharityRegNo'])
            df['CharitySubNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          row['charitysubno'], df['CharitySubNo'])
            df['CharitySubNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          row['charitysubno'], df['CharitySubNo'])
            df['CompanyName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         row['companyname_n'], df['CompanyName'])
            df['CHnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CHnotes'], df['CHnotes'])
            df['CCnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CCnotes'], df['CCnotes'])
            audit_type = '2: CC: ' + row['matchcodeCC'] + ', CH: ' + row['matchcodeCH']
        elif (row['isCharity'] == '1 charity') and (row['isCompany'] != '1 company'):
            df['CharityName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         row['charregname_n'], df['CharityName'])
            df['CharityRegNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          row['charityregno'], df['CharityRegNo'])
            df['CharitySubNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          row['charitysubno'], df['CharitySubNo'])
            df['CompanyName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         np.nan, df['CompanyName'])
            df['CompanyNumber'] = np.where(df['query_string_n'] == row['query_string_n'],
                                           np.nan, df['CompanyNumber'])
            df['CCnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CCnotes'], df['CCnotes'])
            df['CHnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CHnotes'], df['CHnotes'])
            audit_type = '2: CC: ' + row['matchcodeCC']
        elif (row['isCharity'] != '1 charity') and (row['isCompany'] == '1 company'):
            df['CharityName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         np.nan, df['CharityName'])
            df['CharityRegNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          np.nan, df['CharityRegNo'])
            df['CharitySubNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          np.nan, df['CharitySubNo'])
            df['CharityNameNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                           np.nan, df['CharityNameNo'])
            df['CompanyName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         row['companyname'], df['CompanyName'])
            df['CompanyNumber'] = np.where(df['query_string_n'] == row['query_string_n'],
                                           row['companynumber'], df['CompanyNumber'])
            df['CHnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CHnotes'], df['CHnotes'])
            audit_type = '2: CH: ' + row['matchcodeCH']
        else:
            df['CharityName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         np.nan, df['CharityName'])
            df['CharityRegNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          np.nan, df['CharityRegNo'])
            df['CharitySubNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                          np.nan, df['CharitySubNo'])
            df['CharityNameNo'] = np.where(df['query_string_n'] == row['query_string_n'],
                                           np.nan, df['CharityNameNo'])
            df['CompanyName'] = np.where(df['query_string_n'] == row['query_string_n'],
                                         np.nan, df['CompanyName'])
            df['CompanyNumber'] = np.where(df['query_string_n'] == row['query_string_n'],
                                           np.nan, df['CompanyNumber'])
            df['CCnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CCnotes'], df['CCnotes'])
            df['CHnotes'] = np.where(df['query_string_n'] == row['query_string_n'],
                                     row['CHnotes'], df['CHnotes'])
            audit_type = '2: No Matches'
        match_type = get_audit_matchtype(row)
        df['match_type'] = np.where(df['query_string_n'] == row['query_string_n'],
                                    match_type, df['match_type'])
        df['audit_type'] = np.where(df['query_string_n'] == row['query_string_n'],
                                    audit_type, df['audit_type'])
        df['isCIC'] = np.where(df['query_string_n'] == row['query_string_n'],
                               row['isCIC'], df['isCIC'])
        df = df.replace(['nan', 'None'], np.nan)
    return df


def load_payments(pay_path):
    pay_df = pd.read_csv(pay_path, sep='\t',
#                         usecols=['expensetype', 'supplier', 'date', 'dept',
#                                  'amount', 'file', 'expensearea',
#                                  'transactionnumber', 'verif_match',
#                                  'query_string_n',
#                                  'match_type'],
#                         dtype={'query_string_n': str,
#                                'verif_match': str,
#                                'match_type': str,
#                                'transactionnumber': str},
                         parse_dates=['date'])
    pay_df = pay_df[pay_df['dept'] != 'NHS_RED_CCG']
    pay_df = pay_df[pay_df['dept'] != 'NHS_HAV_CCG']
    return pay_df


def load_ccname(cc_path, norm_path):
    """Load CC data for analysis"""
    ex_char = pd.read_csv(os.path.join(cc_path, 'extract_charity.csv'),
                             warn_bad_lines=False, error_bad_lines=False)
    cc_name = pd.read_csv(os.path.join(cc_path, 'extract_name.csv'),
                          warn_bad_lines=False, error_bad_lines=False)
    cc_regdate = pd.read_csv(os.path.join(cc_path,
                                          'extract_registration.csv'),
                             parse_dates=['regdate', 'remdate'],
                             warn_bad_lines=False, error_bad_lines=False)
    cc_name = pd.merge(cc_name, cc_regdate, how='left',
                       left_on=['regno', 'subno'],
                       right_on=['regno', 'subno'])
    norm_df = pd.read_csv(norm_path, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    cc_name['norm_name'] = cc_name['name'].\
                           apply(lambda x: normalizer(x, norm_dict))
    cc_name = cc_name[(cc_name['remdate'].dt.year > 2010) |
                      (cc_name['remdate'].isnull())]
    cc_name = cc_name.drop_duplicates(['norm_name', 'regno'], keep='first')
    cc_name = cc_name.drop_duplicates(['norm_name', 'remdate'], keep=False)
    cc_name = cc_name.sort_values('remdate').drop_duplicates('norm_name',
                                                             keep='last')
    cc_name = cc_name.drop_duplicates(subset='norm_name', keep=False)
    # note a lot of duplicates here to report on
    return cc_name


def load_ch_name(ch_path, norm_path):
    ch_df = pd.read_csv(os.path.join(ch_path,
                                     'BasicCompanyDataAsOneFile-2020-03-01.csv'),
                        usecols=['CompanyName', ' CompanyNumber',
                                 'CompanyCategory'])
    norm_df = pd.read_csv(norm_path, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    ch_df['company_norm'] = ch_df['CompanyName'].apply(lambda x:
                                                       normalizer(x, norm_dict))
    ch_df = ch_df.drop_duplicates(subset=['company_norm'], keep=False)
    return ch_df


def make_final_dfs(in_df, audit_df, cc_name, ch_name, out_path, filename):
    print('Working on building ' + str(filename))
    out_df = pd.merge(in_df, ch_name, how='left',
                      left_on='verif_match', right_on='company_norm')
    out_df = pd.merge(out_df, cc_name[['norm_name', 'regno',
                                       'subno', 'nameno', 'name']],
                      how='left', left_on='verif_match', right_on='norm_name')
    out_df = out_df.rename({' CompanyNumber': 'CompanyNumber'}, axis=1)
    out_df = out_df.rename({'regno': 'CharityRegNo'}, axis=1)
    out_df = out_df.rename({'nameno': 'CharityNameNo'}, axis=1)
    out_df = out_df.rename({'subno': 'CharitySubNo'}, axis=1)
    out_df = out_df.rename({'name': 'CharityName'}, axis=1)
    out_df = out_df.drop('company_norm', axis=1)
    out_df = out_df.drop('norm_name', axis=1)
    out_df = build_in_audit(out_df, audit_df)
    out_df.to_csv(os.path.join(out_path, filename))
    return out_df

def load_audit(data_path, audit_file):
    audit_df = pd.read_excel(os.path.join(data_path, audit_file))
    norm_file = os.path.join(data_path, 'norm_dict.tsv')
    norm_df = pd.read_csv(norm_file, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    audit_df['query_string_n'] = audit_df['supplier'].apply(lambda x: normalizer(x, norm_dict))
    audit_df['charregname_n'] = audit_df['charregname'].apply(lambda x: normalizer(x, norm_dict))
    audit_df['companyname_n'] = audit_df['companyname'].apply(lambda x: normalizer(x, norm_dict))
    return audit_df


def make_groupby_types(df, recon_df, sup_type, data_path, filename):
    print('Working on building the ' + sup_type + ' dataset.')
    df = df[df['match_type'].str.contains(sup_type)]
    if sup_type == 'Charity':
        df_count = df.groupby(['query_string_n'])['amount'].count()
        df_count = df_count.reset_index().rename({'amount': 'count'}, axis=1)
        df_amount = df.groupby(['query_string_n'])['amount'].sum().reset_index()
        merged_df = pd.merge(df_count, df_amount,
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
        merged_df = pd.merge(merged_df,
                             df[['CharityRegNo', 'CharityName', 'audit_type',
                                 'CCnotes', 'query_string_n']].drop_duplicates(subset=['query_string_n']),
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
    elif sup_type == 'Companies':
        df_count = df.groupby(['query_string_n'])['amount'].count()
        df_count = df_count.reset_index().rename({'amount': 'count'}, axis=1)
        df_amount = df.groupby(['query_string_n'])['amount'].sum().reset_index()
        merged_df = pd.merge(df_count, df_amount,
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
        merged_df = pd.merge(merged_df,
                             df[['CompanyNumber', 'CompanyName',
                                 'audit_type', 'CHnotes', 'isCIC',
                                 'query_string_n']].drop_duplicates(subset=['query_string_n']),
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
    else:
        df_count = df.groupby(['query_string_n'])['amount'].count()
        df_count = df_count.reset_index().rename({'amount': 'count'}, axis=1)
        df_amount = df.groupby(['query_string_n'])['amount'].sum().reset_index()
        merged_df = pd.merge(df_count, df_amount,
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
        merged_df = pd.merge(merged_df,
                             df[['verif_match', 'audit_type',
                                 'query_string_n']].drop_duplicates(subset=['query_string_n']),
                             left_on='query_string_n', right_on='query_string_n',
                             how='left')
    merged_df = pd.merge(merged_df, recon_df, how='left',
                         left_on='query_string_n', right_on = 'query_string_n')
    merged_df.to_csv(os.path.join(data_path, 'data_final', filename))


def make_final_datasets():
    """A main function to make the final datasets for the repo"""

    data_path = os.path.join(os.getcwd(), '..', 'data')
    cc_path = os.path.join(data_path, 'data_cc')
    ch_path = os.path.join(data_path, 'data_ch')
    support_path = os.path.join(data_path, 'data_support')
    norm_path = os.path.join(data_path, 'data_support', 'norm_dict.tsv')
    # load and cc/ch
    cc_name = load_ccname(cc_path, norm_path)
    ch_name = load_ch_name(ch_path, norm_path)
    #load and clean audit
    audit_df = load_audit(support_path, 'audit_v3.xlsx')
    # make trust
    trust_pay_path = os.path.join(data_path, 'data_merge', 'trust_merged_with_recon.tsv')
    trust_pay_df = load_payments(trust_pay_path)
    payments_trust_final = make_final_dfs(trust_pay_df, audit_df, cc_name, ch_name,
                                          os.path.join(data_path, 'data_final'),
                                          'payments_trust_final.csv')
    # make ccg
    ccg_pay_path = os.path.join(data_path, 'data_merge', 'ccg_merged_with_recon.tsv')
    ccg_pay_df = load_payments(ccg_pay_path)
    payments_ccg_final = make_final_dfs(ccg_pay_df, audit_df, cc_name, ch_name,
                                        os.path.join(data_path, 'data_final'),
                                        'payments_ccg_final.csv')
    #make nhsengland
    nhsengland_pay_path = os.path.join(data_path, 'data_merge', 'nhsengland_merged_with_recon.tsv')
    nhsengland_pay_df = load_payments(nhsengland_pay_path)
    payments_nhsengland_final = make_final_dfs(nhsengland_pay_df, audit_df, cc_name, ch_name,
                                               os.path.join(data_path, 'data_final'),
                                               'payments_nhsengland_final.csv')

    comb_df = pd.concat([payments_ccg_final, payments_trust_final, payments_nhsengland_final])
    comb_df.to_csv(os.path.join(data_path, 'data_final', 'payments_all.csv'))

    recon_df = pd.read_csv(os.path.join(data_path, 'data_reconciled', 'recon_verified.tsv'), sep='\t',
                           usecols=['query_string_n', 'match_0_n', 'match_1_n', 'match_2_n',
                                    'score_0_n', 'score_1_n', 'score_2_n', 'match_0_n_lev',
                                    'match_1_n_lev', 'match_2_n_lev'])
    comb_df = pd.read_csv(os.path.join(data_path, 'data_final', 'payments_all.csv'))
    make_groupby_types(comb_df, recon_df, 'Charity', data_path, 'supplier_charity_final.csv')
    make_groupby_types(comb_df, recon_df, 'Companies', data_path, 'supplier_company_final.csv')
    make_groupby_types(comb_df, recon_df, 'NHS', data_path, 'supplier_nhsdigital_final.csv')
    make_groupby_types(comb_df, recon_df, 'Doctor', data_path, 'supplier_nameddoctor_final.csv')
    make_groupby_types(comb_df, recon_df, 'Person', data_path, 'supplier_namedperson_final.csv')
    make_groupby_types(comb_df, recon_df, 'No Match', data_path, 'supplier_nomatch_final.csv')


