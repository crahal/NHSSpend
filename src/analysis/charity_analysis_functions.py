import pandas as pd
from geopandas import GeoDataFrame
from geopandas import points_from_xy
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.ticker as mtick
from matplotlib.ticker import FormatStrFormatter
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import matplotlib.colors as colors
import pysal.viz.mapclassify as mc
from matplotlib.colors import rgb2hex
import geopandas as gpd
sys.path.append("..")
import matplotlib.gridspec as gridspec
mpl.font_manager._rebuild()
from reconciliation import normalizer

np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25


def more_or_less_by_age(cc_sup):
    print('Full sample:\n')
    now = pd.Timestamp('now')
    cc_sup_age = cc_sup[cc_sup['regdate'].notnull()]
    cc_sup_age['regdate'] = pd.to_datetime(cc_sup_age['regdate'],
                                           format='%m%d%y')
    cc_sup_age['age'] = (now - cc_sup_age['regdate']).astype('timedelta64[D]')
    print('Correlation between age and amount: ',
          cc_sup_age['age'].corr(cc_sup_age['amount']))
    print('Correlation between age and count:',
          cc_sup_age['age'].corr(cc_sup_age['count']))
    cc_sup_age['age_rank'] = cc_sup_age['age'].rank()
    cc_sup_age['amount_rank'] = cc_sup_age['amount'].rank()
    cc_sup_age['count_rank'] = cc_sup_age['count'].rank()
    print('Correlation between age and amount by rank: ',
          cc_sup_age['age_rank'].corr(cc_sup_age['amount_rank'],
                                      method='spearman'))
    print('Correlation between age and count by rank:',
          cc_sup_age['age_rank'].corr(cc_sup_age['count_rank'],
                                      method='spearman'))
    print('-------------------------------------------')
    print('Companies registered before 2012:\n')
    cc_sup_age1 = cc_sup_age[(cc_sup_age['regdate'].dt.year < 2012) |
                             (cc_sup_age['regdate'].isnull())]
    cc_sup_age1['regdate'] = pd.to_datetime(cc_sup_age1['regdate'],
                                            format='%m%d%y')
    cc_sup_age1['age'] = (now - cc_sup_age1['regdate']).astype('timedelta64[D]')
    print('Correlation between age and amount: ',
          cc_sup_age1['age'].corr(cc_sup_age1['amount']))
    print('Correlation between age and count:',
          cc_sup_age1['age'].corr(cc_sup_age1['count']))
    cc_sup_age1['age_rank'] = cc_sup_age1['age'].rank()
    cc_sup_age1['amount_rank'] = cc_sup_age1['amount'].rank()
    cc_sup_age1['count_rank'] = cc_sup_age1['count'].rank()
    print('Correlation betwen age and amount, by rank: ',
          cc_sup_age1['age_rank'].corr(cc_sup_age1['amount_rank'],
                                       method='spearman'))
    print('Correlation between age and count, by rank: ',
          cc_sup_age1['age_rank'].corr(cc_sup_age1['count_rank'],
                                       method='spearman'))


def plot_temporal(ts_ccg_annual, ts_trust_annual, ts_ccg_monthly,
                  ts_trust_monthly, ts_ccg_month, ts_trust_month,
                  figure_path):
    titlesize = 16
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    fig = plt.figure(figsize=(14,10))
    ax1 = plt.subplot2grid((12, 20), (0, 0), colspan=20, rowspan=3)
    ax2 = plt.subplot2grid((12, 20), (3, 0), colspan=20, rowspan=3)
    ax3 = plt.subplot2grid((12, 20), (6, 0), colspan=10, rowspan=3)
    ax4 = plt.subplot2grid((12, 20), (9, 0), colspan=10, rowspan=3)
    ax5 = plt.subplot2grid((12, 20), (6, 10), colspan=10, rowspan=3, sharey=ax3)
    ax6 = plt.subplot2grid((12, 20), (9, 10), colspan=10, rowspan=3, sharey=ax4)

    ax1.plot(ts_ccg_month['Year-Month'][6:], ts_ccg_month['Amount'][6:],
             color='#377eb8', alpha=0.8, marker='o', markersize=8, markerfacecolor='w',
             label='CCGs')
    ax1a = ax1.twinx()
    ax1a.plot(ts_trust_month['Year-Month'][6:], ts_trust_month['Amount'][6:], color='#ff7f00', alpha=0.8,
              marker='o', markersize=8, markerfacecolor='w', label='NHS Trusts')
    ax1.plot(np.nan, np.nan, color='#ff7f00', alpha=0.8,
              marker='o', markersize=8, markerfacecolor='w', label='NHS Trusts')

    ax2.plot(ts_ccg_month['Year-Month'][6:], ts_ccg_month['Count'][6:], color='#377eb8', alpha=0.8,
             marker='o', markersize=8, markerfacecolor='w', label='CCGs')
    ax2a = ax2.twinx()
    ax2a.plot(ts_trust_month['Year-Month'][6:], ts_trust_month['Count'][6:], color='#ff7f00',
             alpha=0.65,marker='o', markersize=8, markerfacecolor='w', label='NHS Trusts')
    ax2.plot(np.nan, np.nan, color='#ff7f00',
             alpha=0.65,marker='o', markersize=8, markerfacecolor='w', label='NHS Trusts')

    width=0.375
    rects1 = ax3.bar(np.arange(len(ts_trust_annual)), ts_trust_annual['Count'],
                     width, color='#ff7f00', label='NHS Trusts', alpha=0.6, edgecolor='k',
                     linewidth=0.75)
    rects2 = ax3.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Count'],
                     width, color='#377eb8', label='CCGs', alpha=0.6, edgecolor='k',
                     linewidth=0.75)
    ax3.set_xticks(np.arange(len(ts_trust_annual)) + width/2)
    ax3.set_xticklabels(ts_trust_annual['Year'])
    ax3.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)

    rects3 = ax4.bar(np.arange(len(ts_trust_annual)), ts_trust_annual['Amount'],
            width, color='#ff7f00', label='NHS Trusts', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    rects4 = ax4.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Amount'],
            width, color='#377eb8', label='CCGs', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    ax4.set_xticks(np.arange(len(ts_trust_annual)) + width/2)
    ax4.set_xticklabels(ts_trust_annual['Year'])
    ax4.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sept', 'Octo', 'Nov', 'Dec']
    rects5 = ax5.bar(np.arange(len(ts_trust_monthly)), ts_trust_monthly['Count'],
            width, color='#ff7f00', label='NHS Trusts', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    rects6 = ax5.bar(np.arange(len(ts_ccg_monthly))+width, ts_ccg_monthly['Count'],
            width, color='#377eb8', label='CCGs', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    ax5.set_xticks(np.arange(len(ts_trust_monthly)) + width/2)
    ax5.set_xticklabels(months)
    ax5.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)

    rects7 = ax6.bar(np.arange(len(ts_trust_monthly)), ts_trust_monthly['Amount'],
            width, color='#ff7f00', label='NHS Trusts', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    rects8 = ax6.bar(np.arange(len(ts_ccg_monthly))+width, ts_ccg_monthly['Amount'],
            width, color='#377eb8', label='CCGs', alpha=0.6, edgecolor='k',
            linewidth=0.75)
    ax6.set_xticks(np.arange(len(ts_trust_monthly)) + width/2)
    ax6.set_xticklabels(months)
    ax6.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)

    ax1.text(x=0.5, y=1.035, s='Value of payments made to Charity Commission institutions',
             ha='center', fontsize=titlesize, va='bottom', transform=ax1.transAxes, **csfont)
    ax1.text(x=0.0, y=1.01, s='A.', fontsize=titlesize+5, ha='left',
             va='bottom', transform=ax1.transAxes, **csfont)
    ax2.text(x=0.5, y=1.035, s='Number of payments made to Charity Commission institutions',
             fontsize=titlesize, ha='center', va='bottom', transform=ax2.transAxes, **csfont)
    ax2.text(x=0.0, y=1.01, s='B.', fontsize=titlesize+5, ha='left', va='bottom',
             transform=ax2.transAxes, **csfont)
    ax3.text(x=0.5, y=1.02, s='Number of payments across years', fontsize=titlesize,
             ha='center', va='bottom', transform=ax3.transAxes, **csfont)
    ax3.text(x=0.0, y=1.01, s='C.', fontsize=titlesize+5, ha='left', va='bottom',
             transform=ax3.transAxes, **csfont)
    ax4.text(x=0.5, y=1.02, s='Value of payments across years', fontsize=titlesize,
             ha='center', va='bottom', transform=ax4.transAxes, **csfont)
    ax4.text(x=0.0, y=1.01, s='D.', fontsize=titlesize+5, ha='left', va='bottom',
             transform=ax4.transAxes, **csfont)
    ax5.text(x=0.5, y=1.02, s='Number of payments across months', fontsize=titlesize,
             ha='center', va='bottom', transform=ax5.transAxes, **csfont)
    ax5.text(x=0.0, y=1.01, s='E.', fontsize=titlesize+5, ha='left', va='bottom',
             transform=ax5.transAxes, **csfont)
    ax6.text(x=0.5, y=1.02, s='Value of payments across months', fontsize=titlesize,
             ha='center', va='bottom', transform=ax6.transAxes, **csfont)
    ax6.text(x=0.0, y=1.01, s='F.', fontsize=titlesize+5, ha='left', va='bottom',
             transform=ax6.transAxes, **csfont)
    ax1.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax2.legend(loc='lower left', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax3.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax4.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax5.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax6.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=2)
    ax1.set_xticks([])
    ax1a.set_xticks([])
    ax1.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax2.xaxis.set_major_locator(plt.MaxNLocator(12))
    sns.despine(ax=ax1, top=True, left=False, right=False, bottom=False)
    sns.despine(ax=ax2, top=True, left=False, right=False, bottom=False)
#    ax1.grid(linestyle='--', linewidth=0.5, alpha=0.5, color='#d3d3d3',zorder=0)
#    ax2.grid(linestyle='--', linewidth=0.5, alpha=0.5, color='#d3d3d3',zorder=0)
#    ax3.grid(linestyle='--', linewidth=0.5, alpha=0.5, color='#d3d3d3',zorder=0)
#    ax4.grid(linestyle='--', linewidth=0.5, alpha=0.5, color='#d3d3d3',zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1a.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2a.spines['top'].set_visible(False)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax1a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax2a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax4.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax5.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax6.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax1.set_ylabel('Payments by CCGs')
    ax1a.set_ylabel('Payments by NHS Trusts')
    ax2.set_ylabel('Payments by CCGs')
    ax2a.set_ylabel('Payments by NHS Trusts')
    ax3.set_ylabel('Payments to CC orgs')
    ax4.set_ylabel('Payments to CC orgs')
    ax3.set_ylim(0, 6)
    ax1.tick_params(labelbottom=False)
    ax5.tick_params(labelleft=False)
    ax6.tick_params(labelleft=False)
    ax3.tick_params(labelbottom=False)
    ax5.tick_params(labelbottom=False)
    sns.despine(ax=ax3, top=True, right=True)
    sns.despine(ax=ax4, top=True, right=True)
    sns.despine(ax=ax5, left=False)
    sns.despine(ax=ax6, left=False)

#    for rect in rects1:
#        height = rect.get_height()
#        ax3.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=7.5)
#    for rect in rects2:
#        height = rect.get_height()
#        ax3.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=7.5)
#
#    for rect in rects3:
#        height = rect.get_height()
#        ax4.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=7.5)
#    for rect in rects4:
#        height = rect.get_height()
#        ax4.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=7.5)
#
#    for rect in rects5:
#        height = rect.get_height()
#        ax5.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=5)
#    for rect in rects6:
#       height = rect.get_height()
#        ax5.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=5)
#    for rect in rects7:
#        height = rect.get_height()
#        ax6.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=5)
#    for rect in rects8:
#        height = rect.get_height()
#        ax6.annotate(str(round(height,1))+'%',
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 2),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom',
#                        fontsize=5)
    plt.tight_layout()
    plt.subplots_adjust(wspace = 2)
    plt.savefig(os.path.join(figure_path, 'payments_over_time.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'payments_over_time.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'payments_over_time.png'),
                bbox_inches='tight', dpi=600)


def make_monthly(pay_df, pay_df_cc, cc_name):
    split_date_cc = pay_df_cc['date'].astype(str).str.\
        split('-', expand=True)#.rename({'0', 'Year'}, axis=1)
    split_date_cc = split_date_cc.\
        rename(columns={0: 'Year', 1: 'Month'})
    new_df_cc = pd.concat([pay_df_cc, split_date_cc], axis=1)
    split_date = pay_df['date'].astype(str).str.\
        split('-', expand=True)#.rename({'0', 'Year'}, axis=1)
    split_date = split_date.rename(columns={0: 'Year', 1: 'Month'})
    new_df = pd.concat([pay_df, split_date], axis=1)
    ts_plot = pd.DataFrame(columns = ['Month', 'Count', 'Amount'])
    for month in ['01', '02', '03', '04', '05', '06',
                  '07', '08','09', '10', '11', '12']:
        temp_df_cc = new_df_cc[(new_df_cc['Month']==str(month))]
        temp_df = new_df[(new_df['Month']==str(month))]
        count_cc = len(temp_df_cc)
        count = len(temp_df)
        amount_cc = temp_df_cc['amount'].sum()
        amount = temp_df['amount'].sum()
        i = len(ts_plot) + 1
        ts_plot.loc[i] = [str(month),
                          (count_cc/count)*100,
                          (amount_cc/amount)*100]
    return ts_plot


def make_annual(pay_df, pay_df_cc, cc_name):
    split_date_cc = pay_df_cc['date'].astype(str).str.\
        split('-', expand=True)
    split_date_cc = split_date_cc.\
        rename(columns={0: 'Year', 1: 'Month'})
    new_df_cc = pd.concat([pay_df_cc, split_date_cc], axis=1)
    split_date = pay_df['date'].astype(str).str.\
        split('-', expand=True)
    split_date = split_date.rename(columns={0: 'Year', 1: 'Month'})
    new_df = pd.concat([pay_df, split_date], axis=1)
    ts_plot = pd.DataFrame(columns = ['Year', 'Count', 'Amount'])
    for year in range(2013, 2021):
        temp_df_cc = new_df_cc[(new_df_cc['Year']==str(year))]
        temp_df = new_df[(new_df['Year']==str(year))]
        count_cc = len(temp_df_cc)
        count = len(temp_df)
        amount_cc = temp_df_cc['amount'].sum()
        amount = temp_df['amount'].sum()
        i = len(ts_plot) + 1
        ts_plot.loc[i] = [str(year),
                          (count_cc/count)*100,
                          (amount_cc/amount)*100]
    return ts_plot

def make_temporal_df(pay_df, pay_df_cc, icnpo_df, cc_name):
    split_date_cc = pay_df_cc['date'].astype(str).str.\
        split('-', expand=True)#.rename({'0', 'Year'}, axis=1)
    split_date_cc = split_date_cc.\
        rename(columns={0: 'Year', 1: 'Month'})
    new_df_cc = pd.concat([pay_df_cc, split_date_cc], axis=1)
    split_date = pay_df['date'].astype(str).str.\
        split('-', expand=True)#.rename({'0', 'Year'}, axis=1)
    split_date = split_date.rename(columns={0: 'Year', 1: 'Month'})
    new_df = pd.concat([pay_df, split_date], axis=1)
    ts_plot = pd.DataFrame(columns = ['Year', 'Month',
                                      'Year-Month',
                                      'Count', 'Amount'])
    for year in range(2013, 2021):
        for month in ['01', '02', '03', '04', '05', '06',
                      '07', '08','09', '10', '11', '12']:
            temp_df_cc = new_df_cc[(new_df_cc['Year']==str(year)) &
                                   (new_df_cc['Month']==str(month))]
            temp_df = new_df[(new_df['Year']==str(year)) &
                             (new_df['Month']==str(month))]
            count_cc = len(temp_df_cc)
            count = len(temp_df)
            amount_cc = temp_df_cc['amount'].sum()
            amount = temp_df['amount'].sum()
            i = len(ts_plot) + 1
            ts_plot.loc[i] = [str(year), str(month),
                              str(year)+'-'+str(month),
                              (count_cc/count)*100,
                              (amount_cc/amount)*100]
            if (year == 2020) and (month=='02'):
                break
        if (year == 2020) and (month=='02'):
            break
    pay_merge = pd.merge(pay_df_cc, cc_name, how='left',
                         left_on='verif_match',
                         right_on='norm_name')
    pay_merge = pd.merge(pay_merge, icnpo_df, how='left',
                         left_on='regno', right_on='regno')
    split_date_icnpo = pay_merge['date'].astype(str).str.\
        split('-', expand=True)#.rename({'0', 'Year'}, axis=1)
    split_date_icnpo = split_date_icnpo.rename(columns={0: 'Year',
                                                        1: 'Month'})
    icnpo_df = pd.concat([pay_merge, split_date_icnpo], axis=1)
    ts_plot_icnpo = pd.DataFrame(columns = ['Year', 'Month',
                                            'Year-Month', 'ICNPO',
                                            'Count', 'Amount'])
    for year in range(2013, 2021):
        for month in ['01', '02', '03', '04', '05', '06',
                      '07', '08','09', '10', '11', '12']:
            temp_df = new_df[(new_df['Year']==str(year)) &
                             (new_df['Month']==str(month))]
            month_count = len(temp_df)
            month_amount = temp_df['amount'].sum()
            for ICNPO in icnpo_df['ICNPO'].unique():
                temp_df_icnpo = icnpo_df[(icnpo_df['Year']==str(year)) &
                                         (icnpo_df['Month']==str(month)) &
                                         (icnpo_df['ICNPO']==ICNPO)]
                count_icnpo = len(temp_df_icnpo)
                amount_icnpo = temp_df_icnpo['amount'].sum()
                i = len(ts_plot_icnpo) + 1
                ts_plot_icnpo.loc[i] = [str(year), str(month),
                                        str(year)+'-'+str(month),
                                        str(ICNPO),
                                        (count_icnpo/month_count)*100,
                                        (amount_icnpo/month_amount)*100]
            if (year == 2020) and (month=='02'):
                break
        if (year == 2020) and (month=='02'):
            break
    return ts_plot, ts_plot_icnpo


def plot_heatmaps(ts_icnpo_plot_trust, ts_icnpo_plot_ccg, figure_path):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    titlesize = 15
    sns.set_style('ticks')
    fig = plt.figure(constrained_layout=True, figsize=(14, 11))
    gs = gridspec.GridSpec(2,3, width_ratios=[20,20,1], height_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0:1])
    ax2 = fig.add_subplot(gs[0, 1:-1])
    ax3 = fig.add_subplot(gs[0, -1])
    ax4 = fig.add_subplot(gs[1, 0:1])
    ax5 = fig.add_subplot(gs[1, 1:-1])
    ax6 = fig.add_subplot(gs[1, -1])
    ts_icnpo_plot_trust['ICNPO'] = ts_icnpo_plot_trust['ICNPO'].astype(float)
    ts_icnpo_plot_trust = ts_icnpo_plot_trust[ts_icnpo_plot_trust['ICNPO'].notnull()]
    ts_icnpo_plot_trust['ICNPO'] = ts_icnpo_plot_trust['ICNPO'].astype(int)
    ts_icnpo_plot_ccg['ICNPO'] = ts_icnpo_plot_ccg['ICNPO'].astype(float)
    ts_icnpo_plot_ccg = ts_icnpo_plot_ccg[ts_icnpo_plot_ccg['ICNPO'].notnull()]
    ts_icnpo_plot_ccg['ICNPO'] = ts_icnpo_plot_ccg['ICNPO'].astype(int)
    heatmap_data_trust_count = pd.pivot_table(ts_icnpo_plot_trust, values='Count',
                                   index=['Year-Month'],
                                   columns='ICNPO')[6:]
    heatmap_data_trust_amount= pd.pivot_table(ts_icnpo_plot_trust, values='Amount',
                                  index=['Year-Month'],
                                  columns='ICNPO')[6:]
    heatmap_data_ccg_count = pd.pivot_table(ts_icnpo_plot_ccg, values='Count',
                                   index=['Year-Month'],
                                   columns='ICNPO')[6:]
    heatmap_data_ccg_amount = pd.pivot_table(ts_icnpo_plot_ccg, values='Amount',
                                  index=['Year-Month'],
                                  columns='ICNPO')[6:]
    heatmap_data_trust_count = heatmap_data_trust_count.fillna(0)
    heatmap_data_trust_amount = heatmap_data_trust_amount.fillna(0)
    heatmap_data_ccg_count = heatmap_data_ccg_count.fillna(0)
    heatmap_data_ccg_amount = heatmap_data_ccg_amount.fillna(0)
    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    vmax_C = pd.concat([heatmap_data_trust_count,
                        heatmap_data_ccg_count]).fillna(0).to_numpy().max()
    vmax_A = pd.concat([heatmap_data_trust_amount,
                        heatmap_data_ccg_amount]).fillna(0).to_numpy().max()
    ee = sns.heatmap(heatmap_data_trust_count.T, ax=ax1, cmap=my_cmap,
                     xticklabels=12, cbar_ax=None, cbar=False,
                     vmin=0.0000000001, vmax=vmax_C)
    ee.set_xlabel('')
    ee.set_ylabel('ICNPO')
    ee.set_xticks([])
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    ff = sns.heatmap(heatmap_data_trust_amount.T, ax=ax4, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=12, cbar_ax=None, cbar=False, vmax=vmax_A)
    ff.set_xlabel('')
    ff.set_ylabel('ICNPO')
    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    gg = sns.heatmap(heatmap_data_ccg_count.T, ax=ax2, cmap=my_cmap,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     vmin=0.0000000001, cbar_ax=ax3, vmax=vmax_C)
    cbar = ax2.collections[0].colorbar
    cbar.set_label('Total number of payments', labelpad=-65, fontsize=12)
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    gg.set_xticks([])
    gg.set_yticks([])
    gg.set_xlabel('')
    gg.set_ylabel('')
    hh = sns.heatmap(heatmap_data_ccg_amount.T, ax=ax5, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     cbar_ax=ax6, vmax=vmax_A)
    cbar = ax5.collections[0].colorbar
    cbar.set_label('Total value of payments', labelpad=-65, fontsize=12)
    hh.set_xlabel('')
    hh.set_ylabel('')
    hh.set_yticks([])
    ax1.text(x=0.5, y=1.02, s='Number of payments made by NHS Trusts',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax1.text(x=0.0, y=1.01, s='A.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax2.text(x=0.5, y=1.02, s='Number of payments made by CCGs',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax2.transAxes,
             **csfont)
    ax2.text(x=0.0, y=1.01, s='B.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax2.transAxes,
             **csfont)
    ax4.text(x=0.5, y=1.02, s='Value of payments made by NHS Trusts',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax4.transAxes,
             **csfont)
    ax4.text(x=0.0, y=1.01, s='C.',# weight='bold',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax4.transAxes,
             **csfont)
    ax5.text(x=0.5, y=1.02, s='Value of payments made by CCGs',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax5.transAxes,
             **csfont)
    ax5.text(x=0.0, y=1.01, s='D.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax5.transAxes,
             **csfont)
    ax4.tick_params(axis='x', rotation=90)
    ax5.tick_params(axis='x', rotation=90)
    sns.despine(ax=ax1, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax2, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax4, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax5, top=False, bottom=False, left=False, right=False)
    fig.suptitle('')
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'heatmaps.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.png'),
                bbox_inches='tight', dpi=600)


def class_groupings(pay_df_cc, pay_df_cc_ccg, pay_df_cc_trust,
                    cc_name, cc_class, table_path):

    # full dataframe
    cc_count = pay_df_cc.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val = pay_df_cc.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='verif_match')
    cc_merge = pd.merge(cc_merge, cc_name, how='left',
                        left_on='verif_match',
                        right_on='norm_name')
    cc_merge['regno'] = pd.to_numeric(cc_merge['regno'],
                                      errors='coerce')
    cc_merge['regno'] = cc_merge['regno'].astype(float)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, cc_class, how='left',
                        left_on='regno', right_on='regno')
    cc_class_count = cc_merge.groupby(['classtext'])['classtext'].\
        count().reset_index(name="count")
    cc_class_val = cc_merge.groupby(['classtext'])['amount'].\
        sum().reset_index()
    cc_class_count['count_pc'] = (cc_class_count['count'] /
                                  cc_class_count['count'].sum())*100
    cc_class_val['amount_pc'] = (cc_class_val['amount'] /
                                   cc_class_val['amount'].sum())*100
    class_merge = pd.merge(cc_class_count, cc_class_val, how='left',
                           left_on='classtext', right_on='classtext')



    #merge in ccgs
    cc_count_ccg = pay_df_cc_ccg.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val_ccg = pay_df_cc_ccg.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge_ccg = pd.merge(cc_val_ccg, cc_count_ccg, how='left', on='verif_match')
    cc_merge_ccg = pd.merge(cc_merge_ccg, cc_name, how='left',
                            left_on='verif_match',
                            right_on='norm_name')
    cc_merge_ccg['regno'] = pd.to_numeric(cc_merge_ccg['regno'],
                                          errors='coerce')
    cc_merge_ccg['regno'] = cc_merge_ccg['regno'].astype(float)
    cc_merge_ccg['amount'] = cc_merge_ccg['amount'].astype(int)
    cc_merge_ccg = pd.merge(cc_merge_ccg, cc_class, how='left',
                            left_on='regno', right_on='regno')
    cc_class_count_ccg = cc_merge_ccg.groupby(['classtext'])['classtext'].\
        count().reset_index(name="count_ccg")
    cc_class_val_ccg = cc_merge_ccg.groupby(['classtext'])['amount'].\
        sum().reset_index()
    cc_class_count_ccg['count_pc_ccg'] = (cc_class_count_ccg['count_ccg'] /
                                          cc_class_count_ccg['count_ccg'].sum())*100
    cc_class_val_ccg = cc_class_val_ccg.rename({'amount':'amount_ccg'}, axis=1)
    cc_class_val_ccg['amount_pc_ccg'] = (cc_class_val_ccg['amount_ccg'] /
                                         cc_class_val_ccg['amount_ccg'].sum())*100
    class_merge = pd.merge(class_merge, cc_class_count_ccg, how='left',
                               left_on='classtext', right_on='classtext')
    class_merge = pd.merge(class_merge, cc_class_val_ccg, how='left',
                               left_on='classtext', right_on='classtext')

    #merge in trusts
    cc_count_trust = pay_df_cc_trust.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val_trust = pay_df_cc_trust.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge_trust = pd.merge(cc_val_trust, cc_count_trust, how='left', on='verif_match')
    cc_merge_trust = pd.merge(cc_merge_trust, cc_name, how='left',
                            left_on='verif_match',
                            right_on='norm_name')
    cc_merge_trust['regno'] = pd.to_numeric(cc_merge_trust['regno'],
                                          errors='coerce')
    cc_merge_trust['regno'] = cc_merge_trust['regno'].astype(float)
    cc_merge_trust['amount'] = cc_merge_trust['amount'].astype(int)
    cc_merge_trust = pd.merge(cc_merge_trust, cc_class, how='left',
                            left_on='regno', right_on='regno')
    cc_class_count_trust = cc_merge_trust.groupby(['classtext'])['classtext'].\
        count().reset_index(name="count_trust")
    cc_class_val_trust = cc_merge_trust.groupby(['classtext'])['amount'].\
        sum().reset_index()
    cc_class_count_trust['count_pc_trust'] = (cc_class_count_trust['count_trust'] /
                                          cc_class_count_trust['count_trust'].sum())*100
    cc_class_val_trust = cc_class_val_trust.rename({'amount':'amount_trust'}, axis=1)
    cc_class_val_trust['amount_pc_trust'] = (cc_class_val_trust['amount_trust'] /
                                         cc_class_val_trust['amount_trust'].sum())*100
    class_merge = pd.merge(class_merge, cc_class_count_trust, how='left',
                               left_on='classtext', right_on='classtext')
    class_merge = pd.merge(class_merge, cc_class_val_trust, how='left',
                               left_on='classtext', right_on='classtext')

    class_merge = class_merge.drop('amount', axis=1)
    class_merge = class_merge.drop('amount_ccg', axis=1)
    class_merge = class_merge.drop('amount_trust', axis=1)
    class_merge = class_merge.drop('count', axis=1)
    class_merge = class_merge.drop('count_ccg', axis=1)
    class_merge = class_merge.drop('count_trust', axis=1)

    class_merge = class_merge.rename({'amount_pc':'amount'}, axis=1)
    class_merge = class_merge.rename({'count_pc':'count'}, axis=1)

    class_merge = class_merge.rename({'amount_pc_ccg':'amount_ccg'}, axis=1)
    class_merge = class_merge.rename({'count_pc_ccg':'count_ccg'}, axis=1)

    class_merge = class_merge.rename({'amount_pc_trust':'amount_tr'}, axis=1)
    class_merge = class_merge.rename({'count_pc_trust':'count_tr'}, axis=1)
    class_merge = class_merge[['classtext', 'amount', 'count',
                               'amount_ccg', 'count_ccg',
                               'amount_tr', 'count_tr']].round(2)
    print(class_merge)
    class_merge.to_csv(os.path.join(table_path, 'class_table.csv'), index=False)


def charity_age(cc_pay_df, cc_sup, cc_name, cc_class, figure_path):
    titlesize = 15
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    ccgdata_regdate = cc_sup[cc_sup['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    cc_regdate = cc_name[cc_name['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    cc_pay_df_with_cc = pd.merge(cc_pay_df, cc_name, how='left',
                                 left_on='verif_match', right_on='norm_name')
    cc_pay_classtext = pd.merge(cc_pay_df_with_cc, cc_class, how='left',
                                  left_on='regno', right_on='regno')
    cc_pay_adv = cc_pay_classtext[cc_pay_classtext['classtext']=='The Advancement Of Health Or Saving Of Lives']

    cc_adv_date = cc_pay_adv[cc_pay_adv['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    g = sns.distplot(ccgdata_regdate, ax=ax1, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#377eb8', 'alpha': 0.35,
                               'edgecolor': 'k'}, label='NHS Suppliers',
                     bins=np.arange(1950, 2020, 3))
    g = sns.distplot(cc_regdate, ax=ax1, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.35,
                               'edgecolor': 'k'},
                     label='All CC', bins=np.arange(1950, 2020, 3))
    ax1.set_ylabel("Normalized Frequency", fontsize=12)
    ax1.set_xlabel("Charity Registration Year", fontsize=12)
    ax1.set_ylim(0, 0.048)
    ax1.set_title('Distributions of Registration Years',
                  **csfont, fontsize=titlesize, y=1.02)
    ax1.set_title('A.', **csfont, fontsize=titlesize+5, loc='left', y=1.01)
    sns.despine()
    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)

    a = cc_sup[cc_sup['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    b = cc_name[cc_name['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    percs = np.linspace(0, 100, 40)
    qn_a = np.percentile(a, percs)
    qn_b = np.percentile(b, percs)
    x = np.linspace(np.min((qn_a.min(), qn_b.min())),
                    np.max((qn_a.max(), qn_b.max())))
    ax2.plot(x, x, color='k', ls="--", alpha=0.5)
    ax2.plot(qn_a, qn_b, ls="", marker="o", color='#266402', alpha=0.35,
             markersize=14, fillstyle='full', markeredgecolor='k')
    ax2.set_ylabel("NHS Supplier Registration Years",
                   fontsize=12)
    ax2.set_xlabel("All CC Registration Years",
                   fontsize=12)
    ax2.set_title('Q-Q Plot of Registration Years',
                  **csfont, fontsize=titlesize, y=1.02)
    ax2.set_title('B.', loc='left',
                  **csfont, fontsize=titlesize+5, y=1.01)

    def ecdf(data):
        """ Compute ECDF """
        x = np.sort(data)
        n = x.size
        y = np.arange(1, n+1) / n
        return(x, y)

    x1, y1 = ecdf(cc_regdate)
    ax3.plot(x1, y1, label='All Charity Commission',
             color='#ff7f00', alpha=0.7)
    x2, y2 = ecdf(ccgdata_regdate)
    ax3.plot(x2, y2, label='NHS Suppliers', color='#377eb8', alpha=0.7)
    x3, y3 = ecdf(cc_adv_date)
    ax3.plot(x3, y3, label='Advancement of Health',
             color='#266402', alpha=0.7)
    ax3.set_ylabel("Proportion of Data", fontsize=12)
    ax3.set_xlabel("Charity Registration Years", fontsize=12)
    ax3.set_title('Empirical Cumulative Distribution',
                  **csfont, fontsize=titlesize, y=1.02)
    ax3.set_title('C.', loc='left',
                  **csfont, fontsize=titlesize+5, y=1.01)
    ax3.legend(loc='upper left', edgecolor='k',
               frameon=False, fontsize=10)
    h = sns.distplot(ccgdata_regdate, ax=ax4, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#377eb8', 'alpha': 0.35,
                               'edgecolor': 'k'}, label='NHS Suppliers',
                     bins=np.arange(1950, 2020, 3))
    h = sns.distplot(cc_adv_date, ax=ax4, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.35,
                               'edgecolor': 'k'},
                     label='All Advancement of Health', bins=np.arange(1950, 2020, 3))
    ax4.set_ylabel("Normalized Frequency", fontsize=12)
    ax4.set_xlabel("Charity Registration Year", fontsize=12)
    ax4.set_title('Comparison with Healthcare Charities',
                  **csfont, fontsize=titlesize, y=1.02)
    ax4.set_title('D.',
                  **csfont, fontsize=titlesize+5, loc='left', y=1.01)
    h.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)

    ax2.grid(linestyle='--', linewidth=0.4, alpha=0.325, color='#d3d3d3',zorder=0)
    ax3.grid(linestyle='--', linewidth=0.4, alpha=0.325, color='#d3d3d3',zorder=0)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'age_distributions.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'age_distributions.png'),
                bbox_inches='tight', dpi=500)
    plt.savefig(os.path.join(figure_path, 'age_distributions.pdf'),
                bbox_inches='tight')




def plot_choropleths_trusts(support_path, shape_path, figure_path,
                           trust_pay_df, pay_df_cc):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    titlesize = 15
    trust_list = pd.read_excel(os.path.join(support_path, 'trust_list.xls'))
    trust_list = trust_list[['Latitude','Longitude','abrev']]
    total_count = trust_pay_df.groupby(['dept'])['dept'].\
        count().reset_index(name="total_count")
    total_val = trust_pay_df.groupby(['dept'])['amount'].sum().reset_index().\
        rename({'amount': 'total_amount'}, axis=1)
    trust_merge = pd.merge(total_count, total_val, how='left',
                           left_on='dept', right_on='dept')

    charity_count = pay_df_cc.groupby(['dept'])['dept'].\
        count().reset_index(name="charity_count")
    charity_val = pay_df_cc.groupby(['dept'])['amount'].sum().reset_index().\
        rename({'amount': 'charity_amount'}, axis=1)
    trust_merge = pd.merge(trust_merge, charity_count, how='left',
                           left_on='dept', right_on='dept')
    trust_merge = pd.merge(trust_merge, charity_val, how='left',
                           left_on='dept', right_on='dept')
    trust_merge['pc_amount'] = (trust_merge['charity_amount']/trust_merge['total_amount']) * 100
    trust_merge['pc_count'] = (trust_merge['charity_count'] /trust_merge['total_count']) * 100
    #merge in the list for latlongs
    trust_merge = pd.merge(trust_merge, trust_list, how='left',
                          left_on='dept', right_on = 'abrev')
    trust_merge['Latitude'] = trust_merge['Latitude'].astype(float)
    trust_merge['Longitude'] = trust_merge['Longitude'].astype(float)
    trust_merge = trust_merge[trust_merge['total_count'] > 50]
    gdf = GeoDataFrame(trust_merge,
                       geometry=points_from_xy(trust_merge['Longitude'],
                                               trust_merge['Latitude']),
                       crs = 'EPSG:4326')
    gdf = gdf[gdf['pc_count'].notnull()]
    gdf['pc_count'] = gdf['pc_count'].astype(float)
    gdf = gdf[gdf['pc_amount'].notnull()]
    gdf['pc_amount'] = gdf['pc_amount'].astype(float)
    gdf = gdf.to_crs('epsg:27700')

    fig = plt.figure(figsize=(16, 16))
    ax1 = plt.subplot2grid((20, 20), (0, 0), colspan=10, rowspan=17)
    ax2 = plt.subplot2grid((20, 20), (0, 10), colspan=10, rowspan=17)
    ax3 = plt.subplot2grid((20, 20), (17, 2), colspan=7, rowspan=3)
    ax4 = plt.subplot2grid((20, 20), (17, 12), colspan=7, rowspan=3)

    shapefile = os.path.join(shape_path,
                             'Clinical_Commissioning_Group_CCG_IMD_2019_OSGB1936.shp')
    shapefile = gpd.read_file(os.path.join(shape_path, shapefile))
    shapefile = shapefile.to_crs(epsg=27700)
    shapefile.plot(ax=ax1, color='white', edgecolor='black', linewidth=0.35);
    shapefile.plot(ax=ax1, color='None', edgecolor='black', alpha=0.2);
    markersize = gdf['pc_count'] / 5 * 200
    k = 6
    quantiles = mc.Quantiles(gdf.pc_count.dropna(), k=k)
    gdf['pc_count_cat'] = quantiles.find_bin(gdf.pc_count).astype('str')
    #gdf.loc[gdf.pc_amount.isnull(), 'pc_amount'] = 'No Data'
    cmap = plt.cm.get_cmap('Blues', k+2)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='pc_count_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
                 alpha=0.75, ax=ax1, markersize=markersize)
    upper_bounds = quantiles.bins
    bounds = []
    for index, upper_bound in enumerate(upper_bounds):
        if index == 0:
            lower_bound = gdf.pc_amount.min()
        else:
            lower_bound = upper_bounds[index-1]
        bound = str(f'{lower_bound:.1f}% - {upper_bound:.1f}%')
        bounds.append(bound)
    legend_labels = ax1.get_legend().get_texts()
    for bound, legend_label in zip(bounds, legend_labels):
        legend_label.set_text(bound)
    ax1.axis('off')
    ax1.set_title('Total Volume of Payments', **csfont, fontsize=titlesize+2)
    ax1.set_title('A.', **csfont, fontsize=titlesize+8, loc='left')

    shapefile.plot(ax=ax2, color='white', edgecolor='black', linewidth=0.35);
    shapefile.plot(ax=ax2, color='None', edgecolor='black', alpha=0.2);
    markersize = gdf['pc_amount'] / 5 * 200
    k = 6
    quantiles = mc.Quantiles(gdf.pc_amount.dropna(), k=k)
    gdf['pc_amount_cat'] = quantiles.find_bin(gdf.pc_amount).astype('str')
    #gdf.loc[gdf.pc_amount.isnull(), 'pc_amount'] = 'No Data'
    cmap = plt.cm.get_cmap('OrRd', k+2)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='pc_amount_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
                 alpha=0.75, ax=ax2, markersize=markersize)
    upper_bounds = quantiles.bins
    bounds = []
    for index, upper_bound in enumerate(upper_bounds):
        if index == 0:
            lower_bound = gdf.pc_amount.min()
        else:
            lower_bound = upper_bounds[index-1]
        bound = str(f'{lower_bound:.1f}% - {upper_bound:.1f}%')
        bounds.append(bound)
    legend_labels = ax2.get_legend().get_texts()
    for bound, legend_label in zip(bounds, legend_labels):
        legend_label.set_text(bound)
    ax2.axis('off')
    ax2.set_title('Cumulative Payment Amount', **csfont, fontsize=titlesize+2)
    ax2.set_title('B.', **csfont, fontsize=titlesize+8, loc='left')

    count_array = gdf[gdf['pc_count']!='No Data']['pc_count'].astype(float)
    ee = sns.distplot(count_array, ax=ax3, kde_kws={'color': '#377eb8', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#377eb8', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                      bins=20)
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")

    count_array = gdf[gdf['pc_amount']!='No Data']['pc_amount'].astype(float)
    ff = sns.distplot(count_array, ax=ax4, kde_kws={'color': '#ff7f00', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#ff7f00', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                      bins=20)
    ff.set_xlim(0, None)
    ff.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ff.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ff.set_xlabel("")

    sns.despine()
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.65, right=0.6)
    plt.savefig(os.path.join(figure_path, 'choropleth_map_trusts.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'choropleth_map_trusts.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'choropleth_map_trusts.png'),
                bbox_inches='tight', dpi=600)
    print('\nThe top 5 Trusts by %to VCS are: \n')
    print(gdf[['dept', 'charity_amount', 'pc_amount']].sort_values(by='pc_amount', ascending=False)[0:5])


def plot_choropleths_ccg(gdf, figure_path):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    titlesize = 14
#    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 12))
    fig = plt.figure(figsize=(16, 16))
    ax1 = plt.subplot2grid((20, 20), (0, 0), colspan=10, rowspan=17)
    ax2 = plt.subplot2grid((20, 20), (0, 10), colspan=10, rowspan=17)
    ax3 = plt.subplot2grid((20, 20), (17, 2), colspan=7, rowspan=3)
    ax4 = plt.subplot2grid((20, 20), (17, 12), colspan=7, rowspan=3)
    # ax1
    k = 6
    quantiles = mc.Quantiles(gdf.count_pc_cc.dropna(), k=k)
    gdf['count_pc_cc_cat'] = quantiles.find_bin(gdf.count_pc_cc).astype('str')
    gdf.loc[gdf.count_pc_cc.isnull(), 'count_pc_cc_cat'] = 'No Data'
    cmap = plt.cm.get_cmap('Blues', k+2)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_list.append('#ededed')
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='count_pc_cc_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
             alpha=0.75, ax=ax1, linewidth=0.35)
    upper_bounds = quantiles.bins
    bounds = []
    for index, upper_bound in enumerate(upper_bounds):
        if index == 0:
            lower_bound = gdf.count_pc_cc.min()
        else:
            lower_bound = upper_bounds[index-1]
        bound = str(f'{lower_bound:.1f}% - {upper_bound:.1f}%')
        bounds.append(bound)
    legend_labels = ax1.get_legend().get_texts()
    for bound, legend_label in zip(bounds, legend_labels):
        legend_label.set_text(bound)
    ax1.axis('off')
    ax1.set_title('Total Volume of Payments', **csfont, fontsize=titlesize+2)
    ax1.set_title('A.', **csfont, fontsize=titlesize+8, loc='left')

    # ax2
    k = 6
    quantiles = mc.Quantiles(gdf.amount_pc_cc.dropna(), k=k)
    gdf['amount_pc_cc_cat'] = quantiles.find_bin(gdf.amount_pc_cc).\
        astype('str')
    gdf.loc[gdf.amount_pc_cc.isnull(), 'amount_pc_cc_cat'] = 'No Data'
    cmap = plt.cm.get_cmap('OrRd', k+2)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_list.append('#ededed')
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='amount_pc_cc_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
             alpha=0.75, ax=ax2, linewidth=0.35)
    upper_bounds = quantiles.bins
    bounds = []
    for index, upper_bound in enumerate(upper_bounds):
        if index == 0:
            lower_bound = gdf.count_pc_cc.min()
        else:
            lower_bound = upper_bounds[index-1]
        bound = f'{lower_bound:.1f}% - {upper_bound:.1f}%'
        bounds.append(bound)
    legend_labels = ax2.get_legend().get_texts()
    for bound, legend_label in zip(bounds, legend_labels):
        legend_label.set_text(bound)
    ax2.axis('off')
    ax2.set_title('Cumulative Payment Amount', **csfont, fontsize=titlesize+2)
    ax2.set_title('B.', **csfont, fontsize=titlesize+8, loc='left')

    count_array = gdf[gdf['count_pc_cc']!='No Data']['count_pc_cc'].astype(float)
    ee = sns.distplot(count_array, ax=ax3, kde_kws={'color': '#377eb8', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#377eb8', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                               bins=20)
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")

#    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)
    count_array = gdf[gdf['amount_pc_cc']!='No Data']['amount_pc_cc'].astype(float)
    ff = sns.distplot(count_array, ax=ax4, kde_kws={'color': '#ff7f00', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#ff7f00', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                               bins=20)
    ff.set_xlim(0, None)
    ff.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ff.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ff.set_xlabel("")

    sns.despine()
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.65, right=.6)
    plt.savefig(os.path.join(figure_path, 'choropleth_map_ccgs.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'choropleth_map_ccgs.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'choropleth_map_ccgs.png'),
                bbox_inches='tight', dpi=600)
    print('\nThe top 5 Trusts by %to VCS are: \n')
    print(gdf[['dept', 'amount_cc', 'amount_pc_cc']].sort_values(by='amount_pc_cc', ascending=False)[0:5])


def make_ccg_to_gdf(pay_df, pay_df_cc, support_path):
    ccg_count = pay_df.groupby(['dept'])['dept'].\
                     count().reset_index(name="count_total")
    ccg_val = pay_df.groupby(['dept'])['amount'].sum().reset_index().\
        rename({'amount': 'amount_all'}, axis=1)
    ccg_all = pd.merge(ccg_count, ccg_val, how='left',
                       left_on='dept', right_on='dept')
    ccg_count_cc = pay_df_cc.groupby(['dept'])['dept'].\
        count().reset_index(name="count_cc")
    ccg_val_cc = pay_df_cc.groupby(['dept'])['amount'].sum().\
        reset_index().rename({'amount': 'amount_cc'}, axis=1)
    ccg_cc = pd.merge(ccg_count_cc, ccg_val_cc, how='left',
                      left_on='dept', right_on='dept')
    ccg_merged = pd.merge(ccg_all, ccg_cc, how='left',
                          left_on='dept', right_on='dept')
    ccg_merged['count_pc_cc'] = (ccg_merged['count_cc'] /
                                 ccg_merged['count_total'])*100
    ccg_merged['amount_pc_cc'] = (ccg_merged['amount_cc'] /
                                  ccg_merged['amount_all'])*100
    ccg19nm_lookup = pd.read_excel(os.path.join(support_path, 'ccg_list.xls'),
                                   usecols=['ccg19nm', 'abrev'])
    ccg_merged['dept'] = ccg_merged['dept'].str.lower().str.strip()
    ccg19nm_lookup['abrev'] = ccg19nm_lookup['abrev'].str.lower().\
        str.strip()
    ccg_merged = pd.merge(ccg_merged, ccg19nm_lookup, how='left',
                          left_on='dept', right_on='abrev')
    ccg_merged = ccg_merged[ccg_merged['count_total'] > 50]
    return ccg_merged


def make_gdf(ccg_merged, shape_path, support_path):
    shapefile = os.path.join(shape_path,
                             'Clinical_Commissioning_Group_CCG_IMD_2019_OSGB1936.shp')
    gdf = gpd.read_file(os.path.join(shape_path, shapefile))
    gdf['ccg19nm'] = gdf['ccg19nm'].str.lower().str.strip()
    ccg_merged['ccg19nm'] = ccg_merged['ccg19nm'].str.lower().str.strip()
    gdf = pd.merge(gdf, ccg_merged, how='left', left_on='ccg19nm',
                   right_on='ccg19nm')
    gdf = gdf.to_crs(epsg=27700)
    return gdf


def build_charity_df(pay_df, cc_name, icnpo_df, cc_fin, data_path):
    cc_pay_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_pay_df.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val = cc_pay_df.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='verif_match')
    cc_merge = pd.merge(cc_merge, cc_name, how='left',
                        left_on='verif_match',
                        right_on='norm_name')
    cc_merge['regno'] = pd.to_numeric(cc_merge['regno'],
                                      errors='coerce')
    cc_merge['regno'] = cc_merge['regno'].astype(float)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, on=['regno'],
                        how='left', indicator=False)
    cc_sup = pd.merge(cc_merge, cc_fin, on=['regno'],
                      how='left', indicator=False)
    missing_regno = len(cc_sup[cc_sup['regno'].isnull()])
    print('We are missing ' + str(missing_regno) + ' registration numbers')
    print("Can't do anything about that...\n" +
          "This seems to be where two charities have the " +
          "same normalised name, and neither has been " +
          " removed from the register")
    print('This leaves us with ' +
          str(len(cc_sup[cc_sup['regno'].notnull()])) +
          ' charities with regnos.')
    missing_income = len(cc_sup[cc_sup['income'].isnull()])
    print('We are missing ' + str(missing_income) + ' incomes')
    print("Can't do anything about that...")
    missing_icnpo_df = cc_sup[(cc_sup['icnpo_desc'].isnull()) & (cc_merge['regno'].notnull())]#[['verif_match', 'regno']]
    missing_icnpo = len(missing_icnpo_df)
    print('We are missing ' + str(missing_icnpo) + ' ICNPO numbers which have charity numbers')
    if missing_icnpo>0:
        print('The unmapped charities are in data\\support\\unmapped_icnpo.csv')
        missing_icnpo_df[['verif_match', 'regno']].to_csv(os.path.join(data_path, 'data_support', 'unmapped_icnpo.csv'))
    return cc_pay_df, cc_sup


def tabulate_charities(pay_df, cc_name, icnpo_df,
                       cc_fin, tablepath, tablename):
    cc_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_df.groupby(['verif_match'])['verif_match'].\
                     count().reset_index(name="count")
    cc_val = cc_df.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='verif_match')
    cc_merge = cc_merge[~cc_merge['verif_match'].\
               str.contains('FOUNDATION TRUST')]
    cc_merge = pd.merge(cc_merge, cc_name, how='left',
                        left_on='verif_match', right_on='norm_name')
    cc_merge['regno'] = pd.to_numeric(cc_merge['regno'], errors='coerce')
    cc_merge = cc_merge[cc_merge['regno'].notnull()]
    cc_merge['regno'] = cc_merge['regno'].astype(int)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, on=['regno'],
                        how='left', indicator=False)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].fillna(9999)
    cc_merge = pd.merge(cc_merge, cc_fin, on=['regno'],
                        how='left', indicator=False)
    cc_merge = cc_merge[cc_merge['ICNPO'].notnull()]
    cc_merge['ICNPO'] = cc_merge['ICNPO'].astype(int)
    cc_merge = cc_merge.drop(columns=['name', 'norm_name', 'subno',
                                      'nameno', 'icnpo_desc', 'icnpo_group',
                                      'remdate', 'remcode'])
    #cc_merge = cc_merge.set_index('verif_match')
    sorted_values = pd.merge(cc_name, cc_fin, how='left',
                             left_on='regno', right_on='regno').\
        sort_values(by='income', ascending=False)['norm_name'].reset_index()
    sorted_values['norm_name']=sorted_values['norm_name'].str.strip()
    cc_merge['CC Rank'] = np.nan
    cc_merge = cc_merge.sort_values(by='count', ascending=False)[0:10]
    for index, row in cc_merge.iterrows():
        pos = sorted_values[sorted_values['norm_name']==row['verif_match']].index[0]
        cc_merge.at[index, 'CC Rank'] = int(pos)
    cc_merge['regdate'] = pd.to_datetime(cc_merge['regdate']).dt.date
    cc_merge['CC Rank'] = cc_merge['CC Rank'].astype(int)
    print(cc_merge.to_string(index=False))
    cc_merge.to_csv(os.path.join(tablepath, tablename), index=False)

def icnpo_groupings(pay_df, pay_df_ccg, pay_df_trust,
                    cc_name, icnpo_df, icnpo_lookup, table_path):

    ## full df
    cc_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_df.groupby(['verif_match'])['verif_match'].\
                     count().reset_index(name="count")
    cc_val = cc_df.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='verif_match')
    cc_merge = cc_merge[~cc_merge['verif_match'].\
               str.contains('FOUNDATION TRUST')]
    cc_merge = pd.merge(cc_merge, cc_name, how='left',
                        left_on='verif_match', right_on='norm_name')
    cc_merge['regno'] = pd.to_numeric(cc_merge['regno'], errors='coerce')
    cc_merge = cc_merge[cc_merge['regno'].notnull()]
    cc_merge['regno'] = cc_merge['regno'].astype(int)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, on=['regno'],
                        how='left', indicator=False)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].fillna(9999)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].astype(int)
    cc_merge = cc_merge.drop(columns=['name', 'norm_name', 'subno',
                                      'nameno', 'regno', 'verif_match'])
    amount_icnpo_pc = cc_merge.groupby(['ICNPO'])['amount'].sum().rename("amount")
    amount_icnpo_pc = amount_icnpo_pc.reset_index()
    amount_icnpo_pc['amount'] = (amount_icnpo_pc['amount']/
                                 amount_icnpo_pc['amount'].sum())*100
    count_icnpo_pc = cc_merge.groupby(['ICNPO'])['ICNPO'].count().reset_index(name = "count")
    count_icnpo_pc['count'] = (count_icnpo_pc['count']/
                               count_icnpo_pc['count'].sum())*100
    sum_icnpo_pc = cc_merge.groupby(['ICNPO'])['amount'].sum().reset_index()
    sum_icnpo_pc['amount'] = (sum_icnpo_pc['amount']/
                              sum_icnpo_pc['amount'].sum())*100

    ## ccg df
    cc_df_ccg = pay_df_ccg[pay_df_ccg['match_type'].str.contains('Charity')]
    cc_count_ccg = cc_df_ccg.groupby(['verif_match'])['verif_match'].\
                     count().reset_index(name="count_ccg")
    cc_val_ccg = cc_df_ccg.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_val_ccg = cc_val_ccg.rename({'amount': 'amount_ccg'}, axis=1)
    cc_merge_ccg = pd.merge(cc_val_ccg, cc_count_ccg, how='left', on='verif_match')
    cc_merge_ccg = cc_merge_ccg[~cc_merge_ccg['verif_match'].\
               str.contains('FOUNDATION TRUST')]
    cc_merge_ccg = pd.merge(cc_merge_ccg, cc_name, how='left',
                        left_on='verif_match', right_on='norm_name')
    cc_merge_ccg['regno'] = pd.to_numeric(cc_merge_ccg['regno'], errors='coerce')
    cc_merge_ccg = cc_merge_ccg[cc_merge_ccg['regno'].notnull()]
    cc_merge_ccg['regno'] = cc_merge_ccg['regno'].astype(int)
    cc_merge_ccg['amount_ccg'] = cc_merge_ccg['amount_ccg'].astype(int)
    cc_merge_ccg = pd.merge(cc_merge_ccg, icnpo_df, on=['regno'],
                            how='left', indicator=False)
    cc_merge_ccg['ICNPO'] = cc_merge_ccg['ICNPO'].fillna(9999)
    cc_merge_ccg['ICNPO'] = cc_merge_ccg['ICNPO'].astype(int)
    cc_merge_ccg = cc_merge_ccg.drop(columns=['name', 'norm_name', 'subno',
                                              'nameno', 'regno', 'verif_match'])
    amount_icnpo_pc_ccg = cc_merge_ccg.groupby(['ICNPO'])['amount_ccg'].sum().rename("amount_ccg")
    amount_icnpo_pc_ccg = amount_icnpo_pc_ccg.reset_index()
    amount_icnpo_pc_ccg['amount_ccg'] = (amount_icnpo_pc_ccg['amount_ccg']/
                                         amount_icnpo_pc_ccg['amount_ccg'].sum())*100
    count_icnpo_pc_ccg = cc_merge_ccg.groupby(['ICNPO'])['ICNPO'].count().reset_index(name = "count_ccg")
    count_icnpo_pc_ccg['count_ccg'] = (count_icnpo_pc_ccg['count_ccg']/
                                   count_icnpo_pc_ccg['count_ccg'].sum())*100
    sum_icnpo_pc_ccg = cc_merge_ccg.groupby(['ICNPO'])['amount_ccg'].sum().reset_index()
    sum_icnpo_pc_ccg['amount_ccg'] = (sum_icnpo_pc_ccg['amount_ccg']/
                                      sum_icnpo_pc_ccg['amount_ccg'].sum())*100

    #trust_df
    cc_df_trust = pay_df_trust[pay_df_trust['match_type'].str.contains('Charity')]
    cc_count_trust = cc_df_trust.groupby(['verif_match'])['verif_match'].\
                     count().reset_index(name="count_trust")
    cc_val_trust = cc_df_trust.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_val_trust = cc_val_trust.rename({'amount': 'amount_trust'}, axis=1)
    cc_merge_trust = pd.merge(cc_val_trust, cc_count_trust, how='left', on='verif_match')
    cc_merge_trust = cc_merge_trust[~cc_merge_trust['verif_match'].\
               str.contains('FOUNDATION TRUST')]
    cc_merge_trust = pd.merge(cc_merge_trust, cc_name, how='left',
                        left_on='verif_match', right_on='norm_name')
    cc_merge_trust['regno'] = pd.to_numeric(cc_merge_trust['regno'], errors='coerce')
    cc_merge_trust = cc_merge_trust[cc_merge_trust['regno'].notnull()]
    cc_merge_trust['regno'] = cc_merge_trust['regno'].astype(int)
    cc_merge_trust['amount_trust'] = cc_merge_trust['amount_trust'].astype(int)
    cc_merge_trust = pd.merge(cc_merge_trust, icnpo_df, on=['regno'],
                            how='left', indicator=False)
    cc_merge_trust['ICNPO'] = cc_merge_trust['ICNPO'].fillna(9999)
    cc_merge_trust['ICNPO'] = cc_merge_trust['ICNPO'].astype(int)
    cc_merge_trust = cc_merge_trust.drop(columns=['name', 'norm_name', 'subno',
                                              'nameno', 'regno', 'verif_match'])
    amount_icnpo_pc_trust = cc_merge_trust.groupby(['ICNPO'])['amount_trust'].sum().rename("amount_trust")
    amount_icnpo_pc_trust = amount_icnpo_pc_trust.reset_index()
    amount_icnpo_pc_trust['amount_trust'] = (amount_icnpo_pc_trust['amount_trust']/
                                         amount_icnpo_pc_trust['amount_trust'].sum())*100
    count_icnpo_pc_trust = cc_merge_trust.groupby(['ICNPO'])['ICNPO'].count().reset_index(name = "count_trust")
    count_icnpo_pc_trust['count_trust'] = (count_icnpo_pc_trust['count_trust']/
                                   count_icnpo_pc_trust['count_trust'].sum())*100
    sum_icnpo_pc_trust = cc_merge_trust.groupby(['ICNPO'])['amount_trust'].sum().reset_index()
    sum_icnpo_pc_trust['amount_trust'] = (sum_icnpo_pc_trust['amount_trust']/
                                      sum_icnpo_pc_trust['amount_trust'].sum())*100

    icnpo_out = pd.merge(icnpo_lookup, count_icnpo_pc, how='left', left_on = 'icnpo',
                         right_on = 'ICNPO')
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc, how='left', on = 'ICNPO')
    icnpo_out = pd.merge(icnpo_out, count_icnpo_pc_ccg, how='left', left_on = 'icnpo',
                         right_on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = icnpo_out.drop('icnpo', 1)
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc_ccg, how='left', on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = icnpo_out.drop('ICNPO_x', 1)
    icnpo_out = pd.merge(icnpo_out, count_icnpo_pc_trust, how='left', left_on = 'ICNPO',
                         right_on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc_trust, how='left', on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = icnpo_out.drop(columns=['icnpo_desc', 'icnpo_desc', 'in_original_spec'])
    icnpo_out = icnpo_out[icnpo_out['ICNPO'].notnull()]
    icnpo_out['icnpo'] = icnpo_out['ICNPO'].astype(int)
    icnpo_out['icnpo'] = icnpo_out['ICNPO'].fillna(9999)
    for col in ['count_ccg', 'amount_ccg','count_trust','amount_trust']:
        icnpo_out[col] = icnpo_out[col].fillna(0)
    icnpo_out['icnpo'] = icnpo_out['icnpo'].astype(int)
    icnpo_out = icnpo_out.drop(columns=['ICNPO']).set_index('icnpo')
    icnpo_out = icnpo_out.round(2)
    icnpo_out.to_csv(os.path.join(table_path, 'icnpo_table.csv'))
    print(icnpo_out)


def load_ccname(cc_path, norm_path):
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


def load_ccclass(cc_path):
    cc_class = pd.read_csv(os.path.join(cc_path, 'extract_class.csv'),
                           warn_bad_lines=False,
                           error_bad_lines=False)
    class_ref = pd.read_csv(os.path.join(cc_path, 'extract_class_ref.csv'),
                            warn_bad_lines=False,
                            error_bad_lines=False)
    cc_class = pd.merge(cc_class, class_ref, how='left',
                        left_on='class', right_on='classno')
    cc_class = cc_class[cc_class['class'].notnull()]
    cc_class['class'] = cc_class['class'].astype(int)
    cc_class['regno'] = cc_class['regno'].astype(int)
    cc_class = cc_class[['regno', 'class', 'classtext']]
    return cc_class


def load_ccfin(cc_path):
    cc_fin = pd.read_csv(os.path.join(cc_path, 'extract_financial.csv'),
                                  warn_bad_lines=False, error_bad_lines=False,
                                  parse_dates=['fystart', 'fyend'])
    cc_fin = cc_fin[cc_fin['fystart'] > '2012-01-01']
    cc_fin = cc_fin[cc_fin['income'].notnull()]
    cc_fin = cc_fin.groupby('regno')['income'].sum().reset_index()
    return cc_fin


def load_icpno(support_path):
    icnpo_df = pd.read_csv(os.path.join(support_path, 'ICNPO_Classification.csv'))
    icnpo_lookup = pd.read_csv(os.path.join(support_path, 'ICNPO_lookup.csv'))
    icnpo_df = pd.merge(icnpo_df, icnpo_lookup, how = 'left', left_on = 'ICNPO', right_on = 'icnpo')
    icnpo_df = icnpo_df.drop(columns=['general_charities', 'icnpo', 'in_original_spec'])
    icnpo_df['regno'] = pd.to_numeric(icnpo_df['regno'], errors='coerce')
    return icnpo_df, icnpo_lookup
