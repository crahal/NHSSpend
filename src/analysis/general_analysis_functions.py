import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import matplotlib.ticker as ticker
import matplotlib as mpl
import string
import os
from matplotlib_venn import venn3, venn3_circles
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
#np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25
mpl.rc('font', family='sans-serif')
mpl.rc('text', usetex='false')
#matplotlib.rcParams.update({'font.size': 20})


#def make_dfs_for_coauthors(ccg_pay_df, trust_pay_df, nhsengland_pay_df,
#                           cc_name, merge_path, ch_path, data_path):
#    """
#    Deprecated, moved into main NHSSpend.py with
#    outputs going into data_final
#    """
#    def make_df(in_df, ch_df, cc_name, out_path):
#        out_df = pd.merge(in_df, ch_df, how='left',
#                          left_on='verif_match', right_on='company_norm')
#        out_df = pd.merge(out_df, cc_name[['norm_name', 'regno',
#                                           'subno', 'nameno', 'name']],
#                          how='left', left_on='verif_match', right_on='norm_name')
#        out_df = out_df.rename({' CompanyNumber': 'CompanyNumber'}, axis=1)
#        out_df = out_df.rename({'regno': 'CharityRegNo'}, axis=1)
#        out_df = out_df.rename({'nameno': 'CharityNameNo'}, axis=1)
#        out_df = out_df.rename({'subno': 'CharitySubNo'}, axis=1)
#        out_df = out_df.rename({'name': 'CharityName'}, axis=1)
#        out_df = out_df.drop('company_norm', axis=1)
#        out_df = out_df.drop('norm_name', axis=1)
#        out_df.to_csv(os.path.join(out_path))
#        return out_df
#
#    ch_df = pd.read_csv(os.path.join(ch_path, 'BasicCompanyDataAsOneFile-2020-03-01.csv'),
#                        usecols=['CompanyName', ' CompanyNumber',
#                                 'CompanyCategory'])
#    norm_file = os.path.join(data_path, 'data_support', 'norm_dict.tsv')
#    norm_df = pd.read_csv(norm_file, sep='\t')
#    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
#    ch_df['company_norm'] = ch_df['CompanyName'].apply(lambda x:
#                                                       normalizer(x, norm_dict))
#    ch_df = ch_df.drop_duplicates(subset=['company_norm'], keep=False)
#    make_df(ccg_pay_df, ch_df, norm_df,
#            os.path.join(merge_path, 'ccg_for_coauthors.csv'))
#    make_df(trust_pay_df, ch_df, norm_df,
#            os.path.join(merge_path, 'trust_for_coauthors.csv'))
#    make_df(nhsengland_pay_df, ch_df, norm_df,
#            os.path.join(merge_path, 'nhsengland_for_coauthors.csv'))
#    merged_coauth = make_df(pd.concat([ccg_pay_df, trust_pay_df, nhsengland_pay_df]), ch_df, norm_df,
#                            os.path.join(merge_path, 'concatenateddata_for_coauthors.csv'))
#    merged_coauth = merged_coauth[merged_coauth['match_type'].str.contains('Chari')]
#    merged_coauth = merged_coauth.drop_duplicates(subset=['supplier'], keep='first')
#    merged_coauth = merged_coauth[['supplier', 'query_string_n', 'verif_match',
#                                   'match_type', 'CompanyName', 'CompanyNumber',
#                                   'CharityRegNo','CharitySubNo',
#                                   'CharityNameNo', 'CharityName']]
#    comb_pay_df = pd.concat([ccg_pay_df, trust_pay_df, nhsengland_pay_df])
#    comb_pay_df = comb_pay_df[comb_pay_df['match_type'].str.contains('Chari')]
#
#    comb_pay_df_amount = comb_pay_df.groupby(['verif_match'])['amount'].sum()
#    comb_pay_df_count = comb_pay_df.groupby(['verif_match'])['amount'].count()
#    merged_coauth = pd.merge(merged_coauth, comb_pay_df_amount, left_on='verif_match',
#                             how='left', right_index=True)
#    merged_coauth = pd.merge(merged_coauth, comb_pay_df_count, left_on='verif_match',
#                             how='left', right_index=True)
#    merged_coauth = merged_coauth.rename({'amount_x': 'amount_verif'}, axis=1)
#    merged_coauth = merged_coauth.rename({'amount_y': 'count_verif'}, axis=1)
#
#    comb_pay_df_amount = comb_pay_df.groupby(['supplier'])['amount'].sum()
#    comb_pay_df_count = comb_pay_df.groupby(['supplier'])['amount'].count()
#    merged_coauth = pd.merge(merged_coauth, comb_pay_df_amount, left_on='supplier',
#                             how='left', right_index=True)
#    merged_coauth = pd.merge(merged_coauth, comb_pay_df_count, left_on='supplier',
#                             how='left', right_index=True)
#    merged_coauth = merged_coauth.rename({'amount_x': 'amount_rawsup'}, axis=1)
#    merged_coauth = merged_coauth.rename({'amount_y': 'count_rawsup'}, axis=1)
#
#    merged_coauth.to_csv(os.path.join(merge_path, 'charities_for_checking.csv'))



def fix_nhs_confederation_bug(df):
    condition_row = df['CompanyNumber']=='04358614'
    df.loc[condition_row, 'match_type'] = 'Companies House: Charity Commission'
    df.loc[condition_row, 'CharityRegNo'] = 1090329
    df.loc[condition_row, 'CharitySubNo'] = 0
    df.loc[condition_row, 'CharityNameNo'] = 362243
    df.loc[condition_row, 'CharityName'] = 'THE NHS CONFEDERATION'
    df.loc[condition_row, 'audit_type'] = 'THE NHS CONFEDERATION was not given a cc number, but NHS CONFEDERATION was'
    df.loc[condition_row, 'CCnotes'] = 'reg 29/9/15; 71 of 103 NHS pymts 5/5/10-31/8/19 postdate registration. see CHnotes'
    df.loc[condition_row, 'CHnotes'] = 'reg 23/1/02, still active. But note 05256894 The NHS Confederation Group Company Ltd inc 12/10/04 dissolved 29/9/15'
    return df



def normalizer(name, norm_dict={}):
    ''' normalise entity names with manually curated dict'''
    if isinstance(name, str):
        name = name.upper()
        for key, value in norm_dict.items():
            name = name.replace(key, value)
        name = name.replace(r"\(.*\)", "")
        name = "".join(l for l in name if l not in string.punctuation)
        name = ' '.join(name.split())
        name = name.strip()
        return name
    else:
        return None


def overlapping_summary(trust_pay_df, ccg_pay_df, nhsengland_pay_df):
    ch_nhstrust = trust_pay_df[trust_pay_df['match_type'].str.contains('Comp')]['amount'].sum()/trust_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CH in NHS Trust data:', round(ch_nhstrust*100,2))
    ch_ccg = ccg_pay_df[ccg_pay_df['match_type'].str.contains('Comp')]['amount'].sum()/ccg_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CH in CCG data:', round(ch_ccg*100,2))
    ch_nhsengland = nhsengland_pay_df[nhsengland_pay_df['match_type'].str.contains('Comp')]['amount'].sum()/nhsengland_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CH in NHS England data:', round(ch_nhsengland*100,2))
    print('\n')
    cc_nhstrust = trust_pay_df[trust_pay_df['match_type'].str.contains('Char')]['amount'].sum()/trust_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CC in NHS Trust data:', round(cc_nhstrust*100,2))
    cc_ccg = ccg_pay_df[ccg_pay_df['match_type'].str.contains('Char')]['amount'].sum()/ccg_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CC in CCG data:', round(cc_ccg*100,2))
    cc_nhsengland = nhsengland_pay_df[nhsengland_pay_df['match_type'].str.contains('Char')]['amount'].sum()/nhsengland_pay_df['amount'].sum()
    print('Percent value INCLUDING overlapping payments to CC in NHS England data:', round(cc_nhsengland*100,2))


def make_onetable(df):
    columns = ['PDF', 'Excel', 'CSV', 'Total']
    rows = ['Files', 'Rows', 'Value (£m)', 'Mean (£k)', 'Suppliers']
    table = pd.DataFrame(columns=columns, index=rows)
    df_pdf = df[df['file'].str.lower().str.endswith('pdf.csv')]
    table.loc['Files', 'PDF'] = len(df_pdf['file'].unique())
    table.loc['Rows', 'PDF'] = len(df_pdf)
    table.loc['Value (£m)', 'PDF'] = df_pdf['amount'].sum()/1000000
    table.loc['Mean (£k)', 'PDF'] = df_pdf['amount'].mean()/1000
    table.loc['Suppliers', 'PDF'] = len(df_pdf['verif_match'].unique())

    df_excel = df[df['file'].str.lower().str.contains('.xl')]
    table.loc['Files', 'Excel'] = len(df_excel['file'].unique())
    table.loc['Rows', 'Excel'] = len(df_excel)
    table.loc['Value (£m)', 'Excel'] = df_excel['amount'].sum()/1000000
    table.loc['Mean (£k)', 'Excel'] = df_excel['amount'].mean()/1000
    table.loc['Suppliers', 'Excel'] = len(df_excel['verif_match'].unique())

    df_csv = df[df['file'].str.lower().str.endswith('.csv')]
    df_csv = df_csv[~df_csv['file'].str.lower().str.endswith('pdf.csv')]
    table.loc['Files', 'CSV'] = len(df_csv['file'].unique())
    table.loc['Rows', 'CSV'] = len(df_csv)
    table.loc['Value (£m)', 'CSV'] = df_csv['amount'].sum()/1000000
    table.loc['Mean (£k)', 'CSV'] = df_csv['amount'].mean()/1000
    table.loc['Suppliers', 'CSV'] = len(df_csv['verif_match'].unique())
    table.loc['Files', 'Total'] = table.at['Files', 'PDF'] + \
                                  table.at['Files', 'Excel'] + \
                                  table.at['Files', 'CSV']
    table.loc['Rows', 'Total'] = len(df)
    table.loc['Value (£m)', 'Total'] = df['amount'].sum()/1000000
    table.loc['Mean (£k)', 'Total'] =  df['amount'].mean()/1000
    table.loc['Suppliers', 'Total'] =  len(df['verif_match'].unique())
    return table


def check_payments(df, filecheck_path, data_path,
                   orgtype, number_to_check=25):
    if os.path.exists(filecheck_path):
        checker = pd.read_csv(filecheck_path)
    else:
        checker = pd.DataFrame()
    pd.set_option('display.expand_frame_repr', False)
    order_df = df.sort_values(by='amount', ascending=False)
    order_df = order_df.reset_index()[['file', 'dept']].\
        drop_duplicates()[0:number_to_check]
    order_df = pd.merge(order_df, checker, how='left',
                        left_on='file', right_on = 'file')
    if (len(order_df[order_df['checked']!=1])) > 0:
        print('Danger! There are still ' +
              str(len(order_df[order_df['checked']!=1])) +
              ' ' + str(orgtype) + ' payments to check by order!')
        print('Theyre being stored at ' +
              str(os.path.join(data_path, 'data_support',
                               orgtype + '_ordered_to_check.csv')))
        order_df.to_csv(os.path.join(data_path, 'data_support',
                                     orgtype + '_ordered_to_check.csv'))
    else:
        print('Cool! No more ' + str(orgtype) + ' payments to check by order...')
    grouped_df = df.sort_values(by='amount',
                                ascending=False)[0:20000]
#    print(grouped_df)
    grouped_df_sum = grouped_df.groupby(['file'])['amount'].sum()
    grouped_df_count = grouped_df.groupby(['file'])['file'].count()
    grouped_df_merge = pd.merge(grouped_df_sum, grouped_df_count,
                                how='left', left_index=True,
                                right_index=True)
    grouped_df_merge = grouped_df_merge.rename({'file':'count'}, axis=1)
    grouped_df_merge = grouped_df_merge[grouped_df_merge['count']>=5]
    grouped_df_merge = grouped_df_merge.sort_values(by='count',
                                                    ascending=False)[0:number_to_check]
    grouped_df_merge = pd.merge(grouped_df_merge, df[['file', 'dept']].drop_duplicates(subset=['file']),
                                how='left', left_index = True,
                                right_on = 'file')
    grouped_df_merge = pd.merge(grouped_df_merge, checker, how='left',
                                left_on='file', right_on = 'file')
    if (len(grouped_df_merge[grouped_df_merge['checked']!=1]))>0:
        print('Danger! There are still ' +
              str(len(grouped_df_merge[grouped_df_merge['checked']!=1])) +
              ' ' + str(orgtype) + ' payment files to check after groupby!')
        print('Theyre being stored at ' +
              str(os.path.join(data_path, 'data_support',
                               orgtype + '_grouped_to_check.csv')))
        grouped_df_merge.to_csv(os.path.join(data_path, 'data_support',
                                             orgtype + '_grouped_to_check.csv'))
    else:
        print('Cool! No more ' + str(orgtype) + ' payments to check by groupby...')





def check_payments_abs(df, filecheck_path, data_path,
                   orgtype, number_to_check=25):
    if os.path.exists(filecheck_path):
        checker = pd.read_csv(filecheck_path)
    else:
        checker = pd.DataFrame()
    pd.set_option('display.expand_frame_repr', False)
    df['abs_amount'] = df['amount'].abs()
    order_df = df.sort_values(by='abs_amount', ascending=False)
    order_df = order_df.reset_index()[['file', 'dept']].\
        drop_duplicates()[0:number_to_check]
    order_df = pd.merge(order_df, checker, how='left',
                        left_on='file', right_on = 'file')
    if (len(order_df[order_df['checked']!=1])) > 0:
        print('Danger! There are still ' +
              str(len(order_df[order_df['checked']!=1])) +
              ' ' + str(orgtype) + ' absolute amount payments to check by order!')
        print('Theyre being stored at ' +
              str(os.path.join(data_path, 'data_support',
                               orgtype + '_abs_ordered_to_check.csv')))
        order_df.to_csv(os.path.join(data_path, 'data_support',
                                     orgtype + '_abs_ordered_to_check.csv'))
    else:
        print('Cool! No more ' + str(orgtype) + ' absolute amount payments to check by order...')
    grouped_df = df.sort_values(by='abs_amount',
                                ascending=False)[0:20000]
#    print(grouped_df)
    grouped_df_sum = grouped_df.groupby(['file'])['abs_amount'].sum()
    grouped_df_count = grouped_df.groupby(['file'])['file'].count()
    grouped_df_merge = pd.merge(grouped_df_sum, grouped_df_count,
                                how='left', left_index=True,
                                right_index=True)
    grouped_df_merge = grouped_df_merge.rename({'file':'count'}, axis=1)
    grouped_df_merge = grouped_df_merge[grouped_df_merge['count']>=5]
    grouped_df_merge = grouped_df_merge.sort_values(by='count',
                                                    ascending=False)[0:number_to_check]
    grouped_df_merge = pd.merge(grouped_df_merge, df[['file', 'dept']].drop_duplicates(subset=['file']),
                                how='left', left_index = True,
                                right_on = 'file')
    grouped_df_merge = pd.merge(grouped_df_merge, checker, how='left',
                                left_on='file', right_on = 'file')
    if (len(grouped_df_merge[grouped_df_merge['checked']!=1]))>0:
        print('Danger! There are still ' +
              str(len(grouped_df_merge[grouped_df_merge['checked']!=1])) +
              ' ' + str(orgtype) + ' absolute amount payment files to check after groupby!')
        print('Theyre being stored at ' +
              str(os.path.join(data_path, 'data_support',
                               orgtype + 'abs_grouped_to_check.csv')))
        grouped_df_merge.to_csv(os.path.join(data_path, 'data_support',
                                             orgtype + 'abs_grouped_to_check.csv'))
    else:
        print('Cool! No more ' + str(orgtype) + ' absolute amount payments to check by groupby...')



def make_table_one(ccg_pay_df, trust_pay_df, nhsengland_pay_df, table_path):
    ccg_clean = make_onetable(ccg_pay_df)
    trusts_clean = make_onetable(trust_pay_df)
    nhsengland_clean = make_onetable(nhsengland_pay_df)
    all_clean = make_onetable(pd.concat([ccg_pay_df, trust_pay_df, nhsengland_pay_df]))
    df_out = pd.concat([ccg_clean, trusts_clean, nhsengland_clean, all_clean], axis=1)
    df_out.to_csv(os.path.join(table_path, 'Table1.csv'))



def calc_total_files(raw_ccg_path):
    counter = 0
    count = 0
    hold = []
    for root, dirs, files in os.walk(raw_ccg_path):
        hold.append(files)
        holder = []
        for file in files:
            holder.append(file.split('.')[0])
        counter = counter + len(set(holder))
    return counter, len(hold)


def plot_macro_overview(data_path, figure_path):
    titlefont = 20
    letterfont = 22
    labelfont = 14
    mpl.rc('font',family='Helvetica')
    cwd = os.getcwd()
    csfont = {'fontname':'Helvetica'}
    hfont = {'fontname':'Helvetica'}
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    data_path = os.path.join(data_path,'data_support',
                             'summary_plot_data')
    trusts = pd.read_csv(os.path.join(data_path,
                         'trust_performance.csv'))
    trusts['plan'] = trusts['plan']/1000
    trusts['actual'] = trusts['actual']/1000
    oecd_comp = pd.read_csv(os.path.join(data_path,
                                         'oecd_int_comparison.csv'))
    overtime = pd.read_csv(os.path.join(data_path,
                                        'nhs_spending_over_time2.csv'))
    sectors = pd.read_csv(os.path.join(data_path,
                                       'sectors_summary.csv'))
    sectors['indep'] = sectors['indep']/1000000
    sectors['vol'] = sectors['vol']/1000000
    sectors['local_auth'] = sectors['local_auth']/1000000
    oecd_trim = pd.DataFrame()
    temp = oecd_comp[oecd_comp['Year']==2018]
    temp = temp[temp['Measure']=='Share of gross domestic product']
    temp = temp[temp['Function']=='Current expenditure on health (all functions)']
    temp = temp[temp['Financing scheme']=='Government/compulsory schemes']
    oecd_trim['share'] = temp['Value']
    temp = oecd_comp[oecd_comp['Year']==2018]
    temp = temp[temp['Measure']=='Per capita, current prices, current PPPs']
    temp = temp[temp['Function']=='Current expenditure on health (all functions)']
    temp = temp[temp['Financing scheme']=='Government/compulsory schemes']
    temp['Value'] = temp['Value']/1000
    oecd_trim['ppp'] = temp['Value'].tolist()
    oecd_trim['LOCATION'] = temp['LOCATION'].tolist()
    alloc = pd.read_csv(os.path.join(data_path, 'ccg_allocations.csv'))
    alloc['Final allocation'] = alloc['Final allocation']/1000

    fig = plt.figure(figsize=(17, 14))
    ax1 = plt.subplot2grid((12, 2), (0, 0), colspan=1, rowspan=6)
    ax2 = plt.subplot2grid((12, 2), (0, 1), colspan=1, rowspan=6)
    ax3 = plt.subplot2grid((12, 2), (6, 0), colspan=1, rowspan=6)
    ax4 = plt.subplot2grid((12, 2), (6, 1), colspan=1, rowspan=3)
    ax5 = plt.subplot2grid((12, 2), (9, 1), colspan=1, rowspan=3)

    trusts_above = trusts[trusts['actual']>0][['plan', 'actual']]
    trusts_below = trusts[trusts['actual']<=0][['plan', 'actual']]
    ee = trusts_above[['plan', 'actual']].plot.scatter(x='plan', y='actual',
                                                       ax=ax1, edgecolor='k',
                                                       s=100, alpha=0.55, color='#377eb8',
                                                       #label='Trust in Surplus'
                                                       )
    ee = trusts_below[['plan', 'actual']].plot.scatter(x='plan', y='actual',
                                                 ax=ax1, edgecolor='k',
                                                 s=100, alpha=0.55,
                                                 color='#d13232',
#                                                label='Trust in Deficit'
                                                 )
    ee.axhline(y=0.0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
    ee.axvline(x=0.0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
    ee.xaxis.set_ticks_position('none')
#    ee.legend(edgecolor=(0,0,0,1), fontsize=labelfont-4, loc='lower right', framealpha=1)
    ee.yaxis.set_ticks_position('none')
    ee.set_xlabel('Planned deficit/surplus (£m)', **hfont, fontsize=labelfont)
    ee.set_ylabel('Actual deficit/surplus (£m)', **hfont, fontsize=labelfont)
#    ee.set_title('NHS Trust accounts: 2018/2019', fontsize=titlefont,y=1.01)
    ee.set_title('A.', fontsize=letterfont, y=1.04, x=-0.04, loc='left')
    formatter = ticker.FormatStrFormatter('£%1.0fm')
    ee.yaxis.set_major_formatter(formatter)
    ee.xaxis.set_major_formatter(formatter)
    oecd_trim = oecd_trim[oecd_trim['share']<10]
    oecd_trim = oecd_trim[oecd_trim['ppp']<8]
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    inset_axes = inset_axes(ee,
                            width="50%", # width = 30% of parent_bbox
                            height="30%", # height : 1 inch
                            #bbox_to_anchor=(0, 0 ,50, 25),
                            loc='upper left')
    inset_axes.hist(trusts_above['plan']-trusts_above['actual'],
                    edgecolor=(0,0,0,1), alpha=0.55, bins=14,
                    label='Overspend',
                    color='#d13232')
    inset_axes.yaxis.set_label_position('right')
    inset_axes.set_ylabel('Frequency')
    inset_axes.patches[-1].set_color('#377eb8')
    inset_axes.patches[-1].set_alpha(0.55)
    inset_axes.patches[-1].set_label('Underspend')
    inset_axes.patches[-1].set_edgecolor('k')
    lines, labels = inset_axes.get_legend_handles_labels()
    inset_axes.legend(lines, labels,
                      edgecolor='w', fontsize=labelfont-1,
                      loc='upper left')
    formatter = ticker.FormatStrFormatter('£%1.0fm')
    inset_axes.xaxis.set_major_formatter(formatter)
    sns.despine(ax=inset_axes, left=True, right=False, top=True)

    ff = sns.regplot(x='share', y='ppp',
                     data=oecd_trim, ax=ax2,
                     scatter_kws={'s':40, 'edgecolor':'k',
                                  'alpha':0.66},
                     line_kws = {'color': '#e57600',
                                 'alpha': 0.5},
                     ci=68)
#    ff.set_title('International spending: 2018/2019',
#                 fontsize=titlefont,y=1.01)
    ff.set_title('B.', fontsize=letterfont,y=1.04, x=-0.04, loc='left')
    ff.set_xlabel('Share of gross domestic product (%)',
                  **hfont, fontsize=labelfont)
    ff.set_ylabel('Per capita, current prices, current PPPs (£000s)',
                  **hfont, fontsize=labelfont)
    ff.set_xlim(2.8, 10)
    counter = 0
    oecd_trim = oecd_trim.reset_index()
    for i in oecd_trim['LOCATION'].tolist():
        ff.annotate(i, (oecd_trim['share'][counter]+.075,
                    oecd_trim['ppp'][counter]+.075))
        counter = counter+1
    formatter = ticker.FormatStrFormatter('£%1.0fk')
    ff.yaxis.set_major_formatter(formatter)
    vals = ff.get_xticks()
    ff.set_xticklabels(['{:,.2%}'.format(x/100) for x in vals])

    gg = overtime[0:9].plot(ax=ax3, x='time_index',
                       y='pesa_merged_pc', color='#0087DC',
                       linestyle='--', label='Conservative')
    gg2 = overtime[8:22].plot(ax=ax3, x='time_index',
                              y='pesa_merged_pc', color='#DC241f',
                              linestyle='--', label='Labour')
    gg3 = overtime[21:27].plot(ax=ax3, x='time_index',
                              y='pesa_merged_pc', color='#FDBB30',
                              linestyle='--', label='Coalition')
    gg4 = overtime[26:].plot(ax=ax3, x='time_index',
                             y='pesa_merged_pc', color='#0087DC',
                             linestyle='--', label='')
#    gg.set_title('NHS Spending as % GDP over time', fontsize=titlefont,y=1.01)
    gg.set_title('C.', fontsize=letterfont, y=1.04, x=-0.04, loc='left')
    gg.set_ylim(3, 9)
    gg.set_xlim(1985, 2019)
    formatter = ticker.FormatStrFormatter('£%1.0fbn')
    gg.yaxis.set_major_formatter(formatter)
    vals = gg.get_yticks()
    gg.set_yticklabels(['{:,.2%}'.format(x/100) for x in vals])
    gg.set_xlabel('', **hfont, fontsize=labelfont)
    gg.set_ylabel('Percent of Spending (%)', **hfont, fontsize=labelfont)
    gg.set_xlabel('Year', **hfont, fontsize=labelfont)
    gg.annotate('Thatcher/Major', xy=(1991.75, 4.85),
                xytext=(1991.75, 5.1),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=5.4, lengthB=1',
                                lw=1.0))
    gg.annotate('Blair/Brown', xy=(2003.25, 7.55),
                xytext=(2003.25, 7.75),# xycoords='axes fraction',
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=6.8, lengthB=1', lw=1.0))
    gg.annotate('Cameron/Osbourne', xy=(2012.4, 7.9), xytext=(2012.4, 8.1),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=2.6, lengthB=1', lw=1.0))
    gg.annotate('Cameron/May', xy=(2017.5, 8.5), xytext=(2017.5, 8.7),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=2.35, lengthB=1', lw=1.0))
    lines, labels = gg.get_legend_handles_labels()
    gg.legend(lines, labels,
              edgecolor='w',
              fontsize=labelfont-2, loc='upper left')
    hh = sns.distplot(alloc['Final allocation'], ax=ax4,
                      kde_kws={"color": '#ffb94e',
                      "lw": 2, "label": "Kernel Density Estimate",
                      "alpha": 1},
                     hist_kws={"alpha": 0.5,
                               "color": '#377eb8',
                               "label": "Frequency",
                               'edgecolor': 'k'})
    hh.set_xlabel('', **hfont, fontsize=12)
    ii = sns.distplot(alloc['Per capita allocation'],
                      ax=ax5,
                      kde_kws={"color": '#ffb94e', "lw": 2,
                               "label": "Kernel Density Estimate",
                               "alpha": 1},
                     hist_kws={"alpha": 0.5, "label": "Frequency",
                               'edgecolor': 'k',
                               "color": '#377eb8'})
    hh.set_ylabel("Density", **hfont, fontsize=labelfont)
    ii.set_ylabel("Density", **hfont, fontsize=labelfont)
    ii.set_xlabel('Value', **hfont, fontsize=labelfont)
    formatter = ticker.FormatStrFormatter('%.3f')
    hh.yaxis.set_major_formatter(formatter)
    formatter = ticker.FormatStrFormatter('£%1.0fm')
    hh.xaxis.set_major_formatter(formatter)
    ii.legend(edgecolor='w', fontsize=labelfont-2)
    hh.legend(edgecolor='w', fontsize=labelfont-2)
#    hh.set_title('CCG allocations: 2019/2020',
#                 fontsize=titlefont,y=1.01)
    hh.set_title('D.', fontsize=letterfont, y=1.04, x=-0.04, loc='left')
#    ii.set_title('CCG allocations per capita: 2019/2020', fontsize=titlefont,y=1.01)
    ii.set_title('E.', fontsize=letterfont, y=1.04, x=-0.04, loc='left')
    ii.xaxis.set_major_formatter(formatter)
    ii.set_xlabel('', **hfont, fontsize=12)
    formatter = ticker.FormatStrFormatter('£%1.0f')
    ii.xaxis.set_major_formatter(formatter)

    sns.despine(ax=ax1)
    sns.despine(ax=ax2)
    sns.despine(ax=gg)
    sns.despine(ax=ax4)
    sns.despine(ax=ax5)
    plt.subplots_adjust(hspace = 30)
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.png'), dpi=500,
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.svg'),
                bbox_inches='tight')

def load_suppliers(sup_path):
    sup_df = pd.read_csv(sup_path, sep='\t')
    return sup_df


def load_payments(pay_path):
    pay_df = pd.read_csv(pay_path, sep=',',
                         usecols=['expensetype', 'supplier', 'date', 'dept',
                                  'amount', 'file', 'expensearea',
                                  'transactionnumber', 'verif_match',
                                  'query_string_n',
                                  'match_type', 'audit_type',
                                  'CompanyName', 'CompanyNumber',
                                  'CharityRegNo', 'CharitySubNo',
                                  'CharityNameNo', 'CharityName', 'audit_type',
                                  'CHnotes', 'CCnotes', 'isCIC'
                                  ],
                         dtype={'query_string_n': str,
                                'verif_match': str,
                                'match_type': str,
                                'CompanyName': str,
                                'CharityName': str,
                                'transactionnumber': str},
                         parse_dates=['date'])
    pay_df = pay_df[pay_df['dept'] != 'NHS_RED_CCG']
    pay_df = pay_df[pay_df['dept'] != 'NHS_HAV_CCG']
    return pay_df


def analyze_registers(ch_path, cc_path, nhsdigital_path, master_path):
    ch_raw = pd.read_csv(os.path.join(ch_path, 'ch_uniq.csv'))
    ch_norm = pd.read_csv(os.path.join(ch_path, 'ch_uniq_norm.csv'))
    print('Number unique raw CH entries:',
          len(ch_raw['name']))
    print('Number non-duplicated normalized CH entries:',
          len(ch_norm['name_norm']))
    cc_raw = pd.read_csv(os.path.join(cc_path, 'cc_uniq.csv'))
    cc_norm = pd.read_csv(os.path.join(cc_path, 'cc_uniq_norm.csv'))
    print('Number unique raw CC entries:',
          len(cc_raw['name']))
    print('Number non-duplicated normalized CC entries:',
          len(cc_norm['name_norm']))
    nhsdigital_raw = pd.read_csv(os.path.join(nhsdigital_path,
                                              'nhs_uniq.csv'))
    nhsdigital_norm = pd.read_csv(os.path.join(nhsdigital_path,
                                                   'nhs_uniq_norm.csv'))
    print('Number unique raw NHS Digital entries:',
          len(nhsdigital_raw['name']))
    print('Number non-duplicated normalized NHS Digital entries:',
          len(nhsdigital_norm['name_norm']))
    comb_uniq_raw = pd.read_csv(os.path.join(master_path,
                                             'combined_unique_list.csv'))
    comb_uniq_norm = pd.read_csv(os.path.join(master_path,
                                              'combined_unique_list_norm.csv'))
    print('Number unique raw combined entries:',
          len(comb_uniq_raw['name']))
    print('Number non-duplicated normalized combined entries:',
          len(comb_uniq_norm['name_norm']))
    ch_norm = set(ch_norm['name_norm'].tolist())
    cc_norm = set(cc_norm['name_norm'].tolist())
    nhs_norm = set(nhsdigital_norm['name_norm'].tolist())
    ch_and_cc = pd.Series(list(ch_norm.intersection(cc_norm)))
    ch_and_nhs = pd.Series(list(ch_norm.intersection(nhs_norm)))
    cc_and_nhs = pd.Series(list(cc_norm.intersection(nhs_norm)))
    all_three = pd.Series(list(cc_norm.intersection(nhs_norm).intersection(ch_norm)))
    print('There are ' + str(len(ch_and_cc)) +
          ' normalised unique names on both CH and CC')
    print('There are ' + str(len(ch_and_nhs)) +
          ' normalised unique names on both CH and NHS')
    print('There are ' + str(len(cc_and_nhs)) +
          ' normalised unique names on both CC and NHS')
    print('There are ' + str(len(all_three)) +
          ' normalised unique names on all 3')


def summarize_payments(pay_df, payment_type, name_column):
    print('Describing cleaned ' + payment_type + ' payments dataset!')

    pay_df.loc[:, 'date'] = pd.to_datetime(pay_df.loc[:, 'date'], format='mixed')
    print('Length of dataset:', len(pay_df))
    print('Total unique raw suppliers:', len(pay_df['supplier'].unique()))
    print('Total unique verified suppliers:', len(pay_df[name_column].unique()))
    print('Total value (£) of dataset:', int(pay_df['amount'].sum()))
    print('Smallest value payment:', int(pay_df['amount'].min()))
    print('Biggest value payment:', int(pay_df['amount'].max()))
    print('Average value payment:', int(pay_df['amount'].mean()))
    print('Earliest payment was:', pay_df['date'].min())
    print('Latest payment was:', pay_df['date'].max())
    most_dept = pay_df.groupby(['dept']).size().sort_values(ascending=False)
    print('Most payments is: ', most_dept.index[0],
          '('+ str(most_dept[0]) + ')')
    value_dept = pay_df.groupby('dept')['amount'].sum().sort_values(ascending=False)
    print('Highest value payments is:', value_dept.index[0],
          '(£' + str(int(value_dept[0])) + ')')
    most_supp = pay_df[(pay_df['verif_match'] != 'No Match') &
                       (pay_df['verif_match'] != 'Named Doctor')].groupby(['verif_match']).size().sort_values(ascending=False)
    print('Most payments (other than "no match"):', most_supp.index[0],
          '(' + str(most_supp[0]) + ')')
    value_supp = pay_df[(pay_df['verif_match'] != 'No Match') &
                       (pay_df['verif_match'] != 'Named Doctor')].groupby('verif_match')['amount'].sum().sort_values(ascending=False)
    print('Highest value of payments (other than "no match") is:', value_supp.index[0],
          '(' + str(value_supp[0]) + ')')
    print('Number of organisations in clean dataset is: ' +\
          str(len(pay_df['dept'].unique())))
    print('Number of files in clean dataset is: ' +\
          str(len(pay_df[['dept', 'file']].drop_duplicates()['file'].unique())))


from matplotlib_venn import venn3, venn3_circles
import matplotlib.patches as patches
import matplotlib.ticker as ticker

def make_vennlist(payments):
    """ Make the vennlist for the venn diagram"""

    char_sups = payments[payments['match_type'] == 'Charity Commission']
    char_sups = char_sups.drop_duplicates(subset=['CharityRegNo'])
    char_num = len(char_sups)
    all_three = payments[(payments['match_type'].str.
                          contains('Charity Commission')) &
                         (payments['match_type'].str.count(':') == 2)]
    all_three = all_three.drop_duplicates(subset=['CharityRegNo', 'CompanyNumber'])
    char_num_three = len(all_three)
    comp_sups = payments[payments['match_type'] == 'Companies House']
    comp_sups = comp_sups.drop_duplicates(subset=['CompanyNumber'])
    comp_num = len(comp_sups)
    nhs_sups = payments[payments['match_type'] == 'NHS Digital']
    nhs_sups = nhs_sups.drop_duplicates(subset=['verif_match'])
    nhs_num = len(nhs_sups)
    charcom_sups = payments[(payments['match_type'].str.
                              contains('Charity Commission')) &
                             (payments['match_type'].str.
                              contains('Companies House'))]
    charcom_sups = charcom_sups.drop_duplicates(subset=['CharityRegNo', 'CompanyNumber'])
    charcom_num = len(charcom_sups)

    charnhs_sups = payments[(payments['match_type'].str.
                             contains('Charity Commission')) &
                            (payments['match_type'].str.
                             contains('NHS Digital'))]
    charnhs_sups = charnhs_sups.drop_duplicates(subset=['CharityRegNo'])
    charnhs_num = len(charnhs_sups)

    comnhs_sups = payments[(payments['match_type'].str.
                            contains('Companies House')) &
                           (payments['match_type'].str.
                            contains('NHS Digital'))]
    comnhs_sups = charnhs_sups.drop_duplicates(subset=['CompanyNumber'])
    comnhs_num = len(comnhs_sups)
    venn_list = [char_num, comp_num, charcom_num, nhs_num,
                 charnhs_num, comnhs_num, char_num_three]
    return venn_list



def make_match_df(payments):
    uniq_sups = payments[['query_string_n','verif_match', 'match_type']].drop_duplicates(subset=['query_string_n'])
    index = range(0, 18)
    cols = ['Type', 'Identification', 'Number Suppliers',
            'Payment Value', 'Number Payments']
    df = pd.DataFrame(columns=cols, index=index)
    char_num = len(uniq_sups[uniq_sups['match_type'] == 'Charity Commission'])
    char_count = len(payments[payments['match_type'] == 'Charity Commission'])
    char_val = payments[payments['match_type'] == 'Charity Commission']['amount'].sum()
    df.at[0, 'Type'] = 'Charity'
    df.at[0, 'Identification'] = 'Unique'
    df.at[0, 'Number Suppliers'] = char_num
    df.at[0, 'Number Payments'] = char_count
    df.at[0, 'Payment Value'] = char_val
    char_num_two = len(uniq_sups[(uniq_sups['match_type'].str.
                                 contains('Charity Commission')) &
                                 (uniq_sups['match_type'].str.count(':') == 1)])
    char_count_two = len(payments[(payments['match_type'].str.
                                  contains('Charity Commission')) &
                                  (payments['match_type'].str.count(':') == 1)])
    char_val_two = payments[(payments['match_type'].str.
                            contains('Charity Commission')) &
                            (payments['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[1, 'Type'] = 'Charity'
    df.at[1, 'Identification'] = 'Two Registers'
    df.at[1, 'Number Suppliers'] = char_num_two
    df.at[1, 'Number Payments'] = char_count_two
    df.at[1, 'Payment Value'] = char_val_two
    char_num_three = len(uniq_sups[(uniq_sups['match_type'].str.
                                    contains('Charity Commission')) &
                                   (uniq_sups['match_type'].str.count(':') == 2)])
    char_count_three = len(payments[(payments['match_type'].str.
                                    contains('Charity Commission')) &
                                    (payments['match_type'].str.count(':') == 2)])
    char_val_three = payments[(payments['match_type'].str.
                              contains('Charity Commission')) &
                              (payments['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[2, 'Type'] = 'Charity'
    df.at[2, 'Identification'] = 'Three Registers'
    df.at[2, 'Number Suppliers'] = char_num_three
    df.at[2, 'Number Payments'] = char_count_three
    df.at[2, 'Payment Value'] = char_val_three
    comp_num = len(uniq_sups[uniq_sups['match_type'] == 'Companies House'])
    comp_count = len(payments[payments['match_type'] == 'Companies House'])
    comp_val = payments[payments['match_type'] == 'Companies House']['amount'].sum()
    df.at[3, 'Type'] = 'Company'
    df.at[3, 'Identification'] = 'Unique'
    df.at[3, 'Number Suppliers'] = comp_num
    df.at[3, 'Number Payments'] = comp_count
    df.at[3, 'Payment Value'] = comp_val
    comp_num_two = len(uniq_sups[(uniq_sups['match_type'].str.
                                  contains('Companies House')) &
                                 (uniq_sups['match_type'].str.count(':') == 1)])
    comp_count_two = len(payments[(payments['match_type'].str.
                                   contains('Companies House')) &
                                  (payments['match_type'].str.count(':') == 1)])
    comp_val_two = payments[(payments['match_type'].str.
                             contains('Companies House')) &
                            (payments['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[4, 'Type'] = 'Company'
    df.at[4, 'Identification'] = 'Three Registers'
    df.at[4, 'Number Suppliers'] = comp_num_two
    df.at[4, 'Number Payments'] = comp_count_two
    df.at[4, 'Payment Value'] = comp_val_two
    comp_num_three = len(uniq_sups[(uniq_sups['match_type'].str.
                                    contains('Companies House')) &
                                   (uniq_sups['match_type'].str.count(':') == 2)])
    comp_count_three = len(payments[(payments['match_type'].str.
                                     contains('Companies House')) &
                                    (payments['match_type'].str.count(':') == 2)])
    comp_val_three = payments[(payments['match_type'].str.
                              contains('Companies House')) &
                              (payments['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[5, 'Type'] = 'Company'
    df.at[5, 'Identification'] = 'Two Registers'
    df.at[5, 'Number Suppliers'] = comp_num_three
    df.at[5, 'Number Payments'] = comp_count_three
    df.at[5, 'Payment Value'] = comp_val_three
    nhs_num = len(uniq_sups[uniq_sups['match_type'] == 'NHS Digital'])
    nhs_count = len(payments[payments['match_type'] == 'NHS Digital'])
    nhs_val = payments[payments['match_type'] == 'NHS Digital']['amount'].sum()
    df.at[6, 'Type'] = 'NHS'
    df.at[6, 'Identification'] = 'Unique'
    df.at[6, 'Number Suppliers'] = nhs_num
    df.at[6, 'Number Payments'] = nhs_count
    df.at[6, 'Payment Value'] = nhs_val
    nhs_num_two = len(uniq_sups[(uniq_sups['match_type'].str.
                                contains('NHS Digital')) &
                                (uniq_sups['match_type'].str.count(':') == 1)])
    nhs_count_two = len(payments[(payments['match_type'].str.
                                 contains('NHS Digital')) &
                                 (payments['match_type'].str.count(':') == 1)])
    nhs_val_two = payments[(payments['match_type'].str.
                           contains('NHS Digital')) &
                           (payments['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[7, 'Type'] = 'NHS'
    df.at[7, 'Identification'] = 'Two Registers'
    df.at[7, 'Number Suppliers'] = nhs_num_two
    df.at[7, 'Number Payments'] = nhs_count_two
    df.at[7, 'Payment Value'] = nhs_val_two
    nhs_num_three = len(uniq_sups[(uniq_sups['match_type'].str.
                                   contains('NHS Digital')) &
                                  (uniq_sups['match_type'].str.count(':') == 2)])
    nhs_count_three = len(payments[(payments['match_type'].str.
                                    contains('NHS Digital')) &
                                   (payments['match_type'].str.count(':') == 2)])
    nhs_val_three = payments[(payments['match_type'].str.
                             contains('NHS Digital')) &
                            (payments['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[8, 'Type'] = 'NHS'
    df.at[8, 'Identification'] = 'Three Registers'
    df.at[8, 'Number Suppliers'] = nhs_num_three
    df.at[8, 'Number Payments'] = nhs_count_three
    df.at[8, 'Payment Value'] = nhs_val_three
    dr_num = len(uniq_sups[uniq_sups['match_type'] == 'Named Doctor'])
    dr_count = len(payments[payments['match_type'] == 'Named Doctor'])
    dr_val = payments[payments['match_type'] == 'Named Doctor']['amount'].sum()
    df.at[9, 'Type'] = 'Doctor'
    df.at[9, 'Identification'] = 'Unique'
    df.at[9, 'Number Suppliers'] = dr_num
    df.at[9, 'Number Payments'] = dr_count
    df.at[9, 'Payment Value'] = dr_val
    df.at[10, 'Type'] = 'Doctor'
    df.at[10, 'Identification'] = 'Two Registers'
    df.at[10, 'Number Suppliers'] = 0
    df.at[10, 'Number Payments'] = 0
    df.at[10, 'Payment Value'] = 0
    df.at[11, 'Type'] = 'Doctor'
    df.at[11, 'Identification'] = 'Three Registers'
    df.at[11, 'Number Suppliers'] = 0
    df.at[11, 'Number Payments'] = 0
    df.at[11, 'Payment Value'] = 0
    per_num = len(uniq_sups[uniq_sups['match_type'] == 'Named Person'])
    per_count = len(payments[payments['match_type'] == 'Named Person'])
    per_val = payments[payments['match_type'] == 'Named Person']['amount'].sum()
    df.at[12, 'Type'] = 'Person'
    df.at[12, 'Identification'] = 'Unique'
    df.at[12, 'Number Suppliers'] = per_num
    df.at[12, 'Number Payments'] = per_count
    df.at[12, 'Payment Value'] = per_val
    df.at[13, 'Type'] = 'Person'
    df.at[13, 'Identification'] = 'Two Registers'
    df.at[13, 'Number Suppliers'] = 0
    df.at[13, 'Number Payments'] = 0
    df.at[13, 'Payment Value'] = 0
    df.at[14, 'Type'] = 'Person'
    df.at[14, 'Identification'] = 'Three Registers'
    df.at[14, 'Number Suppliers'] = 0
    df.at[14, 'Number Payments'] = 0
    df.at[14, 'Payment Value'] = 0
    none_num = len(uniq_sups[uniq_sups['match_type'] == 'No Match'])
    none_count = len(payments[payments['match_type'] == 'No Match'])
    none_val = payments[payments['match_type'] == 'No Match']['amount'].sum()
    df.at[15, 'Type'] = 'No Match'
    df.at[15, 'Identification'] = 'Unique'
    df.at[15, 'Number Suppliers'] = none_num
    df.at[15, 'Number Payments'] = none_count
    df.at[15, 'Payment Value'] = none_val
    df.at[16, 'Type'] = 'No Match'
    df.at[16, 'Identification'] = 'Two Registers'
    df.at[16, 'Number Suppliers'] = 0
    df.at[16, 'Number Payments'] = 0
    df.at[16, 'Payment Value'] = 0
    df.at[17, 'Type'] = 'No Match'
    df.at[17, 'Identification'] = 'Three Registers'
    df.at[17, 'Number Suppliers'] = 0
    df.at[17, 'Number Payments'] = 0
    df.at[17, 'Payment Value'] = 0
    return df


def plot_match_distribution(sup_df, trust_pay_df, ccg_pay_df, nhsengland_pay_df,
                            figure_path, figsize_tuple):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    colors = ['#41558c', '#E89818', '#CF202A',
               '#8C5E41', '#1856E8', '#2ACF20']
    pay_df = pd.concat([trust_pay_df, ccg_pay_df])
    fig = plt.figure(figsize=figsize_tuple, constrained_layout=True)
    ax1 = plt.subplot2grid((20, 2), (0, 0), colspan=1, rowspan=7)
    ax2 = plt.subplot2grid((20, 2), (0, 1), colspan=1, rowspan=7)
    axfake1 = plt.subplot2grid((20, 2), (7, 1), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid((20, 6), (8, 0), colspan=1, rowspan=4)
    ax4 = plt.subplot2grid((20, 6), (8, 1), colspan=1, rowspan=4)
    ax5 = plt.subplot2grid((20, 6), (8, 2), colspan=1, rowspan=4)
    ax6 = plt.subplot2grid((20, 6), (8, 3), colspan=1, rowspan=4)
    ax7 = plt.subplot2grid((20, 6), (8, 4), colspan=1, rowspan=4)
    ax8 = plt.subplot2grid((20, 6), (8, 5), colspan=1, rowspan=4)
#    axfake2 = plt.subplot2grid((19, 2), (13, 1), colspan=1, rowspan=1)
    ax9 = plt.subplot2grid((20, 6), (12, 0), colspan=1, rowspan=4)
    ax10 = plt.subplot2grid((20, 6), (12, 1), colspan=1, rowspan=4)
    ax11 = plt.subplot2grid((20, 6), (12, 2), colspan=1, rowspan=4)
    ax12 = plt.subplot2grid((20, 6), (12, 3), colspan=1, rowspan=4)
    ax13 = plt.subplot2grid((20, 6), (12, 4), colspan=1, rowspan=4)
    ax14 = plt.subplot2grid((20, 6), (12, 5), colspan=1, rowspan=4)

    ax15 = plt.subplot2grid((20, 6), (16, 0), colspan=1, rowspan=4)
    ax16 = plt.subplot2grid((20, 6), (16, 1), colspan=1, rowspan=4)
    ax17 = plt.subplot2grid((20, 6), (16, 2), colspan=1, rowspan=4)
    ax18 = plt.subplot2grid((20, 6), (16, 3), colspan=1, rowspan=4)
    ax19 = plt.subplot2grid((20, 6), (16, 4), colspan=1, rowspan=4)
    ax20 = plt.subplot2grid((20, 6), (16, 5), colspan=1, rowspan=4)

    full_df = make_match_df(pay_df)
    ccg_df = make_match_df(ccg_pay_df)
    trust_df = make_match_df(trust_pay_df)
    nhsengland_df = make_match_df(nhsengland_pay_df)
    full_venn = make_vennlist(pay_df)
#    trust_venn = make_vennlist(trust_pay_df)
    #    ccg_venn = make_vennlist(ccg_pay_df)

    #make venn
    v = venn3(subsets=(full_venn[0], full_venn[1], full_venn[2],
                       full_venn[3], full_venn[4], full_venn[5],
                       full_venn[6]),
              set_labels=('Charity    \nCommission   ',
                          'Companies House',
                          'NHS Digital'), alpha=0.8, ax=ax2)
    v.get_patch_by_id('100').set_color(colors[3])
    v.get_patch_by_id('010').set_color(colors[0])
    v.get_patch_by_id('001').set_color(colors[2])
    v.get_patch_by_id('110').set_color(colors[1])
    v.get_patch_by_id('101').set_color(colors[4])
    v.get_patch_by_id('011').set_color(colors[5])
    v.get_patch_by_id('111').set_color('w')
    v.get_label_by_id('101').set_text('')
    v.get_label_by_id('011').set_text('')
    v.get_label_by_id('010').set_text('')
    v.get_label_by_id('100').set_text('')
    v.get_label_by_id('001').set_text('')
    v.get_label_by_id('110').set_text('')
    v.get_label_by_id('111').set_text('')

#    for uid in ['100', '010', '001', '110', '101', '011', '111', '101', '011', '010', '100', '100', '001', '110', '111']:
#        v.get_label_by_id(uid).set_position((12, 12))
    for t in v.set_labels:
        t.set_fontsize(12)
    for t in v.subset_labels:
        t.set_fontsize(12)
    c = venn3_circles(subsets=(full_venn[0], full_venn[1], full_venn[2],
                               full_venn[3], full_venn[4], full_venn[5],
                               full_venn[6]),
                      linestyle='--', linewidth=1, ax=ax2,  color="k")
#    v.get_label_by_id("100").set_position((35.1, 122.2))
#    print(dir(v.get_label_by_id('010')))
    ax2.annotate(str(full_venn[6]) + ' suppliers on all three registers',
                 xy=v.get_label_by_id('111').get_position(),
                 fontsize=10, xytext=(+95, -105), **csfont,
                 ha='center', textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.5', ec='k', fc='w', alpha=1, linewidth=0.5),
                 arrowprops=dict(arrowstyle='->', color='k', linewidth=0.75,
                                 connectionstyle='arc3,rad=-0.75'))
    ax2.set_title('b.', fontsize=20, y=1.0, **csfont, loc='left')
    #ax2.set_title('Institutional overlap', fontsize=16,y=1.025, **csfont, loc='right')

    # make bars
    sns.set_style("ticks")
    short_df_trust = trust_df.groupby(['Type'])[['Number Suppliers',
                                                 'Payment Value',
                                                 'Number Payments']].agg('sum')
    short_df_ccg = ccg_df.groupby(['Type'])[['Number Suppliers',
                                             'Payment Value',
                                             'Number Payments']].agg('sum')
    short_df_nhsengland = nhsengland_df.groupby(['Type'])[['Number Suppliers',
                                                           'Payment Value',
                                                           'Number Payments']].agg('sum')
    short_df_full = full_df.groupby(['Type'])[['Number Suppliers',
                                               'Payment Value',
                                               'Number Payments']].agg('sum')
    short_df_trust = short_df_trust.T
    short_df_ccg = short_df_ccg.T
    short_df_nhsengland = short_df_nhsengland.T
    short_df_full = short_df_full.T
    short_df_full = short_df_full*100
    short_df_ccg = short_df_ccg*100
    short_df_trust = short_df_trust*100
    short_df_nhsengland = short_df_nhsengland*100
    short_df_full = (short_df_full.div(short_df_full.sum(axis=1), axis=0))*100
    short_df_trust = (short_df_trust.div(short_df_trust.sum(axis=1), axis=0))*100
    short_df_ccg = (short_df_ccg.div(short_df_ccg.sum(axis=1), axis=0))*100
    short_df_nhsengland = (short_df_nhsengland.div(short_df_nhsengland.sum(axis=1), axis=0))*100
    #make first set of bars: ccgs
    a = short_df_ccg['NHS'].plot(kind='bar', color=colors, alpha=1,
                                 linewidth=1.25, width=0.65, edgecolor='k', ax=ax3)
    b = short_df_ccg['No Match'].plot(kind='bar', color=colors, alpha=1,
                                      linewidth=1.25, width=0.65, edgecolor='k',
                                      ax=ax4)
    c = short_df_ccg['Company'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax5)
    d = short_df_ccg['Doctor'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax6)
    e = short_df_ccg['Charity'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax7)
    f = short_df_ccg['Person'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax8)
    sup = patches.Patch(facecolor=colors[0], label='# Suppliers',
                       alpha=1,edgecolor='k',linewidth=1)
    val = patches.Patch(facecolor=colors[1], label='Value (£)',
                          alpha=1,edgecolor='k',linewidth=1)
    count = patches.Patch(facecolor=colors[2], label='# Payments',
                          alpha=1,edgecolor='k',linewidth=1)
#    ax8.legend(handles=[sup, val, count], loc=2,fontsize=11, edgecolor='k',
#               frameon=False)#, fancybox=True, framealpha=1)
    for axy in [a, b, c, d, e, f]:
        axy.set_ylim(0, short_df_ccg.max().max()+5)
        axy.get_xaxis().set_ticks([])
        for p in axy.patches:
            axy.annotate(str(round(p.get_height(),1))+'%', (p.get_x(),
                                                            p.get_height() + 2.5), fontsize=9)
        if axy!=a:
            sns.despine(ax=axy, left=True, bottom = False, right = True)
            axy.get_yaxis().set_visible(False)
        else:
            sns.despine(ax=axy, left=False, bottom = False, right = True)
            axy.set_ylabel("CCG",fontsize=12)
            axy.yaxis.set_major_formatter(ticker.PercentFormatter())

    # make trusts
    g = short_df_trust['NHS'].plot(kind='bar', color=colors, alpha=1,
                                 linewidth=1.25, width=0.65, edgecolor='k', ax=ax9)
    h = short_df_trust['No Match'].plot(kind='bar', color=colors, alpha=1,
                                      linewidth=1.25, width=0.65, edgecolor='k',
                                      ax=ax10)
    i = short_df_trust['Company'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax11)
    j = short_df_trust['Doctor'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax12)
    k = short_df_trust['Charity'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax13)
    l = short_df_trust['Person'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax14)
    sup = patches.Patch(facecolor=colors[0], label='# Suppliers',
                       alpha=1,edgecolor='k',linewidth=1)
    val = patches.Patch(facecolor=colors[1], label='Value (£)',
                          alpha=1,edgecolor='k',linewidth=1)
    count = patches.Patch(facecolor=colors[2], label='# Payments',
                          alpha=1,edgecolor='k',linewidth=1)
    for axy in [g, h, i, j, k, l]:
        axy.set_ylim(0, short_df_trust.max().max()+5)
        axy.get_xaxis().set_ticks([])
        for p in axy.patches:
            axy.annotate(str(round(p.get_height(),1))+'%', (p.get_x(),
                                                            p.get_height() + 2.5), fontsize=9)
        if axy!=g:
            sns.despine(ax=axy, left=True, bottom = False, right = True)
            axy.get_yaxis().set_visible(False)
        else:
            sns.despine(ax=axy, left=False, bottom = False, right = True)
            axy.set_ylabel("NHS Trust",fontsize=12)
            axy.yaxis.set_major_formatter(ticker.PercentFormatter())
#    ax14.legend(handles=[sup, val, count], loc=2,fontsize=11, edgecolor='k',
#               frameon=False)#, fancybox=True, framealpha=1)


    # make nhsengland
    m = short_df_nhsengland['NHS'].plot(kind='bar', color=colors, alpha=1,
                                 linewidth=1.25, width=0.65, edgecolor='k', ax=ax15)
    n = short_df_nhsengland['No Match'].plot(kind='bar', color=colors, alpha=1,
                                      linewidth=1.25, width=0.65, edgecolor='k',
                                      ax=ax16)
    o = short_df_nhsengland['Company'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax17)
    p = short_df_nhsengland['Doctor'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax18)
    q = short_df_nhsengland['Charity'].plot(kind='bar', color=colors, alpha=1,
                                     linewidth=1.25, width=0.65, edgecolor='k',
                                     ax=ax19)
    r = short_df_nhsengland['Person'].plot(kind='bar', color=colors, alpha=1,
                                    linewidth=1.25, width=0.65, edgecolor='k',
                                    ax=ax20)
    sup = patches.Patch(facecolor=colors[0], label='# Suppliers',
                       alpha=1,edgecolor='k',linewidth=1)
    val = patches.Patch(facecolor=colors[1], label='Value (£)',
                          alpha=1,edgecolor='k',linewidth=1)
    count = patches.Patch(facecolor=colors[2], label='# Payments',
                          alpha=1,edgecolor='k',linewidth=1)
    m.set_xlabel("NHS",fontsize=15,labelpad=8)
    n.set_xlabel("No Match",fontsize=15,labelpad=8)
    o.set_xlabel("Company",fontsize=15,labelpad=8)
    p.set_xlabel("Doctor",fontsize=15,labelpad=8)
    q.set_xlabel("Charity",fontsize=15,labelpad=8)
    r.set_xlabel("Person",fontsize=15,labelpad=8)
    for axy in [m, n, o, p, q, r]:
        axy.set_ylim(0, short_df_nhsengland.max().max()+5)
        axy.get_xaxis().set_ticks([])
        for p in axy.patches:
            axy.annotate(str(round(p.get_height(),1))+'%', (p.get_x(),
                                                            p.get_height() + 2.5), fontsize=9)
        if axy!=m:
            sns.despine(ax=axy, left=True, bottom = False, right = True)
            axy.get_yaxis().set_visible(False)
        else:
            sns.despine(ax=axy, left=False, bottom = False, right = True)
            axy.set_ylabel("NHS England",fontsize=12)
            axy.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax20.legend(handles=[sup, val, count], loc=2,fontsize=11, edgecolor='k',
                framealpha=1)
    legend = ax20.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    ax3.set_title('c.', fontsize=20, y=1.05, **csfont, loc='left')
#    ax9.set_title('D.', fontsize=20, y=1.05, **csfont, loc='left')
#    ax15.set_title('E.', fontsize=20, y=1.05, **csfont, loc='left')
#    ax5.set_title('Payments mapped to a single register',
    #                  fontsize=16, y=1.05, **csfont, loc='center', x=1.1)


#    ax9.set_title('D.', fontsize=17, y=1.025, **csfont, loc='left')
#    ax11.set_title('Trust payments to institutions mapped to one register',
#                   fontsize=16,y=1.05, **csfont, loc='center', x=1.5)

    # make pie
    short_df_full = short_df_full[['Charity', 'Company', 'Doctor', 'NHS', 'Person', 'No Match']]
    labels = []
    for col in short_df_full.columns:
        labels.append(col + ' (£)')
    sizes = short_df_full.loc['Payment Value', :].tolist()
    explode = (0.25, 0.05, 0.05, 0.05, 0.05, 0.05)
    ax1.pie(sizes, explode=explode, labels=labels, colors=['#2ACF20', '#E89818','#1856E8', '#41558c', '#8C5E41', '#CF202A'],
            wedgeprops=dict(width=0.25), autopct='%1.1f%%', shadow=False,
            pctdistance=0.5)

    ax1.set_title('a.', fontsize=20, y=1.0, **csfont, loc='left')
#    ax1.set_title('Value based distribution', fontsize=16,
#                  y=1.03, **csfont, loc='center')
    wedges = [patch for patch in ax1.patches if isinstance(patch, patches.Wedge)]
    for w in wedges:
        w.set_linewidth(0.52)
        w.set_edgecolor('k')
    centre_circle = plt.Circle((0,0), 0.75, color='black', fc='white',linewidth=.25)
    ax1.axis('equal')
    sns.despine(ax=axfake1, top=True, left=True, right=True, bottom=True)
    #sns.despine(ax=axfake2, top=True, left=True, right=True, bottom=True)
    axfake1.set_xticks([])
    axfake1.set_yticks([])
    fig.subplots_adjust(hspace=50)
#    plt.tight_layout()
#    axfake2.set_xticks([])
#    axfake2.set_yticks([])
    plt.savefig(os.path.join(figure_path, 'match_distribution.png'),
                dpi=600)
    plt.savefig(os.path.join(figure_path, 'match_distribution.pdf'))
    plt.savefig(os.path.join(figure_path, 'match_distribution.svg'))
    plt.show()
    



### RnR figures

def scoring_figures(sup_df, figure_path, figsizetuple):
    """plot the scoring figures"""
    legend_fontsize = 17
    csfont = {'fontname':'Helvetica'}

    from matplotlib.collections import LineCollection
    from matplotlib.lines import Line2D
    colors = ['#41558c', '#E89818', '#CF202A']
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ['white', colors[0], colors[1], colors[2]])
    fig = plt.figure(figsize=figsizetuple)
    ax1 = plt.subplot2grid((3, 12), (0, 0), colspan=4)
    ax2 = plt.subplot2grid((3, 12), (0, 4), colspan=4)
    ax3 = plt.subplot2grid((3, 12), (0, 8), colspan=4)
    ax5 = plt.subplot2grid((3, 12), (1, 0), colspan=6)
    ax4 = plt.subplot2grid((3, 12), (1, 6), colspan=6)
    ax8 = plt.subplot2grid((3, 12), (2, 0), colspan=4)
    ax9 = plt.subplot2grid((3, 12), (2, 4), colspan=4)
    ax10 = plt.subplot2grid((3, 12), (2, 8), colspan=4)
    axins1 = inset_axes(ax1, width="25%", height="5%", loc='lower right')
    im1 = ax1.hexbin(sup_df['score_0'], sup_df['score_0_n'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im1, cax=axins1, orientation="horizontal")
    axins1.xaxis.set_ticks_position("top")
    ax1.set_xlabel('ES$^1_r$', fontsize=legend_fontsize, **csfont)
    ax1.set_ylabel('ES$^1_n$', fontsize=legend_fontsize, **csfont)
    #ax1.set_title('Best Match: ES', fontsize=legend_fontsize+2, y=1.025)
    ax1.set_title('a.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    axins2 = inset_axes(ax2, width="25%", height="5%", loc='lower right')
    im2 = ax2.hexbin(sup_df['match_0_lev'], sup_df['match_0_n_lev'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
#    ax2.set_title('Best Match: Lev.', fontsize=legend_fontsize+2, y=1.025)
    ax2.set_title('b.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax2.set_xlabel(r'$\mathcal{L}^1_r$', fontsize=legend_fontsize, **csfont)
    ax2.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize, **csfont)
    fig.colorbar(im2, cax=axins2, orientation="horizontal")
    axins2.xaxis.set_ticks_position("top")
    axins3 = inset_axes(ax3, width="25%", height="5%", loc='lower right')
    im3 = ax3.hexbin(sup_df['score_0_n'], sup_df['match_0_n_lev'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
    ax3.set_xlabel(r'ES$^1_n$', fontsize=legend_fontsize+4, **csfont)
#    ax3.set_title('Best Match: Lev. vs. ES', fontsize=legend_fontsize+2, y=1.025)
    ax3.set_title('c.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax3.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize, **csfont)
    fig.colorbar(im3, cax=axins3, orientation="horizontal")
    axins3.xaxis.set_ticks_position("top")

    a = sns.distplot(sup_df[sup_df['score_0'].notnull()]['score_0'], ax=ax4,
                     kde_kws={'gridsize': 500,
                              'color': colors[0], 'alpha': 1,
                              'linestyle': '--'},
                     hist=False, label='ES$^1_r$', bins=np.arange(0, 60, 1))
    a = sns.distplot(sup_df[sup_df['score_0_n'].notnull()]['score_0_n'],
                     ax=ax4, hist=False, label='ES$^1_n$',
                     kde_kws={'gridsize': 500, 'linestyle': '-',
                              'color': colors[1], 'alpha': 1},
                     bins=np.arange(0, 60, 1))
    a.set_xlim(0, 50)
    #ax4.set_title('Best Match: Elastic Search', fontsize=legend_fontsize+2, y=1.025)
    ax4.set_title('e.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax4.set_xlabel('Elasticsearch Score', fontsize=legend_fontsize, **csfont)
    ax4.set_ylabel('Probability Density', fontsize=legend_fontsize, **csfont)
    b = sns.distplot(sup_df[sup_df['match_0_lev'].notnull()]['match_0_lev'],
                     kde_kws={'gridsize': 500,
                              'color': colors[0], 'linestyle': '--',
                              'alpha': 1},
                     hist=False, label=r'$\mathcal{L}^1_r$',
                     bins=np.arange(0, 100, 1), ax=ax5)
    b = sns.distplot(sup_df[sup_df['match_0_n_lev'].notnull()]['match_0_n_lev'],
                     ax=ax5, kde_kws={'gridsize': 500,
                                      'color': colors[1], 'linestyle': '-',
                                      'alpha': 1},
                     hist=False, label=r'$\mathcal{L}^1_n$',
                     bins=np.arange(0, 100, 1))
    b.set_xlim(0, 150)
    #ax5.set_title('Best Match: Levenshtein Distance', fontsize=legend_fontsize+2, y=1.025)
    ax5.set_title('d.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax5.set_xlabel('Levenshtein Distance', fontsize=legend_fontsize, **csfont)
    ax5.set_ylabel('Probability Density', fontsize=legend_fontsize, **csfont)
    ax8.set_title('f.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    axins8 = inset_axes(ax8,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im8 = ax8.hexbin(sup_df['score_1'], sup_df['score_1_n'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im8, cax=axins8, orientation="horizontal")
    axins8.xaxis.set_ticks_position("top")
    ax8.set_xlabel('ES$^2_r$', fontsize=legend_fontsize)
    ax8.set_ylabel('ES$^2_n$', fontsize=legend_fontsize)

    axins9 = inset_axes(ax9,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im9 = ax9.hexbin(sup_df['match_1_lev'], sup_df['match_1_n_lev'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im9, cax=axins9, orientation="horizontal")
    axins9.xaxis.set_ticks_position("top")
#    ax9.set_title('2nd Match: Lev.', fontsize=legend_fontsize+2, y=1.025)
    ax9.set_title('g.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax9.set_xlabel(r'$\mathcal{L}^2_r$', fontsize=legend_fontsize)
    ax9.set_ylabel(r'$\mathcal{L}^2_n$', fontsize=legend_fontsize)
#    ax9.set_xlim(0, 150)

    axins10 = inset_axes(ax10,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im10 = ax10.hexbin(sup_df['score_1_n'], sup_df['match_1_n_lev'],
                     cmap=cmap, gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im10, cax=axins10, orientation="horizontal")
    axins10.xaxis.set_ticks_position("top")
#    ax10.set_title('2nd Match: Lev. vs ES', fontsize=legend_fontsize+2, y=1.025)
    ax10.set_title('h.', fontsize=legend_fontsize+6, loc='left', y=1.025, x=-.025, **csfont)
    ax10.set_ylabel('ES$^2_n$', fontsize=legend_fontsize)
    ax10.set_xlabel(r'$\mathcal{L}^2_n$', fontsize=legend_fontsize)
    for ax in [ax1, ax2, ax3, ax4, ax5,# ax6, ax7,
               ax8, ax9, ax10]:
        ax.grid(linestyle='--', linewidth='1',
                color='gray', alpha=0.1)
    for ax in [ax1, ax2, ax3, ax8, ax9, ax10]:
        ax.set_ylim(0,)
        ax.set_xlim(0,)
    for ax in [a, b]: #c, d]:
        ax.legend(edgecolor='w', frameon=True, fontsize=legend_fontsize-1)

    legend = ax4.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')

    legend = ax5.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')


    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'matching_summary.png'), dpi=600)
    plt.savefig(os.path.join(figure_path, 'matching_summary.pdf'))
    plt.savefig(os.path.join(figure_path, 'matching_summary.svg'))
