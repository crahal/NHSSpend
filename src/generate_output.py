import pandas as pd
import os
import random
from reconciliation import normalizer


def load_chname(ch_path, norm_path):
    ch_name = pd.read_csv(os.path.join(ch_path, 'ch_uniq.csv'),
                          warn_bad_lines=False, error_bad_lines=False)
    norm_df = pd.read_csv(norm_path, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    ch_name['norm_name'] = ch_name['name'].\
                           apply(lambda x: normalizer(x, norm_dict))
    ch_name = ch_name.drop_duplicates(subset='norm_name', keep=False)
    return ch_name



def build_top_company_df(pay_df, Year, data_path, metric):
    ch_count = pay_df.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    ch_val = pay_df.groupby(['verif_match'])['amount'].sum().reset_index()
    ch_merge = pd.merge(ch_val, ch_count, how='left', on='verif_match')
    ch_path = os.path.join(data_path, 'data_ch')
    norm_path = os.path.join(data_path, 'data_support', 'norm_dict.tsv')
    ch_name = load_chname(ch_path, norm_path)
    ch_merge = pd.merge(ch_merge, ch_name, how='left',
                        left_on='verif_match',
                        right_on='norm_name')
    ch_merge['amount'] = ch_merge['amount'].astype(int)
    ch_merge['Value (%)'] = (ch_merge['amount']/ch_merge['amount'].sum())*100
    ch_merge['Count (%)'] = (ch_merge['count']/ch_merge['count'].sum())*100
    ch_merge = ch_merge.rename({'name': 'Company Name'}, axis=1)
    ch_merge = ch_merge[['Company Name' , 'Value (%)', 'Count (%)']]
    ch_merge['Company Name'] = ch_merge['Company Name'].str.strip()
    ch_merge = ch_merge[ch_merge['Company Name'].notnull()]
    ch_merge = ch_merge.sort_values(metric, ascending=False)[0:10]
    ch_merge = ch_merge.reset_index()
    ch_merge['Rank'] = ch_merge.index+1
    ch_merge= ch_merge.drop('index', 1)
    ch_merge = ch_merge.set_index('Company Name')
    ch_merge['Year'] = Year
    return ch_merge


def build_top_company_suppliers(pay_df, d_path, filename, metric):
    """ Who are the top company suppliers? """
    list_of_dfs = []
    ch_pay_df = pay_df[pay_df['match_type'].str.contains('Compan')]
    data_path = os.path.join(d_path, '..')
    list_of_dfs.append(build_top_company_df(ch_pay_df, 'All Years', data_path, metric))
    for year in range(2013,2020):
        temp_df = ch_pay_df[ch_pay_df['date'].astype(str).str.contains(str(year))]
        ret_df = build_top_company_df(temp_df, str(year), data_path, metric)
        list_of_dfs.append(ret_df)
    df = pd.concat(list_of_dfs)
    df.to_csv(os.path.join(d_path, filename))


def load_ccname(cc_path, norm_path):
    """ load and normalise a frozen variant of the chairty commission data """
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


def build_company_tables(pay_df, d_path, filename, orgtype):
    """ build company table for shapefile merge"""

    trust_list = pd.read_excel(os.path.join(d_path, '..', 'data_support',
                                            orgtype+'_list.xls'))
    if orgtype=='trust':
        varnames = ['trust name', 'NHS Trust', 'Latitude', 'Longitude']
        trust_list = trust_list[[varnames[0], 'abrev','Latitude', 'Longitude']]
    elif orgtype=='ccg':
        varnames = ['ccg19nm', 'NHS CCG']
        trust_list = trust_list[[varnames[0], 'abrev']]
    columns = ['Count', 'Value (m)',
               'Number of Datasets', 'Value (%)', 'Count (%)',
               'Highest Value Company Recipient']
    df = trust_list.reindex(trust_list.columns.tolist() + columns, axis=1)
    df = df[df['abrev'].notnull()]
    df = df.set_index('abrev')
    df['Highest Value Company Recipient'] = df['Highest Value Company Recipient'].astype(str)
    for index in df.index:
        temp_df = pay_df[pay_df['dept']==index]
        if len(temp_df)>0:
            temp_cc = temp_df[temp_df['match_type'].str.contains('Compan')]
            df.at[index, 'Count'] = len(temp_df)
            df.at[index, 'Value (m)'] = int(temp_df['amount'].sum()/1000000)
            df.at[index, 'Number of Datasets'] = len(temp_df['file'].unique())
            df.at[index, 'Number Payments to VCS'] = len(temp_cc)
            df.at[index, 'Value (%)'] = (temp_cc['amount'].sum()/
                                         temp_df['amount'].sum())*100
            df.at[index, 'Count (%)'] = (len(temp_cc)/len(temp_df))*100
            df.at[index, 'Number of Company Suppliers'] = len(temp_cc['verif_match'].unique())
            cc_val = temp_cc.groupby(['verif_match'])['amount'].sum().reset_index()
            try:
                most_cc = cc_val.sort_values(by='amount',
                                             ascending=False).reset_index()['verif_match'][0]
                df.at[index, 'Highest Value Company Recipient'] = most_cc
            except (KeyError, IndexError):
                df.at[index, 'Highest Value Company Recipient'] = 0
    df = df[df['Highest Value Company Recipient'].notnull()]
    df = df[df['Count'].notnull()]
    df.index = df.index.rename('NHS Abrev')
    df.index = df.index.str.replace('NHS_','')
    df.index = df.index.str.replace('_Trust','')
    df.index = df.index.str.replace('_CCG','')
    df.index = df.index.str.upper()
    df.to_csv(os.path.join(d_path, filename))


def build_charity_tables(pay_df, d_path, filename, orgtype):
    """ build charity tables for shapefile merge"""

    trust_list = pd.read_excel(os.path.join(d_path, '..', 'data_support',
                                            orgtype+'_list.xls'))
    if orgtype=='trust':
        varnames = ['trust name', 'NHS Trust', 'Latitude', 'Longitude']
        trust_list = trust_list[[varnames[0], 'abrev','Latitude', 'Longitude']]
    elif orgtype=='ccg':
        varnames = ['ccg19nm', 'NHS CCG']
        trust_list = trust_list[[varnames[0], 'abrev']]
    columns = ['Count', 'Value (m)',
               'Number of Datasets', 'Value (%)', 'Count (%)',
               'Highest Value Charity Recipient']
    df = trust_list.reindex(trust_list.columns.tolist() + columns, axis=1)
    df = df[df['abrev'].notnull()]
    df = df.set_index('abrev')
    df['Highest Value Charity Recipient'] = df['Highest Value Charity Recipient'].astype(str)
    for index in df.index:
        temp_df = pay_df[pay_df['dept']==index]
        if len(temp_df)>0:
            temp_cc = temp_df[temp_df['match_type'].str.contains('Charit')]
            df.at[index, 'Count'] = len(temp_df)
            df.at[index, 'Value (m)'] = int(temp_df['amount'].sum()/1000000)
            df.at[index, 'Number of Datasets'] = len(temp_df['file'].unique())
            df.at[index, 'Number Payments to VCS'] = len(temp_cc)
            df.at[index, 'Value (%)'] = (temp_cc['amount'].sum()/
                                         temp_df['amount'].sum())*100
            df.at[index, 'Count (%)'] = (len(temp_cc)/len(temp_df))*100
            df.at[index, 'Number of Charity Suppliers'] = len(temp_cc['verif_match'].unique())
            cc_val = temp_cc.groupby(['verif_match'])['amount'].sum().reset_index()
            try:
                most_cc = cc_val.sort_values(by='amount',
                                             ascending=False).reset_index()['verif_match'][0]
                df.at[index, 'Highest Value Charity Recipient'] = most_cc
            except (KeyError, IndexError):
                df.at[index, 'Highest Value Charity Recipient'] = 0
    df = df[df['Highest Value Charity Recipient'].notnull()]
    df = df[df['Count'].notnull()]
    df.index = df.index.rename('NHS Abrev')
    df.index = df.index.str.replace('NHS_','')
    df.index = df.index.str.replace('_Trust','')
    df.index = df.index.str.replace('_CCG','')
    df.index = df.index.str.upper()
    df.to_csv(os.path.join(d_path, filename))


def build_top_org_company_df(pay_df, cc_pay_df, Year, trust_list, varname, metric):
    cc_count = cc_pay_df.groupby(['dept'])['dept'].\
        count().reset_index(name="Company Count")
    total_count = pay_df.groupby(['dept'])['dept'].\
        count().reset_index(name="total_count")
    cc_val = cc_pay_df.groupby(['dept'])['amount'].sum().reset_index(name='Company Value')
    total_val = pay_df.groupby(['dept'])['amount'].sum().reset_index(name='total_amount')
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='dept')
    cc_merge = pd.merge(cc_merge, total_count, how='left', on='dept')
    cc_merge = pd.merge(cc_merge, total_val, how='left', on='dept')
    cc_merge['Count (%)'] = (cc_merge['Company Count']/cc_merge['total_count'])*100
    cc_merge['Value (%)'] = (cc_merge['Company Value']/cc_merge['total_amount'])*100
    cc_merge = cc_merge[cc_merge['total_count']>100]
    cc_merge = cc_merge.sort_values(metric, ascending=False)[0:10]
    cc_merge = cc_merge.reset_index()
    cc_merge['Rank'] = cc_merge.index+1
    cc_merge = cc_merge.rename({'dept': 'NHS Abrev'}, axis=1)
    cc_merge = cc_merge.set_index('NHS Abrev')
    cc_merge['Year'] = Year
    cc_merge = cc_merge.drop('index', 1)
    cc_merge = cc_merge.drop('total_count', 1)
    cc_merge = cc_merge.drop('total_amount', 1)
    cc_merge.index.names = ['NHS Abrev']
    cc_merge = pd.merge(cc_merge, trust_list, how='left', left_index=True, right_on='abrev')
    cc_merge = cc_merge.rename({'abrev': 'NHS Abrev'}, axis=1)
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('_CCG', '')
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('_', ' ')
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('NHS ', '')
    cc_merge = cc_merge.set_index('NHS Abrev')
    cc_merge = cc_merge.rename({varname[0]: varname[1]}, axis=1)
    return cc_merge


def build_top_org_charity_df(pay_df, cc_pay_df, Year, trust_list, varname, metric):
    cc_count = cc_pay_df.groupby(['dept'])['dept'].\
        count().reset_index(name="Charity Count")
    total_count = pay_df.groupby(['dept'])['dept'].\
        count().reset_index(name="total_count")
    cc_val = cc_pay_df.groupby(['dept'])['amount'].sum().reset_index(name='Charity Value')
    total_val = pay_df.groupby(['dept'])['amount'].sum().reset_index(name='total_amount')
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='dept')
    cc_merge = pd.merge(cc_merge, total_count, how='left', on='dept')
    cc_merge = pd.merge(cc_merge, total_val, how='left', on='dept')
    cc_merge['Count (%)'] = (cc_merge['Charity Count']/cc_merge['total_count'])*100
    cc_merge['Value (%)'] = (cc_merge['Charity Value']/cc_merge['total_amount'])*100
    cc_merge = cc_merge[cc_merge['total_count']>100]
    cc_merge = cc_merge.sort_values(metric, ascending=False)[0:10]
    cc_merge = cc_merge.reset_index()
    cc_merge['Rank'] = cc_merge.index+1
    cc_merge = cc_merge.rename({'dept': 'NHS Abrev'}, axis=1)
    cc_merge = cc_merge.set_index('NHS Abrev')
    cc_merge['Year'] = Year
    cc_merge = cc_merge.drop('index', 1)
    cc_merge = cc_merge.drop('total_count', 1)
    cc_merge = cc_merge.drop('total_amount', 1)
    cc_merge.index.names = ['NHS Abrev']
    cc_merge = pd.merge(cc_merge, trust_list, how='left', left_index=True, right_on='abrev')
    cc_merge = cc_merge.rename({'abrev': 'NHS Abrev'}, axis=1)
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('_CCG', '')
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('_', ' ')
    cc_merge['NHS Abrev'] = cc_merge['NHS Abrev'].str.replace('NHS ', '')
    cc_merge = cc_merge.set_index('NHS Abrev')
    cc_merge = cc_merge.rename({varname[0]: varname[1]}, axis=1)
    return cc_merge


def build_top_org_company_procurers(pay_df, d_path, filename, orgtype, metric):
    """ build top company procurers"""

    trust_list = pd.read_excel(os.path.join(d_path, '..', 'data_support', orgtype+'_list.xls'))
    if orgtype == 'trust':
        varnames = ['trust name', 'NHS Trust']
    elif orgtype == 'ccg':
        varnames = ['ccg19nm', 'NHS CCG']
    trust_list = trust_list[[varnames[0], 'abrev']]
#    cc_merge = pd.merge(cc_merge, trust_list, how='left', left_index=True, right_on='abrev')
    cc_pay_df = pay_df[pay_df['match_type'].str.contains('Compan')]
    list_of_dfs = []
    list_of_dfs.append(build_top_org_company_df(pay_df, cc_pay_df, 'All Years', trust_list, varnames, metric))
    for year in range(2013,2020):
        temp_df = pay_df[pay_df['date'].astype(str).str.contains(str(year))]
        temp_cc_df = cc_pay_df[cc_pay_df['date'].astype(str).str.contains(str(year))]
        ret_df = build_top_org_company_df(temp_df, temp_cc_df, str(year), trust_list, varnames, metric)
        list_of_dfs.append(ret_df)
    df = pd.concat(list_of_dfs)
    df.index = df.index.str.replace('NHS_','')
    df.index = df.index.str.replace('_CCG','')
    df.index = df.index.str.replace('_Trust','')
    df.index = df.index.str.replace('NHS ','')
    df.index = df.index.str.replace(' CCG','')
    df.index = df.index.str.replace(' Trust','')
    df.index = df.index.str.upper()
    df.to_csv(os.path.join(d_path, filename))


def build_top_org_charity_procurers(pay_df, d_path, filename, orgtype, metric):
    """ Which organisations procure most from charities?"""

    trust_list = pd.read_excel(os.path.join(d_path, '..',
                                            'data_support', orgtype+'_list.xls'))
    if orgtype=='trust':
        varnames = ['trust name', 'NHS Trust']
    elif orgtype=='ccg':
        varnames = ['ccg19nm', 'NHS CCG']
    trust_list = trust_list[[varnames[0], 'abrev']]
#    cc_merge = pd.merge(cc_merge, trust_list, how='left', left_index=True, right_on='abrev')
    cc_pay_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    list_of_dfs = []
    list_of_dfs.append(build_top_org_charity_df(pay_df, cc_pay_df, 'All Years', trust_list, varnames, metric))
    for year in range(2013,2020):
        temp_df = pay_df[pay_df['date'].astype(str).str.contains(str(year))]
        temp_cc_df = cc_pay_df[cc_pay_df['date'].astype(str).str.contains(str(year))]
        ret_df = build_top_org_charity_df(temp_df, temp_cc_df, str(year), trust_list, varnames, metric)
        list_of_dfs.append(ret_df)
    df = pd.concat(list_of_dfs)
    df.index = df.index.str.replace('NHS_','')
    df.index = df.index.str.replace('_CCG','')
    df.index = df.index.str.replace('_Trust','')
    df.index = df.index.str.replace('NHS ','')
    df.index = df.index.str.replace(' CCG','')
    df.index = df.index.str.replace(' Trust','')
    df.index = df.index.str.upper()
    df.to_csv(os.path.join(d_path, filename))


def build_top_charity_df(pay_df, Year, data_path, metric):
    cc_count = pay_df.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val = pay_df.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='verif_match')
    cc_path = os.path.join(data_path, 'data_cc')
    norm_path = os.path.join(data_path, 'data_support', 'norm_dict.tsv')
    cc_name = load_ccname(cc_path, norm_path)
    cc_merge = pd.merge(cc_merge, cc_name, how='left',
                        left_on='verif_match',
                        right_on='norm_name')
    cc_merge['Registration Number'] = pd.to_numeric(cc_merge['regno'],
                                      errors='coerce')
    cc_merge = cc_merge[cc_merge['Registration Number'].notnull()]
    cc_merge['Registration Number'] = cc_merge['Registration Number'].astype(int)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge['Value (%)'] = (cc_merge['amount']/cc_merge['amount'].sum())*100
    cc_merge['Count (%)'] = (cc_merge['count']/cc_merge['count'].sum())*100
    cc_merge = cc_merge.rename({'name': 'Charity Name'}, axis=1)
    cc_merge = cc_merge[['Charity Name' ,'Count (%)',
                         'Value (%)','Registration Number']]
    cc_merge['Charity Name'] = cc_merge['Charity Name'].str.strip()
    cc_merge = cc_merge[cc_merge['Charity Name'].notnull()]
    cc_merge = cc_merge.sort_values(metric, ascending=False)[0:10]
    cc_merge = cc_merge.reset_index()
    cc_merge['Rank'] = cc_merge.index+1
    cc_merge= cc_merge.drop('index', 1)
    cc_merge = cc_merge.set_index('Charity Name')
    cc_merge['Year'] = Year
    return cc_merge


def build_top_charity_suppliers(pay_df, d_path, filename, metric):
    """ Build the top charity suppliers for the dashboard """
    list_of_dfs = []
    cc_pay_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    data_path = os.path.join(d_path, '..')
    list_of_dfs.append(build_top_charity_df(cc_pay_df, 'All Years', data_path, metric))
    for year in range(2013,2020):
        temp_df = cc_pay_df[cc_pay_df['date'].astype(str).str.contains(str(year))]
        ret_df = build_top_charity_df(temp_df, str(year), data_path, metric)
        list_of_dfs.append(ret_df)
    df = pd.concat(list_of_dfs)
    df.to_csv(os.path.join(d_path, filename))




def transparency_score(num_files, days_last_trans, pc_pdfs, ease_scraping):
    return random.randint(1, 100)
    ''' generating the transparency score for the ccg'''


def output_for_dashboard(finalpath, dashboard, mergepath):
    """
    A simple function for building the output for the dashboard

    Parameters
    ----------
    first : file path
        the location of the final data
    second : file path
        the output location of the dashboard data
    Returns
    -------
    None
    """
#    generate_coverage_dashboard_dataset(mergepath, dashboard)
    ccg_pay_df = pd.read_csv(os.path.join(finalpath, 'payments_ccg_final.csv'),
                             index_col=0, low_memory=False)
    trust_pay_df = pd.read_csv(os.path.join(finalpath, 'payments_trust_final.csv'),
                               index_col=0, low_memory=False)

    build_top_charity_suppliers(ccg_pay_df, dashboard, 'ccg_top10_cc_byvalue.csv', 'Value (%)')
    build_top_charity_suppliers(trust_pay_df, dashboard, 'trust_top10_cc_byvalue.csv', 'Value (%)')
    build_top_charity_suppliers(ccg_pay_df, dashboard, 'ccg_top10_cc_bycount.csv', 'Count (%)')
    build_top_charity_suppliers(trust_pay_df, dashboard, 'trust_top10_cc_bycount.csv', 'Count (%)')

    build_top_org_charity_procurers(ccg_pay_df, dashboard, 'ccg_top10_orgs_cc_byvalue.csv', 'ccg', 'Value (%)')
    build_top_org_charity_procurers(trust_pay_df, dashboard, 'trust_top10_orgs_cc_byvalue.csv', 'trust', 'Value (%)')
    build_top_org_charity_procurers(ccg_pay_df, dashboard, 'ccg_top10_orgs_cc_bycount.csv', 'ccg', 'Count (%)')
    build_top_org_charity_procurers(trust_pay_df, dashboard, 'trust_top10_orgs_cc_bycount.csv', 'trust', 'Count (%)')

    build_top_org_company_procurers(ccg_pay_df, dashboard, 'ccg_top10_orgs_ch_byvalue.csv', 'ccg', 'Value (%)')
    build_top_org_company_procurers(trust_pay_df, dashboard, 'trust_top10_orgs_ch_byvalue.csv', 'trust', 'Value (%)')
    build_top_org_company_procurers(ccg_pay_df, dashboard, 'ccg_top10_orgs_ch_bycount.csv', 'ccg', 'Count (%)')
    build_top_org_company_procurers(trust_pay_df, dashboard, 'trust_top10_orgs_ch_bycount.csv', 'trust', 'Count (%)')

    build_top_company_suppliers(ccg_pay_df, dashboard,  'ccg_top10_ch_byvalue.csv', 'Value (%)')
    build_top_company_suppliers(trust_pay_df, dashboard, 'trust_top10_ch_byvalue.csv', 'Value (%)')
    build_top_company_suppliers(ccg_pay_df, dashboard, 'ccg_top10_ch_bycount.csv', 'Count (%)')
    build_top_company_suppliers(trust_pay_df, dashboard, 'trust_top10_ch_bycount.csv', 'Count (%)')

    build_charity_tables(ccg_pay_df, dashboard, 'ccg_table_cc.csv', 'ccg')
    build_charity_tables(trust_pay_df, dashboard, 'trust_table_cc.csv', 'trust')

    build_company_tables(ccg_pay_df, dashboard, 'ccg_table_ch.csv', 'ccg')
    build_company_tables(trust_pay_df, dashboard, 'trust_table_ch.csv', 'trust')


def generate_coverage_dashboard_dataset(mergepath, dashboard):
    df = pd.read_csv(os.path.join(mergepath, 'merged_clean_spending.tsv'),
                     index_col=None, encoding='latin-1', engine='python',
                     sep='\t', error_bad_lines=False,
                     dtype={'transactionnumber': str, 'amount': float,
                            'supplier': str, 'date': str, 'file': str,
                            'expensearea': str, 'expensetype': str})
    coverage_df = pd.DataFrame(index=df['dept'].unique(),
                               columns=['Number_Payments',
                                        'Payment_Value', 'Number_Files',
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
