import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import matplotlib.ticker as ticker
import matplotlib as mpl
import os
from matplotlib_venn import venn3, venn3_circles
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25

github_url = 'https://github.com/google/roboto/blob/master/src/hinted/Roboto-Light.ttf'

url = github_url + '?raw=true'  # You want the actual file, not some html

response = urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

mpl.rc('font', family='sans-serif')
mpl.rc('font', serif=f.name)
mpl.rc('text', usetex='false')
#matplotlib.rcParams.update({'font.size': 20})


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


def check_payments(df, filecheck_path, data_path, orgtype, number_to_check=25):
    checker = pd.read_csv(filecheck_path)
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


def make_table_one(ccg_pay_df, trust_pay_df, table_path):
    ccg_clean = make_onetable(ccg_pay_df)
    trusts_clean = make_onetable(trust_pay_df)
    df_out = pd.concat([ccg_clean, trusts_clean], axis=1)
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
    titlefont = 19
    letterfont = 20
    labelfont = 14
    mpl.rc('font',family='Helvetica')
    cwd = os.getcwd()
    csfont = {'fontname':'Helvetica'}
    hfont = {'fontname':'Helvetica'}
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

    fig = plt.figure(figsize=(14, 13))
    ax1 = plt.subplot2grid((12, 2), (0, 0), colspan=1, rowspan=6)
    ax2 = plt.subplot2grid((12, 2), (0, 1), colspan=1, rowspan=6)
    ax3 = plt.subplot2grid((12, 2), (6, 0), colspan=1, rowspan=6)
    ax4 = plt.subplot2grid((12, 2), (6, 1), colspan=1, rowspan=3)
    ax5 = plt.subplot2grid((12, 2), (9, 1), colspan=1, rowspan=3)

    trusts_above = trusts[trusts['actual']>0][['plan', 'actual']]
    trusts_below = trusts[trusts['actual']<=0][['plan', 'actual']]
    ee = trusts_above[['plan', 'actual']].plot.scatter(x='plan', y='actual',
                                                 ax=ax1, edgecolor='k',
                                                 s=50, alpha=0.5,
                                                 label='NHS Trust in Deficit')
    ee = trusts_below[['plan', 'actual']].plot.scatter(x='plan', y='actual',
                                                 ax=ax1, edgecolor='k',
                                                 s=50, alpha=0.5,
                                                 color='r',
                                                 label='NHS Trust in Surplus')
    ee.axhline(y=0.0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
    ee.axvline(x=0.0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
    ee.xaxis.set_ticks_position('none')
    ee.legend(edgecolor='k', fontsize=labelfont-4, loc='lower right')
    ee.yaxis.set_ticks_position('none')
    ee.set_xlabel('Planned deficit/surplus (£m)', **hfont, fontsize=labelfont)
    ee.set_ylabel('Actual deficit/surplus (£m)', **hfont, fontsize=labelfont)
    ee.set_title('NHS Trust accounts: 2018/2019', fontsize=titlefont,y=1.01)
    ee.set_title('A.', fontsize=letterfont, loc='left')
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
                    edgecolor='k', alpha=0.5, bins=14,
                    label='Overspend',
                    color='#e50000')
    inset_axes.yaxis.set_label_position('right')
    inset_axes.set_ylabel('Frequency')
    inset_axes.patches[-1].set_color('#4C72B0')
    inset_axes.patches[-1].set_alpha(0.5)
    inset_axes.patches[-1].set_label('Underspend')
    inset_axes.patches[-1].set_edgecolor('k')
    lines, labels = inset_axes.get_legend_handles_labels()
    inset_axes.legend(lines, labels,
                      edgecolor='w', fontsize=labelfont-4,
                      loc='upper left')
    formatter = ticker.FormatStrFormatter('£%1.0fm')
    inset_axes.xaxis.set_major_formatter(formatter)
    sns.despine(ax=inset_axes, left=True, right=False, top=True)

    ff = sns.regplot(x='share', y='ppp',
                     data=oecd_trim, ax=ax2,
                     scatter_kws={'s':40, 'edgecolor':'k',
                                  'alpha':0.66},
                     line_kws = {'color': '#e50000',
                                 'alpha': 0.5},
                     ci=68)
    ff.set_title('International spending: 2018/2019',
                 fontsize=titlefont,y=1.01)
    ff.set_title('B.', fontsize=letterfont, loc='left')
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
    vals = ff.get_yticks()
    ff.set_yticklabels(['{:,.2%}'.format(x/100) for x in vals])

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
    gg.set_title('NHS Spending as % GDP over time', fontsize=titlefont,y=1.01)
    gg.set_title('C.', fontsize=letterfont, loc='left')
    gg.set_ylim(3, 9)
    gg.set_xlim(1985, 2019)
    formatter = ticker.FormatStrFormatter('£%1.0fbn')
    gg.yaxis.set_major_formatter(formatter)
    vals = gg.get_yticks()
    gg.set_yticklabels(['{:,.2%}'.format(x/100) for x in vals])
    gg.set_xlabel('', **hfont, fontsize=labelfont)
    gg.set_ylabel('Percent of Spending (%)', **hfont, fontsize=12)
    gg.annotate('Thatcher\Major', xy=(1991.75, 4.85),
                xytext=(1991.75, 5.1),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=5.4, lengthB=1',
                                lw=1.0))
    gg.annotate('Blair\Brown', xy=(2003.25, 7.55),
                xytext=(2003.25, 7.75),# xycoords='axes fraction',
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=6.8, lengthB=1', lw=1.0))
    gg.annotate('Cameron\Osbourne', xy=(2012.4, 7.9), xytext=(2012.4, 8.1),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=2.6, lengthB=1', lw=1.0))
    gg.annotate('Cameron\May', xy=(2017.5, 8.5), xytext=(2017.5, 8.7),
                fontsize=labelfont-2, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white', ec='w'),
                arrowprops=dict(arrowstyle='-[, widthB=2.35, lengthB=1', lw=1.0))
    lines, labels = gg.get_legend_handles_labels()
    gg.legend(lines, labels,
              edgecolor='w',
              fontsize=labelfont-2, loc='upper left')
    hh = sns.distplot(alloc['Final allocation'], ax=ax4,
                      kde_kws={"color": "#fc8d62",
                      "lw": 2, "label": "Kernel Density Estimate",
                      "alpha": 1},
                     hist_kws={"alpha": 0.5,
                               "label": "Frequency",
                               'edgecolor': 'k'})
    hh.set_xlabel('', **hfont, fontsize=12)
    ii = sns.distplot(alloc['Per capita allocation'],
                      ax=ax5,
                      kde_kws={"color": "#fc8d62", "lw": 2,
                               "label": "Kernel Density Estimate",
                               "alpha": 1},
                     hist_kws={"alpha": 0.5, "label": "Frequency",
                               'edgecolor': 'k'})
    formatter = ticker.FormatStrFormatter('%.3f')
    hh.yaxis.set_major_formatter(formatter)
    formatter = ticker.FormatStrFormatter('£%1.0fm')
    hh.xaxis.set_major_formatter(formatter)
    ii.legend(edgecolor='w', fontsize=labelfont-1)
    hh.legend(edgecolor='w', fontsize=labelfont-1)
    hh.set_title('Distribution of CCG allocations: 2019/2020',
                 fontsize=titlefont,y=1.01)
    hh.set_title('D.', fontsize=letterfont, loc='left')
    ii.set_title('CCG allocations per capita: 2019/2020', fontsize=titlefont,y=1.01)
    ii.set_title('E.', fontsize=letterfont, loc='left')
    ii.xaxis.set_major_formatter(formatter)
    ii.set_xlabel('', **hfont, fontsize=12)
    formatter = ticker.FormatStrFormatter('£%1.0f')
    ii.xaxis.set_major_formatter(formatter)

    sns.despine(ax=ax1, left=True, bottom=True)
    sns.despine(ax=ax2)
    sns.despine(ax=gg)
    sns.despine(ax=ax4)
    sns.despine(ax=ax5)
    plt.tight_layout(True)
    plt.subplots_adjust(hspace=500)
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.pdf'))
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.png'), dpi=500)
    plt.savefig(os.path.join(figure_path, 'nhs_spending_macro.svg'))

def load_suppliers(sup_path):
    sup_df = pd.read_csv(sup_path, sep='\t')
    return sup_df


def load_payments(pay_path):
    pay_df = pd.read_csv(pay_path, sep='\t',
                         usecols=['expensetype', 'supplier', 'date', 'dept',
                                  'amount', 'file', 'expensearea',
                                  'transactionnumber', 'verif_match',
                                  'query_string_n',
                                  'match_type'],
                         dtype={'query_string_n': str,
                                'verif_match': str,
                                'match_type': str,
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


def summarize_payments(pay_df, payment_type):
    print('Describing cleaned ' + payment_type + ' payments dataset!')
    print('Length of dataset:', len(pay_df))
    print('Total unique raw suppliers:', len(pay_df['supplier'].unique()))
    print('Total unique verified suppliers:', len(pay_df['verif_match'].unique()))
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
          '(£'+ str(int(value_dept[0])) + ')')
    most_supp = pay_df.groupby(['supplier']).size().sort_values(ascending=False)
    print('Most payments:', most_supp.index[0],
          '('+ str(most_supp[0]) + ')')
    value_supp = pay_df.groupby('supplier')['amount'].sum().sort_values(ascending=False)
    print('Highest value of payments is:', value_supp.index[0],
          '('+ str(value_supp[0]) + ')')
    print('Number of organisations in clean dataset is: ' +\
          str(len(pay_df['dept'].unique())))
    print('Number of files in clean dataset is: ' +\
          str(len(pay_df[['dept','file']].drop_duplicates()['file'].unique())))


def scoring_figures(sup_df, figure_path, figsizetuple):
    """plot the scoring figures"""
    legend_fontsize = 16
    fig = plt.figure(figsize=figsizetuple)
    ax1 = plt.subplot2grid((3, 12), (0, 0), colspan=4)
    ax2 = plt.subplot2grid((3, 12), (0, 4), colspan=4)
    ax3 = plt.subplot2grid((3, 12), (0, 8), colspan=4)
    ax5 = plt.subplot2grid((3, 12), (1, 0), colspan=6)
    ax4 = plt.subplot2grid((3, 12), (1, 6), colspan=6)
#    ax6 = plt.subplot2grid((3, 12), (1, 6), colspan=3)
#    ax7 = plt.subplot2grid((3, 12), (1, 9), colspan=3)
    ax8 = plt.subplot2grid((3, 12), (2, 0), colspan=4)
    ax9 = plt.subplot2grid((3, 12), (2, 4), colspan=4)
    ax10 = plt.subplot2grid((3, 12), (2, 8), colspan=4)
    axins1 = inset_axes(ax1, width="25%", height="5%", loc='lower right')
    im1 = ax1.hexbin(sup_df['score_0'], sup_df['score_0_n'],
                     cmap='Oranges', gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im1, cax=axins1, orientation="horizontal")
    axins1.xaxis.set_ticks_position("top")
    ax1.set_xlabel('ES$^1_r$', fontsize=legend_fontsize)
    ax1.set_ylabel('ES$^1_n$', fontsize=legend_fontsize)
    ax1.set_title('Best Match: ES', fontsize=legend_fontsize+4, y=1.01)
    ax1.set_title('A.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    axins2 = inset_axes(ax2, width="25%", height="5%", loc='lower right')
    im2 = ax2.hexbin(sup_df['match_0_lev'], sup_df['match_0_n_lev'],
                     cmap='Oranges', gridsize=28, bins='log', mincnt=1)
    ax2.set_title('Best Match: Lev.', fontsize=legend_fontsize+4, y=1.01)
    ax2.set_title('B.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    ax2.set_xlabel(r'$\mathcal{L}^1_r$', fontsize=legend_fontsize)
    ax2.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize)
    fig.colorbar(im2, cax=axins2, orientation="horizontal")
    axins2.xaxis.set_ticks_position("top")
    axins3 = inset_axes(ax3, width="25%", height="5%", loc='lower right')
    im3 = ax3.hexbin(sup_df['score_0_n'], sup_df['match_0_n_lev'],
                     cmap='Oranges', gridsize=28, bins='log', mincnt=1)
    ax3.set_xlabel(r'ES$^1_n$', fontsize=legend_fontsize+4, y=1.01)
    ax3.set_title('Best Match: Lev. vs. ES', fontsize=legend_fontsize, y=1.01)
    ax3.set_title('C.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    ax3.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize)
    fig.colorbar(im3, cax=axins3, orientation="horizontal")
    axins3.xaxis.set_ticks_position("top")

    a = sns.distplot(sup_df[sup_df['score_0'].notnull()]['score_0'], ax=ax4,
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'alpha': 0.8,
                              'linestyle': '--'},
                     hist=False, label='ES$^1_r$', bins=np.arange(0, 60, 1))
    a = sns.distplot(sup_df[sup_df['score_0_n'].notnull()]['score_0_n'],
                     ax=ax4, hist=False, label='ES$^1_n$',
                     kde_kws={'gridsize': 500, 'linestyle': '-',
                              'color': '#377eb8', 'alpha': 0.8},
                     bins=np.arange(0, 60, 1))
    a.set_xlim(0, 50)
    ax4.set_title('Best Match: Elastic Search', fontsize=legend_fontsize+4, y=1.01)
    ax4.set_title('E.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    ax4.set_xlabel('Elasticsearch Score', fontsize=legend_fontsize)
    ax4.set_ylabel('Probability Density', fontsize=legend_fontsize)
    b = sns.distplot(sup_df[sup_df['match_0_lev'].notnull()]['match_0_lev'],
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'linestyle': '--',
                              'alpha': 0.8},
                     hist=False, label=r'$\mathcal{L}^1_r$',
                     bins=np.arange(0, 100, 1), ax=ax5)
    b = sns.distplot(sup_df[sup_df['match_0_n_lev'].notnull()]['match_0_n_lev'],
                     ax=ax5, kde_kws={'gridsize': 500,
                                      'color': '#377eb8', 'linestyle': '-',
                                      'alpha': 0.8},
                     hist=False, label=r'$\mathcal{L}^1_n$',
                     bins=np.arange(0, 100, 1))
    b.set_xlim(0, 150)
    ax5.set_title('Best Match: Levenshtein Distance', fontsize=legend_fontsize+4, y=1.01)
    ax5.set_title('D.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    ax5.set_xlabel('Levenshtein Distance', fontsize=legend_fontsize)
    ax5.set_ylabel('Probability Density', fontsize=legend_fontsize)
#    c = sns.distplot(sup_df[sup_df['score_1'].notnull()]['score_1'],
#                     kde_kws={'gridsize': 500,
#                              'color': '#ff7f00',
#                              'linestyle': '--',
#                              'alpha': 0.8},
#                     hist=False, ax=ax6, label=r'ES$^2_r$',
#                     bins=np.arange(0, 60, 1))
#    c = sns.distplot(sup_df[sup_df['score_1_n'].notnull()]['score_1_n'],
#                     kde_kws={'gridsize': 500, 'color': '#377eb8',
#                              'linestyle': '-',
#                              'alpha': 0.8},
#                     hist=False, ax=ax6, label='ES$^2_n$',
#                     bins=np.arange(0, 60, 1))
#    c.set_xlim(0, 40)
#    ax6.set_title('2nd Match: ES', fontsize=legend_fontsize)
#    ax6.set_title('F.', fontsize=legend_fontsize+5, loc='left', y=1.025)
#    ax6.set_xlabel('Elasticsearch Score', fontsize=legend_fontsize)
#    ax6.set_ylabel('Probability Density', fontsize=legend_fontsize)
#    d = sns.distplot(sup_df[sup_df['match_1_lev'].notnull()]['match_1_lev'],
#                     kde_kws={'gridsize': 500,
#                              'color':'#ff7f00',
#                              'linestyle': '--',
#                              'alpha': 0.8},
#                     hist=False, ax=ax7, label=r'$\mathcal{L}^2_r$',
#                     bins=np.arange(0, 100, 1))
#    d = sns.distplot(sup_df[sup_df['match_2_n_lev'].notnull()]['match_1_n_lev'],
#                     kde_kws={'gridsize': 500,
#                              'color': '#377eb8','linestyle': '-',
#                              'alpha': 0.8},
#                     hist=False, ax=ax7, label=r'$\mathcal{L}^2_n$',
#                     bins=np.arange(0, 100, 1))
#    ax7.set_title('2nd Match: Lev.', fontsize=legend_fontsize)
#    ax7.set_title('G.', fontsize=legend_fontsize+5, loc='left', y=1.025)
#    ax7.set_xlabel('Levenshtein Distance', fontsize=legend_fontsize)
#    ax7.set_ylabel('Probability Density', fontsize=legend_fontsize)
#    d.set_xlim(0, 175)

    ax8.set_title('2nd Match: ES', fontsize=legend_fontsize+4, y=1.01)
    ax8.set_title('H.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    axins8 = inset_axes(ax8,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im8 = ax8.hexbin(sup_df['score_1'], sup_df['score_1_n'],
                     cmap='Blues', gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im8, cax=axins8, orientation="horizontal")
    axins8.xaxis.set_ticks_position("top")
    ax8.set_xlabel('ES$^2_r$', fontsize=legend_fontsize)
    ax8.set_ylabel('ES$^2_n$', fontsize=legend_fontsize)

    axins9 = inset_axes(ax9,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im9 = ax9.hexbin(sup_df['match_1_lev'], sup_df['match_1_n_lev'],
                     cmap='Blues', gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im9, cax=axins9, orientation="horizontal")
    axins9.xaxis.set_ticks_position("top")
    ax9.set_title('2nd Match: Lev.', fontsize=legend_fontsize+4, y=1.01)
    ax9.set_title('I.', fontsize=legend_fontsize+6, loc='left', y=1.025)
    ax9.set_xlabel(r'$\mathcal{L}^2_r$', fontsize=legend_fontsize)
    ax9.set_ylabel(r'$\mathcal{L}^2_n$', fontsize=legend_fontsize)
#    ax9.set_xlim(0, 150)

    axins10 = inset_axes(ax10,
                        width="25%",  # width = 50% of parent_bbox width
                        height="5%",  # height : 5%
                        loc='lower right')
    im10 = ax10.hexbin(sup_df['score_1_n'], sup_df['match_1_n_lev'],
                     cmap='Blues', gridsize=28, bins='log', mincnt=1)
    fig.colorbar(im10, cax=axins10, orientation="horizontal")
    axins10.xaxis.set_ticks_position("top")
    ax10.set_title('2nd Match: Lev. vs ES', fontsize=legend_fontsize+4, y=1.01)
    ax10.set_title('J.', fontsize=legend_fontsize+6, loc='left', y=1.025)
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
        ax.legend(edgecolor='w', frameon=True, fontsize=legend_fontsize-3)
    sns.despine()
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'matching_summary.png'), dpi=600)
    plt.savefig(os.path.join(figure_path, 'matching_summary.pdf'))
    plt.savefig(os.path.join(figure_path, 'matching_summary.svg'))
    plt.show()


def plot_match_distribution(sup_df, pay_df, figure_path, figsize_tuple):
    #  legend_fontsize = 10
    fig = plt.figure(figsize=figsize_tuple)
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax2 = plt.subplot2grid((2, 2), (0, 1), colspan=1)
    ax3 = plt.subplot2grid((2, 6), (1, 0), colspan=1)
    ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=1)
    ax5 = plt.subplot2grid((2, 6), (1, 2), colspan=1)
    ax6 = plt.subplot2grid((2, 6), (1, 3), colspan=1)
    ax7 = plt.subplot2grid((2, 6), (1, 4), colspan=1)
    ax8 = plt.subplot2grid((2, 6), (1, 5), colspan=1)
    index = range(0, 18)
#    index = ['Charity', 'Company', 'NHS', 'Named', 'Doctor', 'No Match']
    cols = ['Type', 'Identification', 'Number Suppliers',
            'Payment Value', 'Number Payments']
    df = pd.DataFrame(columns=cols, index=index)
    char_num = len(sup_df[sup_df['match_type'] == 'Charity Commission'])
    char_count = len(pay_df[pay_df['match_type'] == 'Charity Commission'])
    char_val = pay_df[pay_df['match_type'] == 'Charity Commission']['amount'].sum()
    df.at[0, 'Type'] = 'Charity'
    df.at[0, 'Identification'] = 'Unique'
    df.at[0, 'Number Suppliers'] = char_num
    df.at[0, 'Number Payments'] = char_count
    df.at[0, 'Payment Value'] = char_val
    char_num_two = len(sup_df[(sup_df['match_type'].str.
                               contains('Charity Commission')) &
                              (sup_df['match_type'].str.count(':') == 1)])
    char_count_two = len(pay_df[(pay_df['match_type'].str.
                               contains('Charity Commission')) &
                              (pay_df['match_type'].str.count(':') == 1)])
    char_val_two = pay_df[(pay_df['match_type'].str.
                           contains('Charity Commission')) &
                          (pay_df['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[1, 'Type'] = 'Charity'
    df.at[1, 'Identification'] = 'Two Registers'
    df.at[1, 'Number Suppliers'] = char_num_two
    df.at[1, 'Number Payments'] = char_count_two
    df.at[1, 'Payment Value'] = char_val_two
    char_num_three = len(sup_df[(sup_df['match_type'].str.
                                 contains('Charity Commission')) &
                                (sup_df['match_type'].str.count(':') == 2)])
    char_count_three = len(pay_df[(pay_df['match_type'].str.
                                   contains('Charity Commission')) &
                                  (pay_df['match_type'].str.count(':') == 2)])
    char_val_three = pay_df[(pay_df['match_type'].str.
                             contains('Charity Commission')) &
                            (pay_df['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[2, 'Type'] = 'Charity'
    df.at[2, 'Identification'] = 'Three Registers'
    df.at[2, 'Number Suppliers'] = char_num_three
    df.at[2, 'Number Payments'] = char_count_three
    df.at[2, 'Payment Value'] = char_val_three

    comp_num = len(sup_df[sup_df['match_type'] == 'Companies House'])
    comp_count = len(pay_df[pay_df['match_type'] == 'Companies House'])
    comp_val = pay_df[pay_df['match_type'] == 'Companies House']['amount'].sum()
    df.at[3, 'Type'] = 'Company'
    df.at[3, 'Identification'] = 'Unique'
    df.at[3, 'Number Suppliers'] = comp_num
    df.at[3, 'Number Payments'] = comp_count
    df.at[3, 'Payment Value'] = comp_val
    comp_num_two = len(sup_df[(sup_df['match_type'].str.
                               contains('Companies House')) &
                              (sup_df['match_type'].str.count(':') == 1)])
    comp_count_two = len(pay_df[(pay_df['match_type'].str.
                               contains('Companies House')) &
                              (pay_df['match_type'].str.count(':') == 1)])
    comp_val_two = pay_df[(pay_df['match_type'].str.
                           contains('Companies House')) &
                          (pay_df['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[4, 'Type'] = 'Company'
    df.at[4, 'Identification'] = 'Three Registers'
    df.at[4, 'Number Suppliers'] = comp_num_two
    df.at[4, 'Number Payments'] = comp_count_two
    df.at[4, 'Payment Value'] = comp_val_two
    comp_num_three = len(sup_df[(sup_df['match_type'].str.
                                 contains('Companies House')) &
                                (sup_df['match_type'].str.count(':') == 2)])
    comp_count_three = len(pay_df[(pay_df['match_type'].str.
                                   contains('Companies House')) &
                                  (pay_df['match_type'].str.count(':') == 2)])
    comp_val_three = pay_df[(pay_df['match_type'].str.
                             contains('Companies House')) &
                            (pay_df['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[5, 'Type'] = 'Company'
    df.at[5, 'Identification'] = 'Two Registers'
    df.at[5, 'Number Suppliers'] = comp_num_three
    df.at[5, 'Number Payments'] = comp_count_three
    df.at[5, 'Payment Value'] = comp_val_three

    nhs_num = len(sup_df[sup_df['match_type'] == 'NHS Digital'])
    nhs_count = len(pay_df[pay_df['match_type'] == 'NHS Digital'])
    nhs_val = pay_df[pay_df['match_type'] == 'NHS Digital']['amount'].sum()
    df.at[6, 'Type'] = 'NHS'
    df.at[6, 'Identification'] = 'Unique'
    df.at[6, 'Number Suppliers'] = nhs_num
    df.at[6, 'Number Payments'] = nhs_count
    df.at[6, 'Payment Value'] = nhs_val
    nhs_num_two = len(sup_df[(sup_df['match_type'].str.
                              contains('NHS Digital')) &
                             (sup_df['match_type'].str.count(':') == 1)])
    nhs_count_two = len(pay_df[(pay_df['match_type'].str.
                               contains('NHS Digital')) &
                              (pay_df['match_type'].str.count(':') == 1)])
    nhs_val_two = pay_df[(pay_df['match_type'].str.
                           contains('NHS Digital')) &
                          (pay_df['match_type'].str.count(':') == 1)]['amount'].sum()
    df.at[7, 'Type'] = 'NHS'
    df.at[7, 'Identification'] = 'Two Registers'
    df.at[7, 'Number Suppliers'] = nhs_num_two
    df.at[7, 'Number Payments'] = nhs_count_two
    df.at[7, 'Payment Value'] = nhs_val_two
    nhs_num_three = len(sup_df[(sup_df['match_type'].str.
                                contains('NHS Digital')) &
                                (sup_df['match_type'].str.count(':') == 2)])
    nhs_count_three = len(pay_df[(pay_df['match_type'].str.
                                   contains('NHS Digital')) &
                                  (pay_df['match_type'].str.count(':') == 2)])
    nhs_val_three = pay_df[(pay_df['match_type'].str.
                             contains('NHS Digital')) &
                            (pay_df['match_type'].str.count(':') == 2)]['amount'].sum()
    df.at[8, 'Type'] = 'NHS'
    df.at[8, 'Identification'] = 'Three Registers'
    df.at[8, 'Number Suppliers'] = nhs_num_three
    df.at[8, 'Number Payments'] = nhs_count_three
    df.at[8, 'Payment Value'] = nhs_val_three

    dr_num = len(sup_df[sup_df['match_type'] == 'Named Doctor'])
    dr_count = len(pay_df[pay_df['match_type'] == 'Named Doctor'])
    dr_val = pay_df[pay_df['match_type'] == 'Named Doctor']['amount'].sum()
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

    per_num = len(sup_df[sup_df['match_type'] == 'Named Person'])
    per_count = len(pay_df[pay_df['match_type'] == 'Named Person'])
    per_val = pay_df[pay_df['match_type'] == 'Named Person']['amount'].sum()
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

    none_num = len(sup_df[sup_df['match_type'] == 'No Match'])
    none_count = len(pay_df[pay_df['match_type'] == 'No Match'])
    none_val = pay_df[pay_df['match_type'] == 'No Match']['amount'].sum()
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

    charcom_num = len(sup_df[(sup_df['match_type'].str.
                              contains('Charity Commission')) &
                             (sup_df['match_type'].str.
                              contains('Companies House'))])
    charnhs_num = len(sup_df[(sup_df['match_type'].str.
                              contains('Charity Commission')) &
                             (sup_df['match_type'].str.
                              contains('NHS Digital'))])
    comnhs_num = len(sup_df[(sup_df['match_type'].str.
                             contains('Companies House')) &
                            (sup_df['match_type'].str.
                             contains('NHS Digital'))])

    v = venn3(subsets=(char_num, comp_num, charcom_num, nhs_num,
                       charnhs_num, comnhs_num, char_num_three),
              set_labels=('Charity Commission',
                          'Companies House',
                          'NHS Digital'), alpha=0.8, ax=ax2)
    v.get_patch_by_id('100').set_color('#fff2ae')
    v.get_patch_by_id('010').set_color('#cbd5e8')
    v.get_patch_by_id('001').set_color('#fdcdac')
    v.get_patch_by_id('110').set_color('#b3e2cd')
    v.get_patch_by_id('101').set_color('#f4cae4')
    v.get_patch_by_id('011').set_color('#e6f5c9')
    v.get_patch_by_id('111').set_color('w')
    v.get_label_by_id('111').set_text('')
    for t in v.set_labels:
        t.set_fontsize(10)
    for t in v.subset_labels:
        t.set_fontsize(8)
    c = venn3_circles(subsets=(char_num, comp_num, charcom_num,
                               nhs_num, charnhs_num, comnhs_num,
                               char_num_three),
                      linestyle='--', linewidth=1, ax=ax2,  color="k")
#    v.get_label_by_id("100").set_position((35.1, 122.2))
#    print(dir(v.get_label_by_id('010')))
    ax2.annotate(str(char_num_three) + ' suppliers on\nall three registers',
                 xy=v.get_label_by_id('111').get_position(),
                 fontsize=9, xytext=(+100, -70),
                 ha='center', textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.5', ec='k', fc='w', alpha=1),
                 arrowprops=dict(arrowstyle='->', color='k', linewidth=0.75,
                                 connectionstyle='arc3,rad=-0.4'))
    ax2.set_title('B. Institutional overlap', fontsize=16,y=1.05)
#    df['Payment Value'] = df['Payment Value']/pay_df['amount'].sum()
#    df['Number Suppliers'] = df['Number Suppliers']/len(sup_df)
#    df['Number Payments'] = df['Number Payments']/len(pay_df)


    sns.set_style("ticks")
    colors = ['#377eb8', '#ff7f00', '#ffeda0']
    short_df = df.groupby(['Type'])['Number Suppliers',
                                    'Payment Value',
                                    'Number Payments'].agg('sum')
    short_df = short_df.T
    short_df = short_df*100
    short_df = (short_df.div(short_df.sum(axis=1), axis=0))*100
    a = short_df['NHS'].plot(kind='bar', color=colors, alpha=0.575,
                             linewidth=1.25, width=0.65, edgecolor='k', ax=ax3)
    b = short_df['No Match'].plot(kind='bar', color=colors, alpha=0.575,
                                  linewidth=1.25, width=0.65, edgecolor='k',
                             ax=ax4)
    c = short_df['Company'].plot(kind='bar', color=colors, alpha=0.575,
                                 linewidth=1.25, width=0.65, edgecolor='k',
                                 ax=ax5)
    d = short_df['Doctor'].plot(kind='bar', color=colors, alpha=0.575,
                                linewidth=1.25, width=0.65, edgecolor='k',
                                ax=ax6)
    e = short_df['Charity'].plot(kind='bar', color=colors, alpha=0.575,
                                 linewidth=1.25, width=0.65, edgecolor='k',
                                 ax=ax7)
    f = short_df['Person'].plot(kind='bar', color=colors, alpha=0.575,
                                linewidth=1.25, width=0.65, edgecolor='k',
                                ax=ax8)
    sup = patches.Patch(facecolor=colors[0], label='Number Suppliers',
                       alpha=0.575,edgecolor='k',linewidth=1)
    val = patches.Patch(facecolor=colors[1], label='Payment Value',
                          alpha=0.575,edgecolor='k',linewidth=1)
    count = patches.Patch(facecolor=colors[2], label='Number Payments',
                          alpha=0.575,edgecolor='k',linewidth=1)
    plt.legend(handles=[sup, val, count], loc=2,fontsize=11, edgecolor='k',
               frameon=False)#, fancybox=True, framealpha=1)
    a.set_xlabel("C. NHS",fontsize=15,labelpad=8)
    b.set_xlabel("D. No Match",fontsize=15,labelpad=8)
    c.set_xlabel("E. Company",fontsize=15,labelpad=8)
    d.set_xlabel("F. Doctor",fontsize=15,labelpad=8)
    e.set_xlabel("G. Charity",fontsize=15,labelpad=8)
    f.set_xlabel("H. Person",fontsize=15,labelpad=8)
    for axy in [a, b, c, d, e, f]:
        axy.set_ylim(0, short_df.max().max()+2)
        axy.get_xaxis().set_ticks([])
        for p in axy.patches:
            axy.annotate(str(round(p.get_height(),2))+'%', (p.get_x(),
                                                            p.get_height() + 1.6), fontsize=8)
        if axy!=a:
            sns.despine(ax=axy, left=True, bottom = False, right = True)
            axy.get_yaxis().set_visible(False)
        else:
            sns.despine(ax=axy, left=False, bottom = False, right = True)
            axy.set_ylabel("Percent of Total (%)",fontsize=12)
            axy.yaxis.set_major_formatter(ticker.PercentFormatter())
#            vals = axy.get_yticks()/100
#            print(vals)
#            axy.set_yticklabels(['{:,.0%}'.format(x) for x in axy.get_yticks()],fontsize=12)
#    ax3.set_title('C. NHS Digital', fontsize=13, y = 1.075)
#    ax4.set_title('D. Unmatched', fontsize=13, y = 1.075)
#    ax5.set_title('E. Companies', fontsize=13, y = 1.075)
#    ax6.set_title('F. Doctor', fontsize=13, y = 1.075)
#    ax7.set_title('G. Charity', fontsize=13, y = 1.075)
#    ax8.set_title('H. Individual', fontsize=13, y = 1.075)
    short_df = short_df[['Charity', 'Company', 'Doctor', 'NHS', 'Person', 'No Match']]
    labels = []
    for col in short_df.columns:
        labels.append(col + ' (£)')
    sizes = short_df.loc['Payment Value', :].tolist()
    colors = ['#b3e2cd', '#cbd5e8', '#f4cae4', '#fdcdac', '#e6f5c9', '#fff2ae']
    explode = (0.25, 0.05, 0.05, 0.05, 0.05, 0.05)
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            wedgeprops=dict(width=0.25), autopct='%1.1f%%', shadow=False,
            pctdistance=0.5)
    ax1.set_title('A. Value based distribution', fontsize=16,y=1.05)
    wedges = [patch for patch in ax1.patches if isinstance(patch, patches.Wedge)]
    for w in wedges:
        w.set_linewidth(0.52)
        #w.set_alpha(0.75)
        w.set_edgecolor('k')
    centre_circle = plt.Circle((0,0), 0.75, color='black', fc='white',linewidth=.25)

    ax1.axis('equal')
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'match_distribution.png'), dpi=600)
    plt.savefig(os.path.join(figure_path, 'match_distribution.pdf'))
    plt.savefig(os.path.join(figure_path, 'match_distribution.svg'))
    plt.show()
