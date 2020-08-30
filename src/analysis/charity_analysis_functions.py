import pandas as pd
from scipy import stats
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
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import geopandas as gpd
from datetime import timedelta, date
sys.path.append("..")
import matplotlib.gridspec as gridspec
mpl.font_manager._rebuild()
from reconciliation import normalizer

np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25


def make_rolling_windows(ccg_pay_df, trust_pay_df, nhsengland_pay_df, window):
    daterange = pd.date_range(date(2013, 12, 1), date(2019, 10, 1), freq='d')
    temp_df = pd.DataFrame(index=daterange, columns=['CCG_Count',
                                                     'CCG_Amount',
                                                     'Trust_Count',
                                                     'Trust_Amount',
                                                     'NHSEngland_Count',
                                                     'NHSEngland_Amount'])
    for single_date in daterange:
        lower_bound = single_date - pd.Timedelta(window, unit='d')
        ccg_90day_temp = ccg_pay_df[ccg_pay_df['date'].between(lower_bound,
                                                               single_date,
                                                               inclusive=False)]
        ccg_90day_amount_cc = ccg_90day_temp[ccg_90day_temp['match_type'].\
                                             str.contains('Charity')]['amount'].sum()/\
                              ccg_90day_temp['amount'].sum()
        ccg_90day_count_cc = len(ccg_90day_temp[ccg_90day_temp['match_type'].\
                                             str.contains('Charity')])/\
                              len(ccg_90day_temp)
        trust_90day_temp = trust_pay_df[trust_pay_df['date'].between(lower_bound,
                                                                     single_date,
                                                                     inclusive=False)]
        trust_90day_amount_cc = trust_90day_temp[trust_90day_temp['match_type'].\
                                                 str.contains('Charity')]['amount'].sum()/\
                                trust_90day_temp['amount'].sum()
        trust_90day_count_cc = len(trust_90day_temp[trust_90day_temp['match_type'].\
                                                    str.contains('Charity')])/\
                               len(trust_90day_temp)
        nhsengland_90day_temp = nhsengland_pay_df[nhsengland_pay_df['date'].between(lower_bound,
                                                                                    single_date,
                                                                                    inclusive=False)]
        nhsengland_90day_amount_cc = nhsengland_90day_temp[nhsengland_90day_temp['match_type'].\
                                                           str.contains('Charity')]['amount'].sum()/\
                                     nhsengland_90day_temp['amount'].sum()
        nhsengland_90day_count_cc = len(nhsengland_90day_temp[nhsengland_90day_temp['match_type'].\
                                                              str.contains('Charity')])/\
                                    len(nhsengland_90day_temp)
        temp_df.at[single_date, 'CCG_Count'] = ccg_90day_count_cc*100
        temp_df.at[single_date, 'CCG_Amount'] = ccg_90day_amount_cc*100
        temp_df.at[single_date, 'Trust_Count'] = trust_90day_count_cc*100
        temp_df.at[single_date, 'Trust_Amount'] = trust_90day_amount_cc*100
        temp_df.at[single_date, 'NHSEngland_Count'] = nhsengland_90day_count_cc*100
        temp_df.at[single_date, 'NHSEngland_Amount'] = nhsengland_90day_amount_cc*100
    return temp_df


def plot_temporal(ts_ccg_annual, ts_trust_annual, ts_nhsengland_annual,
                  rolling_df_45, rolling_df_365, figure_path):


#    ax3.plot(x1, y1, label='All Charity Commission', color='#d6604d', alpha=0.5, linewidth=2.25)
#    x2, y2 = ecdf(ccgdata_regdate)
#    ax3.plot(x2, y2, label='NHS Suppliers', color='#92c5de', alpha=0.5, linewidth=2.25)
#    x3, y3 = ecdf(cc_adv_date)
#    ax3.plot(x3, y3, label='Advancement of Health', color='#2166ac', alpha=0.5, linewidth=2.25)

    color_list=['#377eb8', '#ffb94e', '#ffeda0']
    titlesize = 16
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    fig = plt.figure(figsize=(12, 12))
    ax1 = plt.subplot2grid((4, 3), (0, 0), colspan=3, rowspan=1)
    ax2 = plt.subplot2grid((4, 3), (1, 0), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid((4, 3), (2, 0), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid((4, 3), (1, 1), colspan=1, rowspan=1)
    ax5 = plt.subplot2grid((4, 3), (2, 1), colspan=1, rowspan=1)
    ax6 = plt.subplot2grid((4, 3), (1, 2), colspan=1, rowspan=1)
    ax7 = plt.subplot2grid((4, 3), (2, 2), colspan=1, rowspan=1)
    ax8 = plt.subplot2grid((4, 3), (3, 0), colspan=3, rowspan=1)

    width=0.225
    rects1 = ax1.bar(np.arange(len(ts_trust_annual)), ts_trust_annual['Count'],
                     width, color=color_list[0], label='NHS Trusts', alpha=0.575, edgecolor='k',
                     linewidth=0.75)
    rects2 = ax1.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Count'],
                     width, color=color_list[1], label='CCGs', alpha=0.575, edgecolor='k',
                     linewidth=0.75)
    rectsX = ax1.bar(np.arange(len(ts_nhsengland_annual))+(2*width), ts_nhsengland_annual['Count'],
                     width, color=color_list[2], label='NHS England', alpha=0.575, edgecolor='k',
                     linewidth=0.75)
    ax1.set_xticks(np.arange(len(ts_trust_annual)) + width)
    ax1.set_xticklabels(ts_trust_annual['Year'])
    ax1.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)
    rects3 = ax8.bar(np.arange(len(ts_trust_annual)), ts_trust_annual['Amount'],
                     width, color=color_list[0], label='NHS Trusts', alpha=0.575, edgecolor='k',
                     linewidth=0.75)
    rects4 = ax8.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Amount'],
                     width, color=color_list[1], label='CCGs', alpha=0.575, edgecolor='k',
                     linewidth=0.75)
    rectsY = ax8.bar(np.arange(len(ts_nhsengland_annual))+(2*width), ts_nhsengland_annual['Amount'],
                     width, color=color_list[2], label='NHS England', alpha=0.575, edgecolor='k',
                     linewidth=0.75)

    ax8.set_xticks(np.arange(len(ts_trust_annual)) + width)
    ax8.set_xticklabels(ts_trust_annual['Year'])
    ax8.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=1)
    ax1.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=3)
    ax8.legend(loc='upper right', edgecolor='k', frameon=False, fontsize=10, ncol=3)
    ax1.set_ylabel('Payments to Non-Profits')
    ax8.set_ylabel('Payments to Non-Profits')
    ax1.set_ylim(0, 5)
#    ax1.tick_params(labelbottom=False)
    for rect in rects1:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    for rect in rects2:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    for rect in rectsX:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)

    for rect in rects3:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    for rect in rects4:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    for rect in rectsY:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    ax2.plot(rolling_df_45['Trust_Count'], color=color_list[0],
             alpha=0.85, linewidth=0.85, label='45 Day Roll')
    ax3.plot(rolling_df_45['Trust_Amount'], color=color_list[0],
             alpha=0.85, linewidth=0.85, label='45 Day Roll')
    ax4.plot(rolling_df_45['CCG_Count'], color=color_list[0],
             alpha=0.85, linewidth=1.25, label='45 Day Roll')
    ax5.plot(rolling_df_45['CCG_Amount'], color=color_list[0],
             alpha=0.85, linewidth=1.25, label='45 Day Roll')
    ax6.plot(rolling_df_45['NHSEngland_Count'], color=color_list[0],
             alpha=0.85, linewidth=1.25, label='45 Day Roll')
    ax7.plot(rolling_df_45['NHSEngland_Amount'], color=color_list[0],
             alpha=0.85, linewidth=1.25, label='45 Day Roll')


    ax2.plot(rolling_df_365['Trust_Count'], color=color_list[1],
             alpha=0.9, linewidth=0.85, label='365 Day Roll')
    ax3.plot(rolling_df_365['Trust_Amount'], color=color_list[1],
             alpha=0.9, linewidth=0.85, label='365 Day Roll')
    ax4.plot(rolling_df_365['CCG_Count'], color=color_list[1],
             alpha=0.85, linewidth=1.25, label='365 Day Roll')
    ax5.plot(rolling_df_365['CCG_Amount'], color=color_list[1],
             alpha=0.85, linewidth=1.25, label='365 Day Roll')
    ax6.plot(rolling_df_365['NHSEngland_Count'], color=color_list[1],
             alpha=0.85, linewidth=1.25, label='365 Day Roll')
    ax7.plot(rolling_df_365['NHSEngland_Amount'], color=color_list[1],
             alpha=0.85, linewidth=1.25, label='365 Day Roll')

    for ax in [ax2, ax3, ax4, ax5, ax6, ax7]:
        ax.legend(loc='upper right', edgecolor='k',
                  frameon=False, fontsize=10)
    ax2.set_ylim(1.2, 2.2)
    ax3.set_ylim(0.4, 1.4)
    ax6.set_ylim(0.4, 1.8)
    ax7.set_ylim(0.4, 1.6)
    ax1.set_title('Number of payments across years', loc='center', size=titlesize-1, y=1.005)
    ax1.set_title('A.', loc='left', size=titlesize-1)
    ax2.set_title('Trusts: Count', loc='center', size=titlesize-3, y=1.005)
    ax2.set_title('B.', loc='left', size=titlesize-1)
    ax3.set_title('Trusts: Amount', loc='center', size=titlesize-3, y=1.005)
    ax3.set_title('E.', loc='left', size=titlesize-1)
    ax4.set_title('CCGs: Count', loc='center', size=titlesize-3, y=1.005)
    ax4.set_title('C.', loc='left', size=titlesize-1)
    ax5.set_title('CCGs: Amount', loc='center', size=titlesize-3, y=1.005)
    ax5.set_title('F.', loc='left', size=titlesize-1)
    ax6.set_title('NHS England: Count', loc='center', size=titlesize-3, y=1.005)
    ax6.set_title('D.', loc='left', size=titlesize-1)
    ax7.set_title('NHS England: Amount', loc='center', size=titlesize-3, y=1.005)
    ax7.set_title('G.', loc='left', size=titlesize-1)
    ax8.set_title('Value of payments across years', loc='center', size=titlesize-1, y=1.005)
    ax8.set_title('H.', loc='left', size=titlesize)

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        sns.despine(ax=ax)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'payments_over_time.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'payments_over_time.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'payments_over_time.png'),
                bbox_inches='tight', dpi=600)


def plot_temporal_makemonths(ts_ccg_monthly, ts_trust_monthly,
                             ts_nhsengland_monthly):
    ts_ccg_monthly = ts_ccg_monthly.rename({'Count': 'Count_CCG',
                                            'Amount':'Amount_CCG'},
                                           axis=1).set_index('Month')
    ts_trust_monthly = ts_trust_monthly.rename({'Count': 'Count_Trust',
                                                'Amount':'Amount_Trust'},
                                               axis=1).set_index('Month')
    ts_nhsengland_monthly = ts_nhsengland_monthly.rename({'Count': 'Count_NHSEngland',
                                                          'Amount':'Amount_NHSEngland'},
                                                         axis=1).set_index('Month')
    merged = pd.merge(ts_ccg_monthly, ts_trust_monthly, how='left',
                      left_index=True, right_index=True)
    merged = pd.merge(merged, ts_nhsengland_monthly, how='left',
                      left_index=True, right_index=True)
    print(merged)


def cyclical_3200(ts_icnpo_plot_ccg):
    ccg_icnpo = ts_icnpo_plot_ccg[ts_icnpo_plot_ccg['ICNPO'].notnull()]
    ccg_icnpo['ICNPO'] = ccg_icnpo['ICNPO'].astype(int)
    ccg_icnpo_ts = pd.pivot_table(ccg_icnpo,
                                  values='Amount',
                                  index=['Year-Month'],
                                  columns='ICNPO')[6:]
    av_3200_april = ccg_icnpo_ts[ccg_icnpo_ts.index.\
                                 str.contains('-04')][3200].mean()
    av_3200_noapril = ccg_icnpo_ts[~ccg_icnpo_ts.index.\
                                   str.contains('-04')][3200].mean()
    print('The average percent of payments going to ICNPO 3200 in April: ',
          round(av_3200_april, 3))
    print('The average percent of payments going to ICNPO 3200 in all other months: ',
          round(av_3200_noapril, 3))
    f, ax = plt.subplots(1, 1, figsize=(16, 3))
    ccg_icnpo_ts[3200][1:].plot(ax=ax, kind='bar', ec='k',
                                alpha=0.65, color='#377eb8')
    sns.despine()
    ax.set_xlabel('')
    ax.set_title('Cyclical Patterns in CCG Payments to ICNPO 3200',
                 loc='center', fontsize=14)
    ax.set_title('A.', loc='left', fontsize=14, y=1.02)
    ax.set_ylabel('Total Payment Amount')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))


def make_inc_table(cc_path, norm_path, nhsengland_pay_df,
                   trust_pay_df, ccg_pay_df, year, outpath):
    cc_name = load_ccname(cc_path, norm_path)
    cc_fin = pd.read_csv(os.path.join(cc_path, 'extract_financial.csv'),
                         warn_bad_lines=False, error_bad_lines=False,
                         parse_dates=['fystart', 'fyend'])
    cc_fin_2018 = cc_fin[cc_fin['fystart'] >= year + '-01-01']
    cc_fin_2018 = cc_fin_2018[cc_fin_2018['fystart'] <= year + '-12-31']
    cc_fin_2018 = cc_fin_2018[cc_fin_2018['income'].notnull()]
    cc_fin_2018 = cc_fin_2018.groupby('regno')['income'].sum().reset_index()
    merge = pd.merge(pd.concat([nhsengland_pay_df, trust_pay_df, ccg_pay_df],
                                ignore_index=True), cc_name, how='left',
                     left_on = 'verif_match', right_on='norm_name')
    cc_fin_2018['inmerge'] = cc_fin_2018["regno"].isin(merge["regno"])
    cc_fin_2018_inmerge = cc_fin_2018[cc_fin_2018['inmerge']]

    merge_byamount = merge.groupby('regno')['amount'].sum().reset_index()
    merge_2018 = pd.merge(merge_byamount, cc_fin_2018,
                          how='left', left_on='regno', right_on='regno')
    merge_2018 = merge_2018[merge_2018['income'].notnull()]

    merge_bycount = merge.groupby(['regno'])['regno'].\
            count().reset_index(name="count")
    merge_2018_c = pd.merge(merge_bycount, cc_fin_2018,
                          how='left', left_on='regno', right_on='regno')
    merge_2018_c = merge_2018_c[merge_2018_c['income'].notnull()]

    micro_amount =  merge_2018[merge_2018['income']<10000]['amount'].sum()
    small_amount =  merge_2018[(merge_2018['income']>=10000) &
                               (merge_2018['income']<=100000)]['amount'].sum()
    med_amount =  merge_2018[(merge_2018['income']>=100000) &
                             (merge_2018['income']<=1000000)]['amount'].sum()
    large_amount =  merge_2018[(merge_2018['income']>=1000000) &
                               (merge_2018['income']<=10000000)]['amount'].sum()
    major_amount =  merge_2018[(merge_2018['income']>=10000000) &
                               (merge_2018['income']<=100000000)]['amount'].sum()
    supermajor_amount =  merge_2018[merge_2018['income']>100000000]['amount'].sum()
    full_amount = merge_2018['amount'].sum()


    micro_count =  merge_2018_c[merge_2018_c['income']<10000]['count'].sum()
    small_count =  merge_2018_c[(merge_2018_c['income']>=10000) &
                                (merge_2018_c['income']<=100000)]['count'].sum()
    med_count =  merge_2018_c[(merge_2018_c['income']>=100000) &
                              (merge_2018_c['income']<=1000000)]['count'].sum()
    large_count =  merge_2018_c[(merge_2018_c['income']>=1000000) &
                                (merge_2018_c['income']<=10000000)]['count'].sum()
    major_count =  merge_2018_c[(merge_2018_c['income']>=10000000) &
                                (merge_2018_c['income']<=100000000)]['count'].sum()
    supermajor_count =  merge_2018_c[merge_2018_c['income']>100000000]['count'].sum()
    full_count = merge_2018_c['count'].sum()

    income_tab = pd.DataFrame(columns=['Minor', 'Small', 'Medium',
                                       'Large', 'Major', 'SuperMajor'],
                              index = ['Entire CCEW', 'Organisation Count',
                                       'Percent of Payments', 'Percent of Amount'])
    # *** Micro ***
    income_tab.at['Entire CCEW','Minor'] = round(len(cc_fin_2018[cc_fin_2018['income']<10000])/
                                                 len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'Minor'] = round(len(cc_fin_2018_inmerge[cc_fin_2018_inmerge['income']<10000])/
                                                        len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'Minor'] = round((micro_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'Minor'] = round((micro_count/full_count)*100, 2)

    # *** Small ***
    income_tab.at['Entire CCEW', 'Small'] = round(len(cc_fin_2018[(cc_fin_2018['income']>=10000) &
                                                     (cc_fin_2018['income']<100000)])/
                                                  len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'Small'] = round(len(cc_fin_2018_inmerge[(cc_fin_2018_inmerge['income']>=10000) &
                                                                                 (cc_fin_2018_inmerge['income']<100000)])/
                                                         len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'Small'] = round((small_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'Small'] = round((small_count/full_count)*100, 2)

    # *** Medium ***
    income_tab.at['Entire CCEW', 'Medium'] = round(len(cc_fin_2018[(cc_fin_2018['income']>=100000) &
                                                     (cc_fin_2018['income']<1000000)])/
                                                  len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'Medium'] = round(len(cc_fin_2018_inmerge[(cc_fin_2018_inmerge['income']>=100000) &
                                                                                 (cc_fin_2018_inmerge['income']<1000000)])/
                                                         len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'Medium'] = round((med_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'Medium'] = round((med_count/full_count)*100, 2)


    # *** Large ***
    income_tab.at['Entire CCEW', 'Large'] = round(len(cc_fin_2018[(cc_fin_2018['income']>=1000000) &
                                                     (cc_fin_2018['income']<10000000)])/
                                                  len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'Large'] = round(len(cc_fin_2018_inmerge[(cc_fin_2018_inmerge['income']>=1000000) &
                                                                                 (cc_fin_2018_inmerge['income']<10000000)])/
                                                         len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'Large'] = round((large_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'Large'] = round((large_count/full_count)*100, 2)

    # *** Major ***
    income_tab.at['Entire CCEW', 'Major'] = round(len(cc_fin_2018[(cc_fin_2018['income']>=10000000) &
                                                     (cc_fin_2018['income']<100000000)])/
                                                  len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'Major'] = round(len(cc_fin_2018_inmerge[(cc_fin_2018_inmerge['income']>=10000000) &
                                                                                 (cc_fin_2018_inmerge['income']<100000000)])/
                                                         len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'Major'] = round((major_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'Major'] = round((major_count/full_count)*100, 2)


    income_tab.at['Entire CCEW','SuperMajor'] = round(len(cc_fin_2018[cc_fin_2018['income']>100000000])/
                                                 len(cc_fin_2018)*100,4)
    income_tab.at['Organisation Count', 'SuperMajor'] = round(len(cc_fin_2018_inmerge[cc_fin_2018_inmerge['income']>100000000])/
                                                        len(cc_fin_2018_inmerge)*100,4)
    income_tab.at['Percent of Amount', 'SuperMajor'] = round((supermajor_amount/full_amount)*100, 2)
    income_tab.at['Percent of Payments', 'SuperMajor'] = round((supermajor_count/full_count)*100, 2)
    print(income_tab)
    income_tab.to_csv(outpath)


def something_with_nuts1(support_path, trust_pay_df, shape_path):
    support = pd.read_csv(os.path.join(shape_path, 'NUTS1', 'joined_points.csv'))
    trust_wnuts = pd.merge(trust_pay_df, support, how='left', left_on='dept', right_on='abrev')
    nuts_am = trust_wnuts.groupby('nuts118nm')['amount'].sum().reset_index()
    nuts_co = trust_wnuts.groupby(['nuts118nm'])['nuts118nm'].\
              count().reset_index(name="count")
    trust_wnuts_ccew = trust_wnuts[trust_wnuts['match_type'].str.contains('Chari')]
    nuts_am_ccew = trust_wnuts_ccew.groupby('nuts118nm')['amount'].\
        sum().reset_index().rename({'amount': 'amount_ccew'}, axis=1)
    nuts_co_ccew = trust_wnuts_ccew.groupby(['nuts118nm'])['nuts118nm'].\
        count().reset_index(name="count_ccew")
    nuts = pd.merge(nuts_am, nuts_co, how='left',
                    left_on='nuts118nm', right_on='nuts118nm')
    nuts = pd.merge(nuts, nuts_co_ccew, how='left',
                    left_on='nuts118nm', right_on='nuts118nm')
    nuts = pd.merge(nuts, nuts_am_ccew, how='left',
                    left_on='nuts118nm', right_on='nuts118nm')
    nuts['count_ccew_pc'] = (nuts['count_ccew']/nuts['count'])*100
    nuts['amount_ccew_pc'] = (nuts['amount_ccew']/nuts['amount'])*100
    nuts = nuts.set_index('nuts118nm')
    print(nuts)
    print('\n')
    total_am = nuts['amount_ccew'].sum()
    total_co = nuts['count_ccew'].sum()
    north_am_cc = nuts.loc['East Midlands (England)', 'amount_ccew'] +\
                  nuts.loc['West Midlands (England)', 'amount_ccew'] +\
                  nuts.loc['North East (England)', 'amount_ccew'] + \
                  nuts.loc['North West (England)', 'amount_ccew'] +\
                  nuts.loc['Yorkshire and The Humber', 'amount_ccew']
    north_co_cc = nuts.loc['East Midlands (England)', 'count_ccew'] +\
                  nuts.loc['West Midlands (England)', 'count_ccew'] +\
                  nuts.loc['North East (England)', 'count_ccew'] + \
                  nuts.loc['North West (England)', 'count_ccew'] +\
                  nuts.loc['Yorkshire and The Humber', 'count_ccew']

    north_co = nuts.loc['East Midlands (England)', 'count'] +\
               nuts.loc['West Midlands (England)', 'count'] +\
               nuts.loc['North East (England)', 'count'] + \
               nuts.loc['North West (England)', 'count'] +\
               nuts.loc['Yorkshire and The Humber', 'count']
    north_am = nuts.loc['East Midlands (England)', 'amount'] +\
               nuts.loc['West Midlands (England)', 'amount'] +\
               nuts.loc['North East (England)', 'amount'] + \
               nuts.loc['North West (England)', 'amount'] +\
               nuts.loc['Yorkshire and The Humber', 'amount']

    south_am_cc = nuts.loc['East of England', 'amount_ccew'] +\
                  nuts.loc['London', 'amount_ccew'] +\
                  nuts.loc['South East (England)', 'amount_ccew'] +\
                  nuts.loc['South West (England)', 'amount_ccew']
    south_co_cc = nuts.loc['East of England', 'count_ccew'] +\
                  nuts.loc['West Midlands (England)', 'count_ccew'] +\
                  nuts.loc['South East (England)','count_ccew'] +\
                  nuts.loc['South West (England)','count_ccew']

    south_am = nuts.loc['East of England', 'amount'] +\
               nuts.loc['London', 'amount'] +\
               nuts.loc['South East (England)', 'amount'] +\
               nuts.loc['South West (England)', 'amount']
    south_co = nuts.loc['East of England', 'count'] +\
               nuts.loc['West Midlands (England)', 'count'] +\
               nuts.loc['South East (England)','count'] +\
               nuts.loc['South West (England)','count']
    print('Percent by count to CCEW in the North: ',
          str(round((north_co_cc/north_co)*100,2)))
    print('Percent by amount to CCEW in the North: ',
          str(round((north_am_cc/north_am)*100,2)))

    print('Percent by count to CCEW in the South: ',
          str(round((south_co_cc/south_co)*100,2)))
    print('Percent by amount to CCEW in the South: ',
          str(round((south_am_cc/south_am)*100,2)))


def make_income_dists(nhsengland_pay_df, trust_pay_df, ccg_pay_df, cc_path, norm_path, figure_path):

    ## Income

    cc_name = load_ccname(cc_path, norm_path)
    cc_fin = pd.read_csv(os.path.join(cc_path, 'extract_financial.csv'),
                         warn_bad_lines=False, error_bad_lines=False,
                         parse_dates=['fystart', 'fyend'])
    print('We have ' + str(len(cc_name['regno'].unique())) + ' regnos in the ccew...')
    print('But only ' + str(len(cc_fin['regno'].unique())) + ' regnos with income data!')

    cc_fin_post2012 = cc_fin[cc_fin['fystart'] >= '2012-01-01']
    cc_fin_post2012 = cc_fin[cc_fin['fystart'] < '2019-01-01']
    cc_fin_post2012 = cc_fin_post2012[cc_fin_post2012['income'].notnull()]
    cc_fin_post2012 = cc_fin_post2012.groupby('regno')['income'].sum().reset_index()

    cc_fin_pre2012 = cc_fin[cc_fin['fystart'] < '2012-01-01']
    cc_fin_post2012 = cc_fin[cc_fin['fystart'] >= '2003-01-01']
    cc_fin_pre2012 = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]
    cc_fin_pre2012 = cc_fin_pre2012.groupby('regno')['income'].sum().reset_index()

    #make nhsengland df
    nhseng_merge = pd.merge(nhsengland_pay_df, cc_name, how='left',
                            left_on = 'verif_match', right_on='norm_name')
    nhseng_byamount = nhseng_merge.groupby('regno')['amount'].sum().reset_index()
    nhseng_post2012 = pd.merge(nhseng_byamount, cc_fin_post2012,
                               how='left', left_on='regno', right_on='regno')
    nhseng_pre2012 = pd.merge(nhseng_byamount, cc_fin_pre2012,
                              how='left', left_on='regno', right_on='regno')
    print('We have ' +
          str(len(nhseng_merge['regno'].unique())),
          ' regnos of NHS England data in total.')
    print('We have ' + str(len(nhseng_post2012[nhseng_post2012['income'].notnull()])) +
          ' rows of NHS England data with post-2012 income data')
    print('We have ' + str(len(nhseng_pre2012[nhseng_pre2012['income'].notnull()])) +
          ' rows of NHS England data with pre-2012 income data')

    #make ccg df
    ccg_merge = pd.merge(ccg_pay_df, cc_name, how='left',
                         left_on = 'verif_match', right_on='norm_name')
    ccg_byamount = ccg_merge.groupby('regno')['amount'].sum().reset_index()
    ccg_post2012 = pd.merge(ccg_byamount, cc_fin_post2012,
                            how='left', left_on='regno', right_on='regno')
    ccg_pre2012 = pd.merge(ccg_byamount, cc_fin_pre2012,
                           how='left', left_on='regno', right_on='regno')
    print('We have ' + str(len(ccg_merge['regno'].unique())),' regnos of CCG data in total.')
    print('We have ' + str(len(ccg_post2012[ccg_post2012['income'].notnull()])) +
          ' rows of CCG data with post-2012 income data')
    print('We have ' + str(len(ccg_pre2012[ccg_pre2012['income'].notnull()])) +
          ' rows of CCG data with pre-2012 income data')

    #trusts
    trust_merge = pd.merge(trust_pay_df, cc_name, how='left',
                         left_on = 'verif_match', right_on='norm_name')
    trust_byamount = trust_merge.groupby('regno')['amount'].sum().reset_index()
    trust_post2012 = pd.merge(trust_byamount, cc_fin_post2012,
                              how='left', left_on='regno', right_on='regno')
    trust_pre2012 = pd.merge(trust_byamount, cc_fin_pre2012,
                             how='left', left_on='regno', right_on='regno')
    print('We have ' +
          str(len(trust_merge['regno'].unique())),
          ' regnos of trust data in total.')
    print('We have ' + str(len(trust_post2012[trust_post2012['income'].notnull()])) +
          ' rows of trust data with post-2012 income data')
    print('We have ' + str(len(trust_pre2012[trust_pre2012['income'].notnull()])) +
          ' rows of trust data with pre-2012 income data')

    # make the df for the uniform plots
    cc_fin_pre2012['intrust'] = cc_fin_pre2012["regno"].isin(trust_merge["regno"])
    cc_fin_pre2012['inccg'] = cc_fin_pre2012["regno"].isin(ccg_merge["regno"])
    cc_fin_pre2012['innhseng'] = cc_fin_pre2012["regno"].isin(nhseng_merge["regno"])
    cc_fin_post2012['intrust'] = cc_fin_post2012["regno"].isin(trust_merge["regno"])
    cc_fin_post2012['inccg'] = cc_fin_post2012["regno"].isin(ccg_merge["regno"])
    cc_fin_post2012['innhseng'] = cc_fin_post2012["regno"].isin(nhseng_merge["regno"])


    titlesize = 15
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    fig = plt.figure(constrained_layout=True, figsize=(12, 6))
    gs = gridspec.GridSpec(4,2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[3, 0])
    ax5 = fig.add_subplot(gs[0, -1])
    ax6 = fig.add_subplot(gs[1, -1])
    ax7 = fig.add_subplot(gs[2, -1])
    ax8 = fig.add_subplot(gs[3, -1])

    trust_array_post = np.log(trust_post2012[trust_post2012['income'].notnull()]['income']+1)
    ccg_array_post = np.log(ccg_post2012[ccg_post2012['income'].notnull()]['income']+1)
    nhseng_array_post = np.log(nhseng_post2012[nhseng_post2012['income'].notnull()]['income']+1)
    ccfin_array_post = np.log(cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income']+1)

    sns.kdeplot(trust_array_post, ax=ax1, shade=True, alpha=0.25,lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(ccg_array_post, ax=ax2, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(nhseng_array_post, ax=ax3, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(ccfin_array_post, ax=ax4, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#ff7f00', legend=False)
    ax1.spines['bottom'].set_visible(True)
    ax2.spines['bottom'].set_visible(True)
    ax3.spines['bottom'].set_visible(True)
    ax4.spines['bottom'].set_visible(True)
    ax1.spines['left'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax4.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_edgecolor('k')
    ax2.spines['bottom'].set_edgecolor('k')
    ax3.spines['bottom'].set_edgecolor('k')
    ax4.spines['bottom'].set_edgecolor('k')
    ax1.set_xticks([])
    ax2.set_xticks([])
    ax3.set_xticks([])
    ax1.set_yticks([])
    ax2.set_yticks([])
    ax3.set_yticks([])
    ax4.set_yticks([])
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax3.set_xlabel('')
    ax4.set_xlabel('Logarithm of cumulative income (+1)')
    sns.despine(ax=ax1, left=True,bottom=False)
    sns.despine(ax=ax2, left=True,bottom=False)
    sns.despine(ax=ax3, left=True,bottom=False)
    sns.despine(ax=ax4, left=True,bottom=False)
    ax1.set_ylim(0,0.225)
    ax2.set_ylim(0,0.225)
    ax3.set_ylim(0,0.225)
    ax4.set_ylim(0,0.225)
    ax1.set_xlim(0,25)
    ax2.set_xlim(0,25)
    ax3.set_xlim(0,25)
    ax4.set_xlim(0,25)
    ax1.set_ylabel('CCG')
    ax2.set_ylabel('Trusts')
    ax3.set_ylabel('NHS England')
    ax4.set_ylabel('CCEW')
    ax1.set_title('Cumulative income distribution post-2012',
                  **csfont, fontsize=titlesize, y=1.05)
    ax1.set_title('A.', **csfont, fontsize=titlesize+5, loc='left', y=1.025)

    trust_array_pre = np.log(trust_pre2012[trust_pre2012['income'].notnull()]['income']+1)
    ccg_array_pre = np.log(ccg_pre2012[ccg_pre2012['income'].notnull()]['income']+1)
    nhseng_array_pre = np.log(nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income']+1)
    ccfin_array_pre = np.log(cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income']+1)

    sns.kdeplot(trust_array_pre, ax=ax5, shade=True, alpha=0.25,lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(ccg_array_pre, ax=ax6, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(nhseng_array_pre, ax=ax7, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#377eb8', legend=False)
    sns.kdeplot(ccfin_array_pre, ax=ax8, shade=True, alpha=0.25, lw=1.2,
                bw=0.5, color='k', facecolor='#ff7f00', legend=False)
    ax5.spines['bottom'].set_visible(True)
    ax6.spines['bottom'].set_visible(True)
    ax7.spines['bottom'].set_visible(True)
    ax8.spines['bottom'].set_visible(True)
    ax5.spines['left'].set_visible(False)
    ax6.spines['left'].set_visible(False)
    ax7.spines['left'].set_visible(False)
    ax8.spines['left'].set_visible(False)
    ax5.spines['bottom'].set_edgecolor('k')
    ax6.spines['bottom'].set_edgecolor('k')
    ax7.spines['bottom'].set_edgecolor('k')
    ax8.spines['bottom'].set_edgecolor('k')
    ax5.set_xticks([])
    ax6.set_xticks([])
    ax7.set_xticks([])
    ax8.set_yticks([])
    ax5.set_yticks([])
    ax6.set_yticks([])
    ax7.set_yticks([])
    ax8.set_yticks([])
    ax5.set_xlabel('')
    ax6.set_xlabel('')
    ax7.set_xlabel('')
    ax8.set_xlabel('Logarithm of cumulative income (+1)')
    sns.despine(ax=ax5, left=True,bottom=False)
    sns.despine(ax=ax6, left=True,bottom=False)
    sns.despine(ax=ax7, left=True,bottom=False)
    sns.despine(ax=ax8, left=True,bottom=False)
    ax5.set_ylim(0,0.225)
    ax6.set_ylim(0,0.225)
    ax7.set_ylim(0,0.225)
    ax8.set_ylim(0,0.225)
    ax5.set_xlim(0,25)
    ax6.set_xlim(0,25)
    ax7.set_xlim(0,25)
    ax8.set_xlim(0,25)
    ax5.set_title('Cumulative income distribution pre-2012',
                  **csfont, fontsize=titlesize, y=1.05)
    ax5.set_title('B.', **csfont, fontsize=titlesize+5, loc='left', y=1.025)

    axy_mean = ccg_post2012[ccg_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(ccg_post2012[ccg_post2012['income'].notnull()]['income'], .1)
    axy_med = ccg_post2012[ccg_post2012['income'].notnull()]['income'].median()
    ax1.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax1.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax1.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = trust_post2012[trust_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(trust_post2012[trust_post2012['income'].notnull()]['income'], .1)
    axy_med = trust_post2012[trust_post2012['income'].notnull()]['income'].median()
    ax2.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax2.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax2.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = nhseng_post2012[nhseng_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(nhseng_post2012[nhseng_post2012['income'].notnull()]['income'], .1)
    axy_med = nhseng_post2012[nhseng_post2012['income'].notnull()]['income'].median()
    ax3.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax3.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax3.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'], .1)
    axy_med = cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'].median()
    ax4.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax4.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax4.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = ccg_pre2012[ccg_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(ccg_pre2012[ccg_pre2012['income'].notnull()]['income'], .1)
    axy_med = ccg_pre2012[ccg_pre2012['income'].notnull()]['income'].median()
    ax5.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax5.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax5.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = trust_pre2012[trust_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(trust_pre2012[trust_pre2012['income'].notnull()]['income'], .1)
    axy_med = trust_pre2012[trust_pre2012['income'].notnull()]['income'].median()
    ax6.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax6.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax6.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'], .1)
    axy_med = nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'].median()
    ax7.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax7.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax7.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    axy_mean = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'], .1)
    axy_med = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'].median()
    ax8.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175))
    ax8.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475))
    ax8.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12))

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.savefig(os.path.join(figure_path, 'income_distributions.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'income_distributions.png'),
                bbox_inches='tight', dpi=500)
    plt.savefig(os.path.join(figure_path, 'income_distributions.pdf'),
                bbox_inches='tight')


def make_obj_freq(cc_objects, cc_name, ccg_pay_df, trust_pay_df,
                  nhsengland_pay_df, figure_path):
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    cc_name['regno'] = pd.to_numeric(cc_name['regno'], errors='coerce')
    cc_name['subno'] = pd.to_numeric(cc_name['subno'], errors='coerce')
    cc_objects['regno'] = pd.to_numeric(cc_objects['regno'], errors='coerce')
    cc_objects['subno'] = pd.to_numeric(cc_objects['subno'], errors='coerce')
    cc_obj_merge = pd.merge(cc_objects, cc_name,
                            how = 'left', left_on=['regno', 'subno'],
                            right_on=['regno', 'subno'])
    cc_obj_merge = cc_obj_merge[cc_obj_merge['norm_name'].notnull()]
    cc_obj_merge = cc_obj_merge [cc_obj_merge['object'].notnull()]
    cc_obj_merge['object']= cc_obj_merge['object'].astype(str).str.lower()
    cc_obj_merge['intrusts'] = cc_obj_merge["norm_name"].isin(trust_pay_df ["verif_match"])
    cc_obj_merge['inccgs'] = cc_obj_merge["norm_name"].isin(ccg_pay_df ["verif_match"])
    cc_obj_merge['innhseng'] = cc_obj_merge["norm_name"].isin(nhsengland_pay_df ["verif_match"])
    df_cc = freq_dist(cc_obj_merge, 'english')
    df_trusts = freq_dist(cc_obj_merge[cc_obj_merge['intrusts']], 'english')
    df_ccgs = freq_dist(cc_obj_merge[cc_obj_merge['inccgs']], 'english')
    df_nhsengland = freq_dist(cc_obj_merge[cc_obj_merge['innhseng']], 'english')
    fig = plt.figure(figsize=(14,12))
    ax = fig.add_subplot(221, projection='polar')
    iN = len(df_cc['count'])
    labs = df_cc.index
    arrCnts = np.array(df_cc['count'])
    theta=np.arange(0,2*np.pi,2*np.pi/iN)
    width = (5*np.pi)/iN
    bottom = 1.33
    ax.set_theta_zero_location('W')
    ax.plot(theta, len(theta)*[1], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                   color='#377eb8', markersize=7, markerfacecolor='w',
                   markeredgecolor='#ff5148')
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax.text(0, 0, label, transform=None,
                      ha='center', va='center')
        renderer = ax.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax.transData._b, color="k", alpha=0.3)
    ax.add_artist(circle)
    ax.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax.set_title('A.', loc='left', y=0.915,  **hfont, fontsize=22, x=-.15)
    ax.set_title("Frequency distribution: Charity Commission 'objects'",
                 loc='center',y=0.92, **hfont, fontsize=15)



    ax2 = fig.add_subplot(222, projection='polar')
    iN = len(df_trusts['count'])
    arrCnts = np.array(df_trusts['count'])
    theta=np.arange(0,2*np.pi,2*np.pi/iN)
    labs = df_trusts.index
    width = (5*np.pi)/iN
    bottom = 1.1
    ax2.set_theta_zero_location('W')
    ax2.plot(theta, len(theta)*[1], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax2.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                    color='#377eb8', markersize=7, markerfacecolor='w',
                    markeredgecolor='#ff5148')
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax2.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax2.text(0, 0, label, transform=None,
                      ha='center', va='center')
        renderer = ax2.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax2.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax2.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax2.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax2.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax2.transData._b, color="k", alpha=0.3)
    ax2.add_artist(circle)
    ax2.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax2.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax2.set_title('B.', loc='left', y=0.915,  **hfont, fontsize=22, x=-.15)
    ax2.set_title("Frequency distribution: NHS Trust 'objects'",
                 loc='center',y=0.92, **hfont, fontsize=15)


    ax3 = fig.add_subplot(223, projection='polar')
    iN = len(df_ccgs['count'])
    arrCnts = np.array(df_ccgs['count'])
    theta=np.arange(0,2*np.pi,2*np.pi/iN)
    width = (5*np.pi)/iN
    labs = df_ccgs.index
    bottom = 0.6
    ax3.set_theta_zero_location('W')
    ax3.plot(theta, len(theta)*[1], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax3.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                   color='#377eb8', markersize=7, markerfacecolor='w', markeredgecolor='#ff5148')
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax3.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax3.text(0, 0, label, transform=None,
                      ha='center', va='center')
        renderer = ax3.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax3.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax3.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax3.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax3.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax3.transData._b, color="k", alpha=0.3)
    ax3.add_artist(circle)
    ax3.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax3.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax3.set_title('C.', loc='left', y=0.915,  **hfont, fontsize=22, x=-.15)
    ax3.set_title("Frequency distribution: CCG 'objects'",
                 loc='center',y=0.92, **hfont, fontsize=15)

    ax4 = fig.add_subplot(224, projection='polar')
    iN = len(df_nhsengland['count'])
    arrCnts = np.array(df_nhsengland['count'])
    theta=np.arange(0,2*np.pi,2*np.pi/iN)
    labs = df_nhsengland.index
    width = (5*np.pi)/iN
    bottom = 1.4
    ax4.set_theta_zero_location('W')
    ax4.plot(theta, len(theta)*[1], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax4.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                   color='#377eb8', markersize=7, markerfacecolor='w', markeredgecolor='#ff5148')
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax4.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax4.text(0, 0, label, transform=None,
                      ha='center', va='center')
        renderer = ax4.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax4.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax4.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax4.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax4.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    #for thet,cnt in zip(theta, arrCnts):
    #    y= np.arange(-5,5,1)
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax4.transData._b, color="k", alpha=0.3)
    ax4.add_artist(circle)
    ax4.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax4.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax4.set_title('D.', loc='left', y=0.915,  **hfont, fontsize=22, x=-.15)
    ax4.set_title("Frequency distribution: NHS England 'objects'",
                 loc='center',y=0.92, **hfont, fontsize=15)

    plt.subplots_adjust(left=-3, bottom=0.1, right=-2, top=1.01, wspace=0, hspace=0)
    plt.savefig(os.path.join(figure_path, 'freq_dist.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'freq_dist.svg'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'freq_dist.png'), bbox_inches='tight', dpi=500)


def freq_dist(df, language):
    sentences = '\n'.join(df['object'].astype(str).tolist())
    stop = nltk.corpus.stopwords.words(language)
    en_stemmer = SnowballStemmer(language)
    words = word_tokenize(sentences, language = language)
    counts = FreqDist(en_stemmer.stem(w) for w in words if w.isalnum() and not w in stop)
    df_fdist = pd.DataFrame.from_dict(counts, orient='index', columns=['count'])
    df_fdist = df_fdist.sort_values(by='count', ascending=False)[:30]
    df_fdist['count'] = (df_fdist['count']/df_fdist['count'].sum())*100
    df_fdist.index = df_fdist.index.str.title() + ': ' + df_fdist['count'].round(1).astype(str) + '%'
    return df_fdist


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
        try:
            ts_plot.loc[i] = [str(year),
                              (count_cc/count)*100,
                              (amount_cc/amount)*100]
        except ZeroDivisionError:
            ts_plot.loc[i] = np.nan
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
            try:
                ts_plot.loc[i] = [str(year), str(month),
                                  str(year)+'-'+str(month),
                                  (count_cc/count)*100,
                                  (amount_cc/amount)*100]
            except ZeroDivisionError:
                ts_plot.loc[i] = np.nan
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
                try:
                    ts_plot_icnpo.loc[i] = [str(year), str(month),
                                            str(year)+'-'+str(month),
                                            str(ICNPO),
                                            (count_icnpo/month_count)*100,
                                            (amount_icnpo/month_amount)*100]
                except ZeroDivisionError:
                    ts_plot_icnpo.loc[i] = np.nan
            if (year == 2020) and (month=='02'):
                break
        if (year == 2020) and (month=='02'):
            break
    return ts_plot, ts_plot_icnpo


def plot_heatmaps(ts_icnpo_plot_trust, ts_icnpo_plot_ccg,
                  ts_icnpo_plot_nhsengland, figure_path):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    titlesize = 15
    sns.set_style('ticks')
    fig = plt.figure(constrained_layout=True, figsize=(16, 9))
    gs = gridspec.GridSpec(2,4, width_ratios=[20,20,20,1], height_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0:1])
    ax2 = fig.add_subplot(gs[0, 1:2])
    ax3 = fig.add_subplot(gs[0, 2:-1])
    ax4 = fig.add_subplot(gs[0, -1])
    ax5 = fig.add_subplot(gs[1, 0:1])
    ax6 = fig.add_subplot(gs[1, 1:2])
    ax7 = fig.add_subplot(gs[1, 2:-1])
    ax8 = fig.add_subplot(gs[1, -1])


    ts_icnpo_plot_trust['ICNPO'] = ts_icnpo_plot_trust['ICNPO'].astype(float)
    ts_icnpo_plot_trust = ts_icnpo_plot_trust[ts_icnpo_plot_trust['ICNPO'].notnull()]
    ts_icnpo_plot_trust['ICNPO'] = ts_icnpo_plot_trust['ICNPO'].astype(int)
    ts_icnpo_plot_ccg['ICNPO'] = ts_icnpo_plot_ccg['ICNPO'].astype(float)
    ts_icnpo_plot_ccg = ts_icnpo_plot_ccg[ts_icnpo_plot_ccg['ICNPO'].notnull()]
    ts_icnpo_plot_ccg['ICNPO'] = ts_icnpo_plot_ccg['ICNPO'].astype(int)
    ts_icnpo_plot_nhsengland['ICNPO'] = ts_icnpo_plot_nhsengland['ICNPO'].astype(float)
    ts_icnpo_plot_nhsengland = ts_icnpo_plot_nhsengland[ts_icnpo_plot_nhsengland['ICNPO'].notnull()]
    ts_icnpo_plot_nhsengland['ICNPO'] = ts_icnpo_plot_nhsengland['ICNPO'].astype(int)

    heatmap_data_trust_count = pd.pivot_table(ts_icnpo_plot_trust,
                                              values='Count',
                                              index=['Year-Month'],
                                              columns='ICNPO')[6:]
    heatmap_data_trust_amount= pd.pivot_table(ts_icnpo_plot_trust,
                                              values='Amount',
                                              index=['Year-Month'],
                                              columns='ICNPO')[6:]
    heatmap_data_ccg_count = pd.pivot_table(ts_icnpo_plot_ccg,
                                            values='Count',
                                            index=['Year-Month'],
                                            columns='ICNPO')[6:]
    heatmap_data_ccg_amount = pd.pivot_table(ts_icnpo_plot_ccg,
                                             values='Amount',
                                             index=['Year-Month'],
                                             columns='ICNPO')[6:]
    heatmap_data_nhsengland_count = pd.pivot_table(ts_icnpo_plot_nhsengland,
                                                   values='Count',
                                                   index=['Year-Month'],
                                                   columns='ICNPO')[6:]
    heatmap_data_nhsengland_amount = pd.pivot_table(ts_icnpo_plot_nhsengland,
                                                    values='Amount',
                                                    index=['Year-Month'],
                                                    columns='ICNPO')[6:]

    heatmap_data_trust_count = heatmap_data_trust_count.fillna(0)
    heatmap_data_trust_amount = heatmap_data_trust_amount.fillna(0)
    heatmap_data_ccg_count = heatmap_data_ccg_count.fillna(0)
    heatmap_data_ccg_amount = heatmap_data_ccg_amount.fillna(0)
    heatmap_data_nhsengland_count = heatmap_data_nhsengland_count.fillna(0)
    heatmap_data_nhsengland_amount = heatmap_data_nhsengland_amount.fillna(0)

    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    vmax_C = pd.concat([heatmap_data_trust_count,
                        heatmap_data_ccg_count,
                        heatmap_data_nhsengland_count]).fillna(0).to_numpy().max()
    vmax_A = pd.concat([heatmap_data_trust_amount,
                        heatmap_data_ccg_amount,
                        heatmap_data_nhsengland_amount]).fillna(0).to_numpy().max()
    ee = sns.heatmap(heatmap_data_trust_count.T, ax=ax1, cmap=my_cmap,
                     xticklabels=12, cbar_ax=None, cbar=False,
                     vmin=0.0000000001, vmax=vmax_C)
    ee.set_xlabel('')
    ee.set_ylabel('ICNPO')
    ee.set_xticks([])
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    ff = sns.heatmap(heatmap_data_trust_amount.T, ax=ax5, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=12, cbar_ax=None, cbar=False, vmax=vmax_A)
    ff.set_xlabel('')
    ff.set_ylabel('ICNPO')
    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    gg = sns.heatmap(heatmap_data_ccg_count.T, ax=ax2, cmap=my_cmap,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     vmin=0.0000000001, cbar_ax=None, cbar=False, vmax=vmax_C)
#    cbar = ax2.collections[0].colorbar
#    cbar.set_label('Total number of payments', labelpad=-65, fontsize=12)
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    gg.set_xticks([])
    gg.set_yticks([])
    gg.set_xlabel('')
    gg.set_ylabel('')
    hh = sns.heatmap(heatmap_data_ccg_amount.T, ax=ax6, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     cbar_ax=None, vmax=vmax_A, cbar=False)
#    cbar = ax5.collections[0].colorbar
#    cbar.set_label('Total value of payments', labelpad=-65, fontsize=12)
    hh.set_xlabel('')
    hh.set_ylabel('')
    hh.set_yticks([])

    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    ii = sns.heatmap(heatmap_data_nhsengland_count.T, ax=ax3, cmap=my_cmap,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     vmin=0.0000000001, cbar_ax=ax4, vmax=vmax_C)
    cbar = ax3.collections[0].colorbar
    cbar.set_label('Total number of payments', labelpad=-65, fontsize=12)
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    ii.set_xticks([])
    ii.set_yticks([])
    ii.set_xlabel('')
    ii.set_ylabel('')
    jj = sns.heatmap(heatmap_data_nhsengland_amount.T,
                     ax=ax7, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=12, cbar_kws={'format': '%.1f%%',
                                               'pad': 0.0575},
                     cbar_ax=ax8, vmax=vmax_A)
    cbar = ax7.collections[0].colorbar
    cbar.set_label('Total value of payments', labelpad=-65, fontsize=12)
    jj.set_xlabel('')
    jj.set_ylabel('')
    jj.set_yticks([])


    ax1.text(x=0.5, y=1.02, s='Payments made by NHS Trusts',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax1.text(x=0.0, y=1.01, s='A.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax2.text(x=0.5, y=1.02, s='Payments made by CCGs',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax2.transAxes,
             **csfont)
    ax2.text(x=0.0, y=1.01, s='B.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax2.transAxes,
             **csfont)

    ax3.text(x=0.5, y=1.02, s='Payments made by NHS England',
             fontsize=titlesize+1, ha='center', va='bottom', transform=ax3.transAxes,
             **csfont)
    ax3.text(x=0.0, y=1.01, s='C.',
             fontsize=titlesize+5, ha='left', va='bottom', transform=ax3.transAxes,
             **csfont)

#    ax5.text(x=0.5, y=1.02, s='Value of payments made by NHS Trusts',
#             fontsize=titlesize+1, ha='center', va='bottom', transform=ax5.transAxes,
#             **csfont)
#    ax5.text(x=0.0, y=1.01, s='D.',# weight='bold',
#             fontsize=titlesize+5, ha='left', va='bottom', transform=ax5.transAxes,
#             **csfont)
#    ax6.text(x=0.5, y=1.02, s='Value of payments made by CCGs',
#             fontsize=titlesize+1, ha='center', va='bottom', transform=ax6.transAxes,
#             **csfont)
#    ax6.text(x=0.0, y=1.01, s='E.',
#             fontsize=titlesize+5, ha='left', va='bottom', transform=ax6.transAxes,
#             **csfont)
#    ax7.text(x=0.5, y=1.02, s='Value of payments made by NHS England',
#             fontsize=titlesize+1, ha='center', va='bottom', transform=ax7.transAxes,
#             **csfont)
#    ax7.text(x=0.0, y=1.01, s='F.',
#             fontsize=titlesize+5, ha='left', va='bottom', transform=ax7.transAxes,
#             **csfont)
    ax5.tick_params(axis='x', rotation=90)
    ax6.tick_params(axis='x', rotation=90)
    ax7.tick_params(axis='x', rotation=90)
    sns.despine(ax=ax1, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax2, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax3, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax5, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax6, top=False, bottom=False, left=False, right=False)
    sns.despine(ax=ax7, top=False, bottom=False, left=False, right=False)
    fig.suptitle('')
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'heatmaps.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.png'),
                bbox_inches='tight', dpi=600)


def class_groupings(pay_df_cc, pay_df_cc_ccg, pay_df_cc_trust,
                    pay_df_cc_nhsengland, cc_name, cc_class, table_path):

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


    #merge in nhsengland
    cc_count_eng = pay_df_cc_nhsengland.groupby(['verif_match'])['verif_match'].\
        count().reset_index(name="count")
    cc_val_eng = pay_df_cc_nhsengland.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_merge_eng = pd.merge(cc_val_eng, cc_count_eng, how='left', on='verif_match')
    cc_merge_eng = pd.merge(cc_merge_eng, cc_name, how='left',
                            left_on='verif_match',
                            right_on='norm_name')
    cc_merge_eng['regno'] = pd.to_numeric(cc_merge_eng['regno'],
                                          errors='coerce')
    cc_merge_eng['regno'] = cc_merge_eng['regno'].astype(float)
    cc_merge_eng['amount'] = cc_merge_eng['amount'].astype(int)
    cc_merge_eng = pd.merge(cc_merge_eng, cc_class, how='left',
                            left_on='regno', right_on='regno')
    cc_class_count_eng = cc_merge_eng.groupby(['classtext'])['classtext'].\
        count().reset_index(name="count_eng")
    cc_class_val_eng = cc_merge_eng.groupby(['classtext'])['amount'].\
        sum().reset_index()
    cc_class_count_eng['count_pc_eng'] = (cc_class_count_eng['count_eng'] /
                                          cc_class_count_eng['count_eng'].sum())*100
    cc_class_val_eng = cc_class_val_eng.rename({'amount':'amount_eng'}, axis=1)
    cc_class_val_eng['amount_pc_eng'] = (cc_class_val_eng['amount_eng'] /
                                         cc_class_val_eng['amount_eng'].sum())*100
    class_merge = pd.merge(class_merge, cc_class_count_eng, how='left',
                               left_on='classtext', right_on='classtext')
    class_merge = pd.merge(class_merge, cc_class_val_eng, how='left',
                               left_on='classtext', right_on='classtext')

    class_merge = class_merge.drop('amount', axis=1)
    class_merge = class_merge.drop('amount_ccg', axis=1)
    class_merge = class_merge.drop('amount_trust', axis=1)
    class_merge = class_merge.drop('amount_eng', axis=1)
    class_merge = class_merge.drop('count', axis=1)
    class_merge = class_merge.drop('count_ccg', axis=1)
    class_merge = class_merge.drop('count_trust', axis=1)
    class_merge = class_merge.drop('count_eng', axis=1)

    class_merge = class_merge.rename({'amount_pc':'amount'}, axis=1)
    class_merge = class_merge.rename({'count_pc':'count'}, axis=1)

    class_merge = class_merge.rename({'amount_pc_ccg':'amo_ccg'}, axis=1)
    class_merge = class_merge.rename({'count_pc_ccg':'cou_ccg'}, axis=1)

    class_merge = class_merge.rename({'amount_pc_trust':'amo_tr'}, axis=1)
    class_merge = class_merge.rename({'count_pc_trust':'cou_tr'}, axis=1)

    class_merge = class_merge.rename({'amount_pc_eng':'amo_eng'}, axis=1)
    class_merge = class_merge.rename({'count_pc_eng':'cou_eng'}, axis=1)

    class_merge = class_merge[['classtext',
                               'amo_ccg', 'cou_ccg',
                               'amo_tr', 'cou_tr',
                               'amo_eng', 'cou_eng']].round(2)
    print(class_merge)
    class_merge.to_csv(os.path.join(table_path, 'class_table.csv'), index=False)


def charity_age(cc_pay_df, cc_sup, cc_name, cc_class, figure_path):
    titlesize = 15
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    ccgdata_regdate = cc_sup[cc_sup['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    cc_regdate = cc_name[cc_name['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    cc_pay_df_with_cc = pd.merge(cc_pay_df, cc_name, how='left',
                                 left_on='verif_match', right_on='norm_name')
    cc_pay_classtext = pd.merge(cc_pay_df_with_cc, cc_class, how='left',
                                  left_on='regno', right_on='regno')
    cc_pay_adv = cc_pay_classtext[cc_pay_classtext['classtext']=='The Advancement Of Health Or Saving Of Lives']

    cc_adv_date = cc_pay_adv[cc_pay_adv['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    g = sns.distplot(ccgdata_regdate, ax=ax1, kde_kws={'gridsize': 500, 'color': '#377eb8'},
                     hist_kws={'color': '#377eb8', 'alpha': 0.25,
                               'edgecolor': 'k', 'linewidth':1},
                     label='NHS Suppliers',
                     bins=np.arange(1950, 2020, 3))
    g = sns.distplot(cc_regdate, ax=ax1, kde_kws={'gridsize': 500, 'color': '#ff7f00'},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.25,
                               'edgecolor': 'k', 'linewidth':1},
                     label='All CC', bins=np.arange(1950, 2020, 3))
    ax1.set_ylabel("Normalized Frequency", fontsize=12)
    ax1.set_xlabel("Charity Registration Year", fontsize=12)
#    ax1.set_ylim(0, 0.048)
    ax1.set_title('Distributions of Registration Years',
                  **csfont, fontsize=titlesize, y=1.02)
    ax1.set_title('A.', **csfont, fontsize=titlesize+5, loc='left', y=1.01)
    sns.despine()
    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)

    a = cc_sup[cc_sup['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    b = cc_name[cc_name['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    percs = np.linspace(0, 100, 40)
    qn_a = np.percentile(a, percs)
    qn_b = np.percentile(b, percs)
    x = np.linspace(np.min((qn_a.min(), qn_b.min())),
                    np.max((qn_a.max(), qn_b.max())))
    ax2.plot(x, x, color='k', ls="--", alpha=0.5)
    ax2.plot(qn_a, qn_b, ls="", marker="o", color='#377eb8', alpha=0.25,
             markersize=12.5, fillstyle='full', markeredgecolor='#ff7f00')
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
    ax3.plot(x1, y1, label='All Charity Commission', color='#d6604d', alpha=0.5, linewidth=2.25)
    x2, y2 = ecdf(ccgdata_regdate)
    ax3.plot(x2, y2, label='NHS Suppliers', color='#92c5de', alpha=0.5, linewidth=2.25)
    x3, y3 = ecdf(cc_adv_date)
    ax3.plot(x3, y3, label='Advancement of Health', color='#2166ac', alpha=0.5, linewidth=2.25)
    ax3.set_ylabel("Proportion of Data", fontsize=12)
    ax3.set_xlabel("Charity Registration Years", fontsize=12)
    ax3.set_title('Empirical Cumulative Distribution',
                  **csfont, fontsize=titlesize, y=1.02)
    ax3.set_title('C.', loc='left',
                  **csfont, fontsize=titlesize+5, y=1.01)
    ax3.legend(loc='upper left', edgecolor='k',
               frameon=False, fontsize=10)
    h = sns.distplot(ccgdata_regdate, ax=ax4, kde_kws={'gridsize': 500, 'color': '#377eb8'},
                     hist_kws={'color': '#377eb8', 'alpha': 0.25,
                               'edgecolor': 'k', 'linewidth':1}, label='NHS Suppliers',
                     bins=np.arange(1950, 2020, 3))
    h = sns.distplot(cc_adv_date, ax=ax4, kde_kws={'gridsize': 500, 'color': '#ff7f00'},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.25,
                               'edgecolor': 'k', 'linewidth':1},
                     label='All Advancement of Health', bins=np.arange(1950, 2020, 3))
    ax4.set_ylabel("Normalized Frequency", fontsize=12)
    ax4.set_xlabel("Charity Registration Year", fontsize=12)
    ax4.set_title('Comparison with Healthcare Charities',
                  **csfont, fontsize=titlesize, y=1.02)
    ax4.set_title('D.',
                  **csfont, fontsize=titlesize+5, loc='left', y=1.01)
    h.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)
    ax1.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax2.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax2.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax3.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    sns.despine(ax=ax1, top=False, left=False, right=False, bottom=False)
    sns.despine(ax=ax2, top=False, left=False, right=False, bottom=False)
    sns.despine(ax=ax3, top=False, left=False, right=False, bottom=False)
    sns.despine(ax=ax4, top=False, left=False, right=False, bottom=False)
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
    ax1.set_title('Total Volume of Payments', **csfont, fontsize=titlesize+2,y=1.1)
    ax1.set_title('A.', **csfont, fontsize=titlesize+8, loc='left', y=1)

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
    ax2.set_title('Cumulative Payment Amount', **csfont, fontsize=titlesize+2, y=1.1)
    ax2.set_title('B.', **csfont, fontsize=titlesize+8, loc='left', y=1.0)

    count_array = gdf[gdf['pc_count']!='No Data']['pc_count'].astype(float)
    ee = sns.distplot(count_array, ax=ax3, kde_kws={'color': '#4e94ff', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#4e94ff', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                      bins=20)
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")

    count_array = gdf[gdf['pc_amount']!='No Data']['pc_amount'].astype(float)
    ff = sns.distplot(count_array, ax=ax4, kde_kws={'color': '#ffb94e', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#ffb94e', 'alpha': 0.5,
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
    print(gdf[['dept', 'charity_amount',
               'pc_amount', 'charity_count']].sort_values(by='pc_amount',
                                                          ascending=False)[0:5])


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
    ax1.set_title('Total Volume of Payments', **csfont, fontsize=titlesize+2, y=1.1)
    ax1.set_title('A.', **csfont, fontsize=titlesize+8, loc='left', y=1)

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
    ax2.set_title('Cumulative Payment Amount', **csfont, fontsize=titlesize+2, y=1.1)
    ax2.set_title('B.', **csfont, fontsize=titlesize+8, loc='left', y=1)

    count_array = gdf[gdf['count_pc_cc']!='No Data']['count_pc_cc'].astype(float)
    ee = sns.distplot(count_array, ax=ax3, kde_kws={'color': '#4e94ff', 'alpha':0.9,
                                                    'label':'KDE', 'linewidth': 1},
                      hist_kws={'color': '#4e94ff', 'alpha': 0.5,
                               'edgecolor': 'k', 'label': 'Histogram'},
                               bins=20)
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")

#    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)
    count_array = gdf[gdf['amount_pc_cc']!='No Data']['amount_pc_cc'].astype(float)
    ff = sns.distplot(count_array, ax=ax4, kde_kws={'color': '#ffb94e', 'alpha':0.9,
                                                    'label':'KDE', 'linewidth': 1},
                      hist_kws={'color': '#ffb94e', 'alpha': 0.5,
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
    print(gdf[['dept', 'amount_cc',
               'amount_pc_cc', 'count_cc']].sort_values(by='amount_pc_cc',
                                                        ascending=False)[0:5])


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

def icnpo_groupings(pay_df, pay_df_ccg, pay_df_trust, pay_df_nhsengland,
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

    #nhsengland_df
    cc_df_nhsengland = pay_df_nhsengland[pay_df_nhsengland['match_type'].str.contains('Charity')]
    cc_count_nhsengland = cc_df_nhsengland.groupby(['verif_match'])['verif_match'].\
                     count().reset_index(name="count_eng")
    cc_val_nhsengland = cc_df_nhsengland.groupby(['verif_match'])['amount'].sum().reset_index()
    cc_val_nhsengland = cc_val_nhsengland.rename({'amount': 'amount_eng'}, axis=1)
    cc_merge_nhsengland = pd.merge(cc_val_nhsengland, cc_count_nhsengland,
                                   how='left', on='verif_match')
    cc_merge_nhsengland = cc_merge_nhsengland[~cc_merge_nhsengland['verif_match'].\
               str.contains('FOUNDATION TRUST')]
    cc_merge_nhsengland = pd.merge(cc_merge_nhsengland, cc_name, how='left',
                                   left_on='verif_match', right_on='norm_name')
    cc_merge_nhsengland['regno'] = pd.to_numeric(cc_merge_nhsengland['regno'], errors='coerce')
    cc_merge_nhsengland = cc_merge_nhsengland[cc_merge_nhsengland['regno'].notnull()]
    cc_merge_nhsengland['regno'] = cc_merge_nhsengland['regno'].astype(int)
    cc_merge_nhsengland['amount_eng'] = cc_merge_nhsengland['amount_eng'].astype(int)
    cc_merge_nhsengland = pd.merge(cc_merge_nhsengland, icnpo_df, on=['regno'],
                                   how='left', indicator=False)
    cc_merge_nhsengland['ICNPO'] = cc_merge_nhsengland['ICNPO'].fillna(9999)
    cc_merge_nhsengland['ICNPO'] = cc_merge_nhsengland['ICNPO'].astype(int)
    cc_merge_nhsengland = cc_merge_nhsengland.drop(columns=['name', 'norm_name', 'subno',
                                                            'nameno', 'regno', 'verif_match'])
    amount_icnpo_pc_nhsengland = cc_merge_nhsengland.groupby(['ICNPO'])['amount_eng'].sum().rename("amount_eng")
    amount_icnpo_pc_nhsengland = amount_icnpo_pc_nhsengland.reset_index()
    amount_icnpo_pc_nhsengland['amount_eng'] = (amount_icnpo_pc_nhsengland['amount_eng']/
                                                       amount_icnpo_pc_nhsengland['amount_eng'].sum())*100
    count_icnpo_pc_nhsengland = cc_merge_nhsengland.groupby(['ICNPO'])['ICNPO'].count().reset_index(name = "count_eng")
    count_icnpo_pc_nhsengland['count_eng'] = (count_icnpo_pc_nhsengland['count_eng']/
                                                     count_icnpo_pc_nhsengland['count_eng'].sum())*100
    sum_icnpo_pc_nhsengland = cc_merge_nhsengland.groupby(['ICNPO'])['amount_eng'].sum().reset_index()
    sum_icnpo_pc_nhsengland['amount_eng'] = (sum_icnpo_pc_nhsengland['amount_eng']/
                                             sum_icnpo_pc_nhsengland['amount_eng'].sum())*100

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

    icnpo_out = pd.merge(icnpo_out, count_icnpo_pc_nhsengland, how='left', left_on = 'ICNPO',
                         right_on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc_nhsengland, how='left', on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = icnpo_out.drop(columns=['icnpo_desc', 'icnpo_desc', 'in_original_spec'])
    icnpo_out = icnpo_out[icnpo_out['ICNPO'].notnull()]
    icnpo_out['icnpo'] = icnpo_out['ICNPO'].astype(int)
    icnpo_out['icnpo'] = icnpo_out['ICNPO'].fillna(9999)
    for col in ['count_ccg', 'amount_ccg',
                'count_trust','amount_trust',
                'count_eng', 'amount_eng']:
        icnpo_out[col] = icnpo_out[col].fillna(0)
    icnpo_out['icnpo'] = icnpo_out['icnpo'].astype(int)
    icnpo_out = icnpo_out.drop(columns=['ICNPO']).set_index('icnpo')
    icnpo_out = icnpo_out.drop(columns=['amount'])
    icnpo_out = icnpo_out.drop(columns=['count'])
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
