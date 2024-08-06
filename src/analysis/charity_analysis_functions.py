import os
import sys
import json
import string
import requests
import datetime
from datetime import timedelta, date
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from matplotlib.colors import rgb2hex

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from matplotlib.ticker import FuncFormatter

from scipy import stats
import pysal.viz.mapclassify as mc

from geopandas import GeoDataFrame
from geopandas import points_from_xy
import geopandas as gpd
import statsmodels.api as sm

csfont = {'fontname': 'Helvetica'}

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



#np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25


def possibly_public(trust_pay_df, ccg_pay_df, nhsengland_pay_df):
    trust_pay_df['data_type'] = 'Trusts'
    ccg_pay_df['data_type'] = 'CCGs'
    nhsengland_pay_df['data_type'] = 'NHS_Eng'
    concat = pd.concat([trust_pay_df, ccg_pay_df, nhsengland_pay_df], ignore_index=True)

    public = concat[['date', 'expensetype', 'expensearea', 'supplier', 'amount', 'data_type']].copy()

    possible_substrings = ['council', 'municipality', 'local auth',
                           'library', 'government', 'police',
                           'department of', 'her majest', 'job centre']

    public['Possibly_Public'] = 0

    for term in possible_substrings:
        public['is_' + term] = 0
        public['Possibly_Public'] = np.where(public['supplier'].str.lower().str.contains(term), 1,
                                             public['Possibly_Public'])
        public['is_' + term] = np.where(public['supplier'].str.lower().str.contains(term), 1, public['is_' + term])
        print('There are a total of {} strings containing: {}'.format(public['is_' + term].sum(), term))

    print('There are a total of {} possibly public strings'.format(public['Possibly_Public'].sum()))
    print('This is {}% of all payments'.format(np.round(public['Possibly_Public'].sum() / len(public) * 100, 2)))
    print('The value of these payments is: ',
          np.round(public[public['Possibly_Public']==1]['amount'].sum()))
    print('As a percent, this represents: ',
          np.round(public[public['Possibly_Public'] == 1]['amount'].sum()/
                   public['amount'].sum()*100))
    print('The mean value of these payments is: ',
          np.round(public[public['Possibly_Public']==1]['amount'].mean()))
    result_df = public[public['Possibly_Public'] == 1]['data_type'].value_counts().reset_index()
    result_df.columns = ['data_type', 'count']
    result_df['pc_all_public'] = result_df['count'] / result_df['count'].sum() * 100
    result_df = result_df.set_index('data_type')

    result_df.loc['CCGs', 'pc_within_type'] = np.round(result_df.loc['CCGs', 'count'] / len(ccg_pay_df) * 100, 2)
    result_df.loc['Trusts', 'pc_within_type'] = np.round(result_df.loc['Trusts', 'count'] / len(trust_pay_df) * 100, 2)
    result_df.loc['NHS_Eng', 'pc_within_type'] = np.round(
        result_df.loc['NHS_Eng', 'count'] / len(nhsengland_pay_df) * 100, 2)

    print(result_df.to_markdown(index=True))
    print("\nThe most commonly seen 'Possibly Public' entities:")
    print(public[public['Possibly_Public']==1]['supplier'].value_counts().head(5).to_markdown(index=True))


def make_rolling_windows_top10(ccg_pay_df, trust_pay_df, nhsengland_pay_df,
                               combined_pay_df, window):
    daterange = pd.date_range(date(2013, 12, 1), date(2019, 10, 1), freq='d')
    temp_df = pd.DataFrame(index=daterange, columns=['CCG_Amount_5',
                                                     'Trust_Amount_5',
                                                     'NHSEngland_Amount_5',
                                                     'Combined_Amount_5',
                                                     'CCG_Amount_10',
                                                     'Trust_Amount_10',
                                                     'NHSEngland_Amount_10',
                                                     'Combined_Amount_10',
                                                     'CCG_Amount_20',
                                                     'Trust_Amount_20',
                                                     'NHSEngland_Amount_20',
                                                     'Combined_Amount_20'])
    for single_date in daterange:
        lower_bound = single_date - pd.Timedelta(window, unit='d')
        ccg_90day_temp = ccg_pay_df[ccg_pay_df['date'].between(lower_bound,
                                                               single_date,
                                                               inclusive='neither')]
        trust_90day_temp = trust_pay_df[trust_pay_df['date'].between(lower_bound,
                                                                     single_date,
                                                                     inclusive='neither')]
        nhsengland_90day_temp = nhsengland_pay_df[nhsengland_pay_df['date'].between(lower_bound,
                                                                                    single_date,
                                                                                    inclusive='neither')]
        combined_90day_temp = combined_pay_df[combined_pay_df['date'].between(lower_bound,
                                                                              single_date,
                                                                              inclusive='neither')]
        charity_ccg = ccg_90day_temp[ccg_90day_temp['match_type'].str.contains('Charity')]
        charity_ccg_groupby_sum = charity_ccg.groupby(['CharityRegNo'])['amount'].sum()
        charity_ccg_groupby_sum = charity_ccg_groupby_sum.reset_index().sort_values(by = 'amount', ascending=False)
        charity_ccg_groupby_sum = charity_ccg_groupby_sum.reset_index()
        ccg_amount_5 = charity_ccg_groupby_sum['amount'][0:5].sum()/charity_ccg_groupby_sum['amount'].sum()
        ccg_amount_10 = charity_ccg_groupby_sum['amount'][0:10].sum()/charity_ccg_groupby_sum['amount'].sum()
        ccg_amount_20 = charity_ccg_groupby_sum['amount'][0:20].sum()/charity_ccg_groupby_sum['amount'].sum()
#        charity_ccg_groupby_count = charity_ccg.groupby(['verif_match'])['amount'].count()
#        charity_ccg_groupby_count = charity_ccg_groupby_count.sort_values(ascending=False)
#        ccg_count = charity_ccg_groupby_count[0:5].sum()/charity_ccg_groupby_count.sum()

        charity_trust = trust_90day_temp[trust_90day_temp['match_type'].str.contains('Charity')]
        charity_trust_groupby_sum = charity_trust.groupby(['CharityRegNo'])['amount'].sum()
        charity_trust_groupby_sum = charity_trust_groupby_sum.reset_index().sort_values(by = 'amount', ascending=False)
        charity_trust_groupby_sum = charity_trust_groupby_sum.reset_index()
        trust_amount_5 = charity_trust_groupby_sum['amount'][0:5].sum()/charity_trust_groupby_sum['amount'].sum()
        trust_amount_10 = charity_trust_groupby_sum['amount'][0:10].sum()/charity_trust_groupby_sum['amount'].sum()
        trust_amount_20 = charity_trust_groupby_sum['amount'][0:20].sum()/charity_trust_groupby_sum['amount'].sum()
#        charity_trust_groupby_count = charity_trust.groupby(['verif_match'])['amount'].count()
#        charity_trust_groupby_count = charity_trust_groupby_count.sort_values(ascending=False)
#        trust_count = charity_trust_groupby_count[0:5].sum()/charity_trust_groupby_count.sum()

        charity_nhsengland = nhsengland_90day_temp[nhsengland_90day_temp['match_type'].str.contains('Charity')]
        charity_nhsengland_groupby_sum = charity_nhsengland.groupby(['CharityRegNo'])['amount'].sum()
        charity_nhsengland_groupby_sum = charity_nhsengland_groupby_sum.reset_index().sort_values(by = 'amount', ascending=False)
        charity_nhsengland_groupby_sum = charity_nhsengland_groupby_sum.reset_index()
        nhsengland_amount_5 = charity_nhsengland_groupby_sum['amount'][0:5].sum()/charity_nhsengland_groupby_sum['amount'].sum()
        nhsengland_amount_10 = charity_nhsengland_groupby_sum['amount'][0:10].sum()/charity_nhsengland_groupby_sum['amount'].sum()
        nhsengland_amount_20 = charity_nhsengland_groupby_sum['amount'][0:20].sum()/charity_nhsengland_groupby_sum['amount'].sum()
#        charity_nhsengland_groupby_count = charity_nhsengland.groupby(['verif_match'])['amount'].count()
#        charity_nhsengland_groupby_count = charity_nhsengland_groupby_count.sort_values(ascending=False)
#        nhsengland_count = charity_nhsengland_groupby_count[0:5].sum()/charity_nhsengland_groupby_count.sum()

        charity_combined = combined_90day_temp[combined_90day_temp['match_type'].str.contains('Charity')]
        charity_combined_groupby_sum = charity_combined.groupby(['CharityRegNo'])['amount'].sum()
        charity_combined_groupby_sum = charity_combined_groupby_sum.reset_index().sort_values(by = 'amount', ascending=False)
        charity_combined_groupby_sum = charity_combined_groupby_sum.reset_index()
        combined_amount_5 = charity_combined_groupby_sum['amount'][0:5].sum()/charity_combined_groupby_sum['amount'].sum()
        combined_amount_10 = charity_combined_groupby_sum['amount'][0:10].sum()/charity_combined_groupby_sum['amount'].sum()
        combined_amount_20 = charity_combined_groupby_sum['amount'][0:20].sum()/charity_combined_groupby_sum['amount'].sum()
#        charity_combined_groupby_count = charity_combined.groupby(['verif_match'])['amount'].count()
#        charity_combined_groupby_count = charity_combined_groupby_count.sort_values(ascending=False)
#        combined_count = charity_combined_groupby_count[0:5].sum()/charity_combined_groupby_count.sum()

        #temp_df.at[single_date, 'CCG_Count'] = ccg_count
        #temp_df.at[single_date, 'Trust_Count'] = trust_count
        #temp_df.at[single_date, 'NHSEngland_Count'] = nhsengland_count
        #temp_df.at[single_date, 'Combined_Count'] = combined_count
        temp_df.at[single_date, 'CCG_Amount_5'] = ccg_amount_5
        temp_df.at[single_date, 'Trust_Amount_5'] = trust_amount_5
        temp_df.at[single_date, 'NHSEngland_Amount_5'] = nhsengland_amount_5
        temp_df.at[single_date, 'Combined_Amount_5'] = combined_amount_5
        temp_df.at[single_date, 'CCG_Amount_10'] = ccg_amount_10
        temp_df.at[single_date, 'Trust_Amount_10'] = trust_amount_10
        temp_df.at[single_date, 'NHSEngland_Amount_10'] = nhsengland_amount_10
        temp_df.at[single_date, 'Combined_Amount_10'] = combined_amount_10
        temp_df.at[single_date, 'CCG_Amount_20'] = ccg_amount_20
        temp_df.at[single_date, 'Trust_Amount_20'] = trust_amount_20
        temp_df.at[single_date, 'NHSEngland_Amount_20'] = nhsengland_amount_20
        temp_df.at[single_date, 'Combined_Amount_20'] = combined_amount_20
    return temp_df


def plot_conc(figure_path, rolling_df_45_top10, rolling_df_90_top10,
              rolling_df_180_top10, rolling_df_365_top10):
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(13, 11))
    csfont = {'fontname': 'Helvetica'}
    colors = ['#41558c', '#E89818', '#CF202A']
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    rolling_df_180_top10['CCG_Amount_5'].plot(ax=ax1, color=color1, alpha=0.8)
    rolling_df_180_top10['CCG_Amount_10'].plot(ax=ax1, color=color2, alpha=0.8)
    rolling_df_180_top10['CCG_Amount_20'].plot(ax=ax1, color=color3, alpha=0.8)

    rolling_df_180_top10['Trust_Amount_5'].plot(ax=ax2, color=color1, alpha=0.8)
    rolling_df_180_top10['Trust_Amount_10'].plot(ax=ax2, color=color2, alpha=0.8)
    rolling_df_180_top10['Trust_Amount_20'].plot(ax=ax2, color=color3, alpha=0.8)

    rolling_df_180_top10['NHSEngland_Amount_5'].plot(ax=ax3, color=color1, alpha=0.8)
    rolling_df_180_top10['NHSEngland_Amount_10'].plot(ax=ax3, color=color2, alpha=0.8)
    rolling_df_180_top10['NHSEngland_Amount_20'].plot(ax=ax3, color=color3, alpha=0.8)

    rolling_df_180_top10['Combined_Amount_5'].plot(ax=ax4, color=color1, alpha=0.8)
    rolling_df_180_top10['Combined_Amount_10'].plot(ax=ax4, color=color2, alpha=0.8)
    rolling_df_180_top10['Combined_Amount_20'].plot(ax=ax4, color=color3, alpha=0.8)
    ax1.set_title('a.', loc='left', size=21, y=1.02)
    ax2.set_title('b.', loc='left', size=21, y=1.02)
    ax3.set_title('c.', loc='left', size=21, y=1.02)
    ax4.set_title('d.', loc='left', size=21, y=1.02)
    ax1.set_ylabel('Concentration Ratio: CCGs', **csfont, size=14)
    ax2.set_ylabel('Concentration Ratio: Trusts', **csfont, size=14)
    ax3.set_ylabel('Concentration Ratio: NHS England', **csfont, size=14)
    ax4.set_ylabel('Concentration Ratio: Combined', **csfont, size=14)
    ax2.legend(loc='upper right', edgecolor=(0, 0, 0,1),
               frameon=True, fontsize=11, labels=['Top 5 Non-Profits',
                                                  'Top 10 Non-Profits',
                                                  'Top 20 Non-Profits'],
               facecolor='w', framealpha=1)
    legend = ax2.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    ax3.set_xlabel('Time', **csfont, size=14)
    ax4.set_xlabel('Time', **csfont, size=14)
    sns.despine()
    plt.tight_layout(pad=3.5)
    plt.savefig(os.path.join(figure_path, 'concentrations.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'concentrations.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'concentrations.png'),
                bbox_inches='tight', dpi=800)



def make_rolling_windows(ccg_pay_df, trust_pay_df, nhsengland_pay_df, window):
    if window == 365:
        daterange = pd.date_range(date(2013, 12, 1), date(2019, 10, 1), freq='d')
    elif window == 90:
        daterange = pd.date_range(date(2013, 12, 1), date(2019, 10, 1), freq='d')

    temp_df = pd.DataFrame(index=daterange, columns=['CCG_Count',
                                                     'CCG_Amount',
                                                     'Trust_Count',
                                                     'Trust_Amount',
                                                     'NHSEngland_Count',
                                                     'NHSEngland_Amount',
                                                     'All_Count',
                                                     'All_Amount'])
    comb_pay_df = pd.concat([ccg_pay_df, trust_pay_df, nhsengland_pay_df], ignore_index=True)
    for single_date in daterange:
        lower_bound = single_date - pd.Timedelta(window, unit='d')
        ccg_90day_temp = ccg_pay_df[ccg_pay_df['date'].between(lower_bound,
                                                               single_date,
                                                               inclusive='neither')]
        ccg_90day_amount_cc = ccg_90day_temp[ccg_90day_temp['match_type'].\
                                             str.contains('Charity')]['amount'].sum()/\
                              ccg_90day_temp['amount'].sum()
        ccg_90day_count_cc = len(ccg_90day_temp[ccg_90day_temp['match_type'].\
                                             str.contains('Charity')])/\
                              len(ccg_90day_temp)
        trust_90day_temp = trust_pay_df[trust_pay_df['date'].between(lower_bound,
                                                                     single_date,
                                                                     inclusive='neither')]
        trust_90day_amount_cc = trust_90day_temp[trust_90day_temp['match_type'].\
                                                 str.contains('Charity')]['amount'].sum()/\
                                trust_90day_temp['amount'].sum()
        trust_90day_count_cc = len(trust_90day_temp[trust_90day_temp['match_type'].\
                                                    str.contains('Charity')])/\
                               len(trust_90day_temp)
        nhsengland_90day_temp = nhsengland_pay_df[nhsengland_pay_df['date'].between(lower_bound,
                                                                                    single_date,
                                                                                    inclusive='neither')]
        nhsengland_90day_amount_cc = nhsengland_90day_temp[nhsengland_90day_temp['match_type'].\
                                                           str.contains('Charity')]['amount'].sum()/\
                                     nhsengland_90day_temp['amount'].sum()
        nhsengland_90day_count_cc = len(nhsengland_90day_temp[nhsengland_90day_temp['match_type'].\
                                                              str.contains('Charity')])/\
                                    len(nhsengland_90day_temp)




        comb_90day_temp = comb_pay_df[comb_pay_df['date'].between(lower_bound,
                                                                  single_date,
                                                                  inclusive='neither')]
        comb_90day_amount_cc = comb_90day_temp[comb_90day_temp['match_type']. \
            str.contains('Charity')]['amount'].sum() / \
                                     comb_90day_temp['amount'].sum()
        comb_90day_count_cc = len(comb_90day_temp[comb_90day_temp['match_type']. \
                                        str.contains('Charity')]) / \
                              len(comb_90day_temp)


        temp_df.at[single_date, 'CCG_Count'] = ccg_90day_count_cc*100
        temp_df.at[single_date, 'CCG_Amount'] = ccg_90day_amount_cc*100
        temp_df.at[single_date, 'Trust_Count'] = trust_90day_count_cc*100
        temp_df.at[single_date, 'Trust_Amount'] = trust_90day_amount_cc*100
        temp_df.at[single_date, 'NHSEngland_Count'] = nhsengland_90day_count_cc*100
        temp_df.at[single_date, 'NHSEngland_Amount'] = nhsengland_90day_amount_cc*100
        temp_df.at[single_date, 'All_Amount'] = comb_90day_amount_cc*100
        temp_df.at[single_date, 'All_Count'] = comb_90day_count_cc * 100
        temp_df.at[single_date, 'CCG_Median'] = ccg_90day_temp['amount'].median()
        temp_df.at[single_date, 'Trust_Median'] = trust_90day_temp['amount'].median()
        temp_df.at[single_date, 'NHSEngland_Median'] = nhsengland_90day_temp['amount'].median()
        temp_df.at[single_date, 'All_Median'] = comb_90day_temp['amount'].median()
    return temp_df


def plot_temporal(ts_ccg_annual, ts_trust_annual, ts_nhsengland_annual,
                  rolling_df_45, rolling_df_365, figure_path):

    import matplotlib.ticker as mtick
#    ax3.plot(x1, y1, label='All Charity Commission', color='#d6604d', alpha=0.5, linewidth=2.25)
#    x2, y2 = ecdf(ccgdata_regdate)
#    ax3.plot(x2, y2, label='NHS Suppliers', color='#92c5de', alpha=0.5, linewidth=2.25)
#    x3, y3 = ecdf(cc_adv_date)
#    ax3.plot(x3, y3, label='Advancement of Health', color='#2166ac', alpha=0.5, linewidth=2.25)

    colors = ['#41558c', '#E89818', '#CF202A']
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
                     width, color=colors[0], label='NHS Trusts', alpha=1, edgecolor='k',
                     linewidth=1)
    rects2 = ax1.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Count'],
                     width, color=colors[1], label='CCGs', alpha=1, edgecolor='k',
                     linewidth=1)
    rectsX = ax1.bar(np.arange(len(ts_nhsengland_annual))+(2*width), ts_nhsengland_annual['Count'],
                     width, color=colors[2], label='NHS England', alpha=1, edgecolor='k',
                     linewidth=1)
    ax1.set_xticks(np.arange(len(ts_trust_annual)) + width)
    ax1.set_xticklabels(ts_trust_annual['Year'])
    rects3 = ax8.bar(np.arange(len(ts_trust_annual)), ts_trust_annual['Amount'],
                     width, color=colors[0], label='NHS Trusts', alpha=1, edgecolor='k',
                     linewidth=1)
    rects4 = ax8.bar(np.arange(len(ts_ccg_annual))+width, ts_ccg_annual['Amount'],
                     width, color=colors[1], label='CCGs', alpha=1, edgecolor='k',
                     linewidth=1)
    rectsY = ax8.bar(np.arange(len(ts_nhsengland_annual))+(2*width), ts_nhsengland_annual['Amount'],
                     width, color=colors[2], label='NHS England', alpha=1, edgecolor='k',
                     linewidth=1)

    ax8.set_xticks(np.arange(len(ts_trust_annual)) + width)
    ax8.set_xticklabels(ts_trust_annual['Year'])
    ax1.legend(loc='upper right', edgecolor='k', frameon=True, framealpha=1, fontsize=10, ncol=3)
    ax8.legend(loc='upper right', edgecolor='k', frameon=True, framealpha=1, fontsize=10, ncol=3)

    ax1.set_ylabel('Payments to Non-Profits', **csfont, fontsize=13)
    ax2.set_ylabel('Payments to Non-Profits', **csfont, fontsize=13)
    ax3.set_ylabel('Payments to Non-Profits', **csfont, fontsize=13)
    ax8.set_ylabel('Payments to Non-Profits', **csfont, fontsize=13)

    ax1.set_ylim(0, 5.5)
#    ax1.tick_params(labelbottom=False)
    for rect in rects1:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)
    for rect in rects2:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)
    for rect in rectsX:
        height = rect.get_height()
        ax1.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)

    for rect in rects3:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)
    for rect in rects4:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)
    for rect in rectsY:
        height = rect.get_height()
        ax8.annotate(str(round(height,1))+'%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=7)
    ax2.plot(rolling_df_45['Trust_Count'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')
    ax3.plot(rolling_df_45['Trust_Amount'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')
    ax4.plot(rolling_df_45['CCG_Count'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')
    ax5.plot(rolling_df_45['CCG_Amount'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')
    ax6.plot(rolling_df_45['NHSEngland_Count'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')
    ax7.plot(rolling_df_45['NHSEngland_Amount'], color=colors[0],
             alpha=1, linewidth=1, label='45 Day Roll')


    ax2.plot(rolling_df_365['Trust_Count'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')
    ax3.plot(rolling_df_365['Trust_Amount'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')
    ax4.plot(rolling_df_365['CCG_Count'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')
    ax5.plot(rolling_df_365['CCG_Amount'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')
    ax6.plot(rolling_df_365['NHSEngland_Count'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')
    ax7.plot(rolling_df_365['NHSEngland_Amount'], color=colors[1],
             alpha=1, linewidth=1, label='365 Day Roll')

#    for ax in [ax2, ax3, ax4, ax5]:
#        ax.legend(loc='upper right', edgecolor='k',
#                  frameon=False, fontsize=10)
#    for ax in [ax6, ax7]:
#        ax.legend(loc='upper left', edgecolor='k',
#                  frameon=False, fontsize=10)

    ax6.legend(loc='upper left', edgecolor='k', frameon=True, fontsize=10, ncol=1)
    legend = ax6.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)

    legend = ax1.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)

    legend = ax8.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)


#    ax2.set_ylim(1.2, 2.2)
#    ax3.set_ylim(0.4, 1.4)
#    ax6.set_ylim(0.4, 1.8)
#    ax7.set_ylim(0.4, 1.6)
    ax8.set_ylim(0.0, 1.4)

    #ax8.set_xlim(-0.525, 8.5)
    #ax1.set_xlim(-0.525, 8.5)
    #ax1.set_title('Number of payments across years', loc='center', size=titlesize-1, y=1.005)
    ax1.set_title('a.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax2.set_title('Trusts: Count', loc='center', size=titlesize-3, y=1.005)
    ax2.set_title('b.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax3.set_title('Trusts: Amount', loc='center', size=titlesize-3, y=1.005)
    ax3.set_title('c.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax4.set_title('CCGs: Count', loc='center', size=titlesize-3, y=1.005)
    ax4.set_title('d.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax5.set_title('CCGs: Amount', loc='center', size=titlesize-3, y=1.005)
    #ax6.set_title('NHS England: Count', loc='center', size=titlesize-3, y=1.005)
    ax5.set_title('e.', loc='left', size=titlesize-1, y=1.025, **csfont)
    ax6.set_title('f.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax7.set_title('NHS England: Amount', loc='center', size=titlesize-3, y=1.005)
    ax7.set_title('g.', loc='left', size=titlesize-1, y=1.025, **csfont)
    #ax8.set_title('Value of payments across years', loc='center', size=titlesize-1, y=1.005)
    ax8.set_title('h.', loc='left', size=titlesize, y=1.025, **csfont)

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        sns.despine(ax=ax)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    plt.tight_layout(pad=2.5)
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
                         on_bad_lines='skip',
                         parse_dates=['fystart', 'fyend'])
    cc_fin_2018 = cc_fin[cc_fin['fystart'] >= year + '-01-01']
    cc_fin_2018 = cc_fin_2018[cc_fin_2018['fystart'] <= year + '-12-31']
    cc_fin_2018 = cc_fin_2018[cc_fin_2018['income'].notnull()]
    cc_fin_2018 = cc_fin_2018.groupby('regno')['income'].sum().reset_index()
    merge = pd.concat([nhsengland_pay_df, trust_pay_df, ccg_pay_df], ignore_index=True)
#    merge = pd.merge(pd.concat([nhsengland_pay_df, trust_pay_df, ccg_pay_df],
#                                ignore_index=True), cc_name, how='left',
#                     left_on='CharityRegNo', right_on='regno')
    cc_fin_2018['inmerge'] = cc_fin_2018["regno"].isin(merge["CharityRegNo"])
    cc_fin_2018_inmerge = cc_fin_2018[cc_fin_2018['inmerge']]

    merge_byamount = merge.groupby('CharityRegNo')['amount'].sum().reset_index()
    merge_2018 = pd.merge(merge_byamount, cc_fin_2018,
                          how='left', left_on='CharityRegNo', right_on='regno')
    merge_2018 = merge_2018[merge_2018['income'].notnull()]

    merge_bycount = merge.groupby(['CharityRegNo'])['CharityRegNo'].\
            count().reset_index(name="count")
    merge_2018_c = pd.merge(merge_bycount, cc_fin_2018,
                          how='left', left_on='CharityRegNo', right_on='regno')
    merge_2018_c = merge_2018_c[merge_2018_c['income'].notnull()]

    micro_amount = merge_2018[merge_2018['income'] < 10000]['amount'].sum()
    small_amount = merge_2018[(merge_2018['income'] >= 10000) &
                               (merge_2018['income'] <= 100000)]['amount'].sum()
    med_amount = merge_2018[(merge_2018['income'] >= 100000) &
                             (merge_2018['income'] <= 1000000)]['amount'].sum()
    large_amount = merge_2018[(merge_2018['income'] >= 1000000) &
                               (merge_2018['income'] <= 10000000)]['amount'].sum()
    major_amount = merge_2018[(merge_2018['income'] >= 10000000) &
                               (merge_2018['income'] <= 100000000)]['amount'].sum()
    supermajor_amount =  merge_2018[merge_2018['income'] > 100000000]['amount'].sum()
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

    color1='#41558c'
    color2= '#E89818'

    cc_name = load_ccname(cc_path, norm_path)
    cc_fin = pd.read_csv(os.path.join(cc_path, 'extract_financial.csv'),
                         on_bad_lines='skip',
                         parse_dates=['fystart', 'fyend'])
    print('We have ' + str(len(cc_name[cc_name['regno'].notnull()]['regno'].unique())) + ' regnos in the ccew...')
    print('We have ' + str(len(cc_fin[cc_fin['regno'].notnull()]['regno'].unique())) + ' regnos with income data!')

    cc_fin_post2012 = cc_fin[cc_fin['fystart'] >= '2012-01-01']
    cc_fin_post2012 = cc_fin[cc_fin['fystart'] < '2019-01-01']
    cc_fin_post2012 = cc_fin_post2012[cc_fin_post2012['income'].notnull()]
    cc_fin_post2012 = cc_fin_post2012.groupby('regno')['income'].sum().reset_index()

    cc_fin_pre2012 = cc_fin[cc_fin['fystart'] < '2012-01-01']
    cc_fin_post2012 = cc_fin[cc_fin['fystart'] >= '2003-01-01']
    cc_fin_pre2012 = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]
    cc_fin_pre2012 = cc_fin_pre2012.groupby('regno')['income'].sum().reset_index()

    #make nhsengland df
    #nhseng_merge = pd.merge(nhsengland_pay_df, cc_name, how='left',
    #                        left_on = 'verif_match', right_on='norm_name')
    nhseng_byamount = nhsengland_pay_df.groupby('CharityRegNo')['amount'].sum().reset_index()
    nhseng_post2012 = pd.merge(nhseng_byamount, cc_fin_post2012,
                               how='left', left_on='CharityRegNo', right_on='regno')
    nhseng_pre2012 = pd.merge(nhseng_byamount, cc_fin_pre2012,
                              how='left', left_on='CharityRegNo', right_on='regno')
    print('We have ' +
          str(len(nhsengland_pay_df['CharityRegNo'].unique())) +
          ' regnos of NHS England data in total.')
    print('We have ' + str(len(nhseng_post2012[nhseng_post2012['income'].notnull()])) +
          ' rows of NHS England data with post-2012 income data')
    print('We have ' + str(len(nhseng_pre2012[nhseng_pre2012['income'].notnull()])) +
          ' rows of NHS England data with pre-2012 income data')

    #make ccg df
    #ccg_merge = pd.merge(ccg_pay_df, cc_name, how='left',
    #                     left_on = 'verif_match', right_on='norm_name')
    ccg_byamount = ccg_pay_df.groupby('CharityRegNo')['amount'].sum().reset_index()
    ccg_post2012 = pd.merge(ccg_byamount, cc_fin_post2012,
                            how='left', left_on='CharityRegNo', right_on='regno')
    ccg_pre2012 = pd.merge(ccg_byamount, cc_fin_pre2012,
                           how='left', left_on='CharityRegNo', right_on='regno')
    print('We have ' + str(len(ccg_pay_df['CharityRegNo'].unique())) + ' regnos of CCG data in total.')
    print('We have ' + str(len(ccg_post2012[ccg_post2012['income'].notnull()])) +
          ' rows of CCG data with post-2012 income data')
    print('We have ' + str(len(ccg_pre2012[ccg_pre2012['income'].notnull()])) +
          ' rows of CCG data with pre-2012 income data')

    #trusts
    #trust_merge = pd.merge(trust_pay_df, cc_name, how='left',
    #                     left_on = 'verif_match', right_on='norm_name')
    trust_byamount = trust_pay_df.groupby('CharityRegNo')['amount'].sum().reset_index()
    trust_post2012 = pd.merge(trust_byamount, cc_fin_post2012,
                              how='left', left_on='CharityRegNo', right_on='regno')
    trust_pre2012 = pd.merge(trust_byamount, cc_fin_pre2012,
                             how='left', left_on='CharityRegNo', right_on='regno')
    print('We have ' +
          str(len(trust_pay_df['CharityRegNo'].unique())),
          ' regnos of trust data in total.')
    print('We have ' + str(len(trust_post2012[trust_post2012['income'].notnull()])) +
          ' rows of trust data with post-2012 income data')
    print('We have ' + str(len(trust_pre2012[trust_pre2012['income'].notnull()])) +
          ' rows of trust data with pre-2012 income data')

    # make the df for the uniform plots nhsengland_pay_df, trust_pay_df, ccg_pay_df
    cc_fin_pre2012 = cc_fin_pre2012.copy()
    cc_fin_pre2012.loc[:, 'intrust'] = cc_fin_pre2012["regno"].isin(trust_pay_df["CharityRegNo"])
    cc_fin_pre2012.loc[:, 'inccg'] = cc_fin_pre2012["regno"].isin(ccg_pay_df["CharityRegNo"])
    cc_fin_pre2012.loc[:, 'innhseng'] = cc_fin_pre2012["regno"].isin(nhsengland_pay_df["CharityRegNo"])
    cc_fin_post2012 = cc_fin_post2012.copy()
    cc_fin_post2012.loc[:, 'intrust'] = cc_fin_post2012["regno"].isin(trust_pay_df["CharityRegNo"])
    cc_fin_post2012.loc[:, 'inccg'] = cc_fin_post2012["regno"].isin(ccg_pay_df["CharityRegNo"])
    cc_fin_post2012.loc[:, 'innhseng'] = cc_fin_post2012["regno"].isin(nhsengland_pay_df["CharityRegNo"])

    titlesize = 15
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    fig = plt.figure(figsize=(12, 8))
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

    sns.kdeplot(trust_array_post, ax=ax1, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(ccg_array_post, ax=ax2, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(nhseng_array_post, ax=ax3, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(ccfin_array_post, ax=ax4, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color2, legend=False)
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
    ax4.set_xlabel('Logarithm of cumulative income (+1): Post-2012', fontsize=14)
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
    ax1.set_ylabel('CCG', fontsize=14)
    ax2.set_ylabel('Trusts', fontsize=14)
    ax3.set_ylabel('NHS England', fontsize=14)
    ax4.set_ylabel('CCEW', fontsize=14)

#    ax1.set_title('Cumulative income distribution post-2012',
#                  **csfont, fontsize=titlesize, y=1.05)
    ax1.set_title('a.', **csfont, fontsize=titlesize+5, loc='left', y=1.025)

    trust_array_pre = np.log(trust_pre2012[trust_pre2012['income'].notnull()]['income']+1)
    ccg_array_pre = np.log(ccg_pre2012[ccg_pre2012['income'].notnull()]['income']+1)
    nhseng_array_pre = np.log(nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income']+1)
    ccfin_array_pre = np.log(cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income']+1)

    sns.kdeplot(trust_array_pre, ax=ax5, fill=True, alpha=0.6, lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(ccg_array_pre, ax=ax6, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(nhseng_array_pre, ax=ax7, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color1, legend=False)
    sns.kdeplot(ccfin_array_pre, ax=ax8, fill=True, alpha=0.6,lw=1,
                bw_method=0.5, color='k', facecolor=color2, legend=False)
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
    ax8.set_xlabel('Logarithm of cumulative income (+1): Pre-2012', fontsize=14)
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
#    ax5.set_title('Cumulative income distribution pre-2012',
#                  **csfont, fontsize=titlesize, y=1.05)
    ax5.set_title('b.', **csfont, fontsize=titlesize+5, loc='left', y=1.025)

    axy_mean = ccg_post2012[ccg_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(ccg_post2012[ccg_post2012['income'].notnull()]['income'], .1)
    axy_med = ccg_post2012[ccg_post2012['income'].notnull()]['income'].median()
    ax1.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax1.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax1.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = trust_post2012[trust_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(trust_post2012[trust_post2012['income'].notnull()]['income'], .1)
    axy_med = trust_post2012[trust_post2012['income'].notnull()]['income'].median()
    ax2.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax2.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax2.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = nhseng_post2012[nhseng_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(nhseng_post2012[nhseng_post2012['income'].notnull()]['income'], .1)
    axy_med = nhseng_post2012[nhseng_post2012['income'].notnull()]['income'].median()
    ax3.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax3.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax3.annotate('Trimmed Mean: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'], .1)
    axy_med = cc_fin_post2012[cc_fin_post2012['income'].notnull()]['income'].median()
    ax4.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax4.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax4.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = ccg_pre2012[ccg_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(ccg_pre2012[ccg_pre2012['income'].notnull()]['income'], .1)
    axy_med = ccg_pre2012[ccg_pre2012['income'].notnull()]['income'].median()
    ax5.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax5.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax5.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = trust_pre2012[trust_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(trust_pre2012[trust_pre2012['income'].notnull()]['income'], .1)
    axy_med = trust_pre2012[trust_pre2012['income'].notnull()]['income'].median()
    ax6.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax6.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax6.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'], .1)
    axy_med = nhseng_pre2012[nhseng_pre2012['income'].notnull()]['income'].median()
    ax7.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax7.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax7.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    axy_mean = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'].mean()
    axy_trimmed = stats.trim_mean(cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'], .1)
    axy_med = cc_fin_pre2012[cc_fin_pre2012['income'].notnull()]['income'].median()
    ax8.annotate('Mean: £' + str(int(axy_mean/1000000)) + 'm', xy=(1, 0.175), fontsize=13)
    ax8.annotate('Median: £' + str(int(axy_med/1000000)) + 'm', xy=(1, 0.1475), fontsize=13)
    ax8.annotate('Trimmed: £' + str(int(axy_trimmed/1000000)) + 'm', xy=(1, 0.12), fontsize=13)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.savefig(os.path.join(figure_path, 'income_distributions.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'income_distributions.png'),
                bbox_inches='tight', dpi=500)
    plt.savefig(os.path.join(figure_path, 'income_distributions.pdf'),
                bbox_inches='tight')


def make_obj_freq(cc_objects, #cc_name,
                  ccg_pay_df, trust_pay_df,
                  nhsengland_pay_df, figure_path):
    import nltk
    colors = ['#41558c', '#E89818', '#CF202A']
    nltk.download('stopwords')
    nltk.download('punkt')
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    cc_objects['regno'] = pd.to_numeric(cc_objects['regno'], errors='coerce')
    cc_objects = cc_objects[cc_objects['object'].notnull()]
    cc_objects = cc_objects.copy()
    cc_objects.loc[:, 'object'] = cc_objects['object'].astype(str).str.lower()
    cc_objects.loc[:, 'intrusts'] = cc_objects["regno"].isin(trust_pay_df ["CharityRegNo"])
    cc_objects.loc[:, 'inccgs'] = cc_objects["regno"].isin(ccg_pay_df ["CharityRegNo"])
    cc_objects.loc[:, 'innhseng'] = cc_objects["regno"].isin(nhsengland_pay_df ["CharityRegNo"])
    df_cc = freq_dist(cc_objects, 'english')
    df_trusts = freq_dist(cc_objects[cc_objects['intrusts']], 'english')
    df_ccgs = freq_dist(cc_objects[cc_objects['inccgs']], 'english')
    df_nhsengland = freq_dist(cc_objects[cc_objects['innhseng']], 'english')
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
                   color=colors[0], markersize=9, markerfacecolor='w',
                   markeredgecolor=colors[2])
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax.text(0, 0, label, transform=None,
                      ha='center', va='center', fontsize=10)
        renderer = ax.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax.fill_between(theta, arrCnts, alpha=0.075, color=colors[1])
    ax.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax.transData._b, color="k", alpha=0.3)
    ax.add_artist(circle)
    ax.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax.set_title('a.', loc='left', y=0.9,  **hfont, fontsize=22, x=-.15)
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
                    color=colors[0], markersize=9, markerfacecolor='w',
                    markeredgecolor=colors[2])
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax2.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax2.text(0, 0, label, transform=None,
                      ha='center', va='center', fontsize=10)
        renderer = ax2.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax2.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax2.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax2.fill_between(theta, arrCnts, alpha=0.075, color=colors[1])
    ax2.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax2.transData._b, color="k", alpha=0.3)
    ax2.add_artist(circle)
    ax2.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax2.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax2.set_title('b.', loc='left', y=0.9,  **hfont, fontsize=22, x=-.15)
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
                   color=colors[0], markersize=9, markerfacecolor='w',
                    markeredgecolor=colors[2])
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax3.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax3.text(0, 0, label, transform=None,
                      ha='center', va='center', fontsize=10)
        renderer = ax3.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax3.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax3.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax3.fill_between(theta, arrCnts, alpha=0.075, color=colors[1])
    ax3.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax3.transData._b, color="k", alpha=0.3)
    ax3.add_artist(circle)
    ax3.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax3.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax3.set_title('c.', loc='left', y=0.9,  **hfont, fontsize=22, x=-.15)
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
                   color=colors[0], markersize=9, markerfacecolor='w',
                    markeredgecolor=colors[2])
    plt.axis('off')
    rotations = np.rad2deg(theta)
    y0,y1 = ax4.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom+bar)/(y1-y0)
        lab = ax4.text(0, 0, label, transform=None,
                      ha='center', va='center', fontsize=10)
        renderer = ax4.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax4.transData.inverted().transform([[0,0],[bbox.width,0] ])
        lab.set_position((x,offset+(invb[1][0]-invb[0][0])))
        lab.set_transform(ax4.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax4.fill_between(theta, arrCnts, alpha=0.075, color=colors[1])
    ax4.fill_between(theta, len(theta)*[1], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax4.transData._b, color="k", alpha=0.3)
    ax4.add_artist(circle)
    ax4.plot((0, theta[0]), ( 0, arrCnts[0]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax4.plot((0, theta[-1]), ( 0, arrCnts[-1]-.175), color='k',linewidth=1, alpha=0.5, linestyle='--')
    ax4.set_title('d.', loc='left', y=0.9,  **hfont, fontsize=22, x=-.15)
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
    now = pd.Timestamp.now()
    cc_sup_age = cc_sup[cc_sup['regdate'].notnull()]
    cc_sup_age = cc_sup_age.copy()
    cc_sup_age.loc[:, 'regdate'] = pd.to_datetime(cc_sup_age['regdate'],
                                                  format='%m%d%y')
    cc_sup_age.loc[:, 'age'] = (now - cc_sup_age['regdate']).dt.days#.astype('timedelta64[D]')
    print('Correlation between age and amount: ',
          cc_sup_age['age'].corr(cc_sup_age['amount']))
    print('Correlation between age and count:',
          cc_sup_age['age'].corr(cc_sup_age['count']))
    cc_sup_age.loc[:, 'age_rank'] = cc_sup_age['age'].rank()
    cc_sup_age.loc[:, 'amount_rank'] = cc_sup_age['amount'].rank()
    cc_sup_age.loc[:, 'count_rank'] = cc_sup_age['count'].rank()
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
    cc_sup_age1 = cc_sup_age1.copy()
    cc_sup_age1.loc[:, 'regdate'] = pd.to_datetime(cc_sup_age1['regdate'],
                                                   format='%m%d%y')
    cc_sup_age1.loc[:, 'age'] = (now - cc_sup_age1['regdate']).dt.days#.astype('timedelta64[D]')
    print('Correlation between age and amount: ',
          cc_sup_age1['age'].corr(cc_sup_age1['amount']))
    print('Correlation between age and count:',
          cc_sup_age1['age'].corr(cc_sup_age1['count']))
    cc_sup_age1.loc[:, 'age_rank'] = cc_sup_age1['age'].rank()
    cc_sup_age1.loc[:, 'amount_rank'] = cc_sup_age1['amount'].rank()
    cc_sup_age1.loc[:, 'count_rank'] = cc_sup_age1['count'].rank()
    print('Correlation betwen age and amount, by rank: ',
          cc_sup_age1['age_rank'].corr(cc_sup_age1['amount_rank'],
                                       method='spearman'))
    print('Correlation between age and count, by rank: ',
          cc_sup_age1['age_rank'].corr(cc_sup_age1['count_rank'],
                                       method='spearman'))


def make_monthly(pay_df, pay_df_cc):
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


def make_annual(pay_df, pay_df_cc):
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

def make_temporal_df(pay_df, pay_df_cc, icnpo_df
                     #, cc_name):
                     ):
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
#    pay_merge = pd.merge(pay_df_cc, cc_name, how='left',
#                         left_on='verif_match',
#                         right_on='norm_name')
    pay_merge = pd.merge(pay_df_cc, icnpo_df, how='left',
                         left_on='CharityRegNo', right_on='regno')
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
    gs = gridspec.GridSpec(2, 4,
                           width_ratios=[20, 20, 20, 1],
                           height_ratios=[1, 1],
                           figure=fig)
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
    ts_icnpo_plot_nhsengland = ts_icnpo_plot_nhsengland.copy()
    ts_icnpo_plot_nhsengland.loc[:, 'ICNPO'] = ts_icnpo_plot_nhsengland['ICNPO'].astype(int)

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
    plt.savefig(os.path.join(figure_path, 'heatmaps.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.png'),
                bbox_inches='tight', dpi=600)


def class_groupings(pay_df_cc, pay_df_cc_ccg, pay_df_cc_trust,
                    pay_df_cc_nhsengland, #cc_name,
                    cc_class, table_path):

    # full dataframe
    cc_count = pay_df_cc.groupby(['CharityRegNo'])['CharityRegNo'].\
        count().reset_index(name="count")
    cc_val = pay_df_cc.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='CharityRegNo')
#    cc_merge = pd.merge(cc_merge, cc_name, how='left',
#                        left_on='verif_match',
#                        right_on='norm_name')
    cc_merge['CharityRegNo'] = pd.to_numeric(cc_merge['CharityRegNo'],
                                             errors='coerce')
    cc_merge['CharityRegNo'] = cc_merge['CharityRegNo'].astype(float)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, cc_class, how='left',
                        left_on='CharityRegNo', right_on='regno')
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
    cc_count_ccg = pay_df_cc_ccg.groupby(['CharityRegNo'])['CharityRegNo'].\
        count().reset_index(name="count")
    cc_val_ccg = pay_df_cc_ccg.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge_ccg = pd.merge(cc_val_ccg, cc_count_ccg, how='left', on='CharityRegNo')
#    cc_merge_ccg = pd.merge(cc_merge_ccg, cc_name, how='left',
#                            left_on='verif_match',
#                            right_on='norm_name')
    cc_merge_ccg['CharityRegNo'] = pd.to_numeric(cc_merge_ccg['CharityRegNo'],
                                                 errors='coerce')
    cc_merge_ccg['CharityRegNo'] = cc_merge_ccg['CharityRegNo'].astype(float)
    cc_merge_ccg['amount'] = cc_merge_ccg['amount'].astype(int)
    cc_merge_ccg = pd.merge(cc_merge_ccg, cc_class, how='left',
                            left_on='CharityRegNo', right_on='regno')
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
    cc_count_trust = pay_df_cc_trust.groupby(['CharityRegNo'])['CharityRegNo'].\
        count().reset_index(name="count")
    cc_val_trust = pay_df_cc_trust.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge_trust = pd.merge(cc_val_trust, cc_count_trust, how='left', on='CharityRegNo')
#    cc_merge_trust = pd.merge(cc_merge_trust, cc_name, how='left',
#                            left_on='verif_match',
#                            right_on='norm_name')
    cc_merge_trust['CharityRegNo'] = pd.to_numeric(cc_merge_trust['CharityRegNo'],
                                                   errors='coerce')
    cc_merge_trust['CharityRegNo'] = cc_merge_trust['CharityRegNo'].astype(float)
    cc_merge_trust['amount'] = cc_merge_trust['amount'].astype(int)
    cc_merge_trust = pd.merge(cc_merge_trust, cc_class, how='left',
                            left_on='CharityRegNo', right_on='regno')
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
    cc_count_eng = pay_df_cc_nhsengland.groupby(['CharityRegNo'])['CharityRegNo'].\
        count().reset_index(name="count")
    cc_val_eng = pay_df_cc_nhsengland.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge_eng = pd.merge(cc_val_eng, cc_count_eng, how='left', on='CharityRegNo')
#    cc_merge_eng = pd.merge(cc_merge_eng, cc_name, how='left',
#                            left_on='verif_match',
#                            right_on='norm_name')
    cc_merge_eng['CharityRegNo'] = pd.to_numeric(cc_merge_eng['CharityRegNo'],
                                                 errors='coerce')
    cc_merge_eng['CharityRegNo'] = cc_merge_eng['CharityRegNo'].astype(float)
    cc_merge_eng['amount'] = cc_merge_eng['amount'].astype(int)
    cc_merge_eng = pd.merge(cc_merge_eng, cc_class, how='left',
                            left_on='CharityRegNo', right_on='regno')
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
    order_list = class_merge.sort_values(ascending=False, by='amount')['classtext'].to_list()
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
    class_merge = class_merge.set_index('classtext')
    class_merge = class_merge.reindex(order_list)
    print(class_merge)
    class_merge.to_csv(os.path.join(table_path, 'class_table.csv'))


def charity_age(allcc_pay_df, cc_sup, cc_name, cc_class, figure_path):
    colors = ['#41558c', '#E89818', '#CF202A']
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    titlesize = 15
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    cc_sup = pd.merge(cc_sup, cc_name, how='left', left_on='CharityRegNo', right_on='regno')
    allsups_data_regdate = cc_sup[cc_sup['regdate'].notnull()]['regdate'].astype(str).str[0:4].astype(float)
    cc_regdate = cc_name[cc_name['regdate'].notnull()]['regdate'].astype(str).str[0:4].astype(float)
    allcc_pay_df_with_cc = pd.merge(allcc_pay_df, cc_name, how='left',
                                    left_on='CharityRegNo', right_on='regno')
    cc_pay_classtext = pd.merge(allcc_pay_df_with_cc, cc_class, how='left',
                                 left_on='CharityRegNo', right_on='regno')
    cc_pay_adv = cc_pay_classtext[cc_pay_classtext['classtext']=='The Advancement Of Health Or Saving Of Lives']

    cc_adv_date = cc_pay_adv[cc_pay_adv['regdate'].notnull()].drop_duplicates(subset=['regno_x'])['regdate'].\
        astype(str).str[0:4].astype(float)
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10.5))
    g = sns.distplot(allsups_data_regdate, ax=ax1, kde_kws={'gridsize': 500, 'color': color1},
                     label='NHS Suppliers',
                     hist=False)
    g = sns.distplot(cc_regdate, ax=ax1, kde_kws={'gridsize': 500, 'color': color2},
                     label='All CC',
                     hist=False)
    ax1.set_ylabel("Normalized Frequency", fontsize=14)
    ax1.set_xlabel("Charity Registration Year", fontsize=14)
    ax1.set_title('a.', **csfont, fontsize=titlesize+6, loc='left', y=1.02)
    sns.despine()
    g.legend(loc='upper left', edgecolor='k', facecolor='w', frameon=True, fontsize=10, framealpha=1)



    a = cc_sup[cc_sup['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    b = cc_name[cc_name['regdate'].notnull()].drop_duplicates(subset=['regno'])['regdate'].\
        astype(str).str[0:4].astype(float)
    percs = np.linspace(0, 100, 40)
    qn_a = np.percentile(a, percs)
    qn_b = np.percentile(b, percs)
    x = np.linspace(np.min((qn_a.min(), qn_b.min())),
                    np.max((qn_a.max(), qn_b.max())))
    ax2.plot(x, x, color='k', ls="--", alpha=0.75)
    ax2.plot(qn_a, qn_b, ls="", marker="o", color=color1, alpha=1,
             markersize=10, fillstyle='full', markeredgecolor='k',
            linewidth=0.25)
    ax2.set_ylabel("NHS Supplier Registration Years",
                   fontsize=14)
    ax2.set_xlabel("All CC Registration Years",
                   fontsize=14)
    ax2.set_title('b.', loc='left',
                  **csfont, fontsize=titlesize+6, y=1.02)

    def ecdf(data):
        """ Compute ECDF """
        x = np.sort(data)
        n = x.size
        y = np.arange(1, n+1) / n
        return(x, y)

    x1, y1 = ecdf(cc_regdate)
    ax3.plot(x1, y1, label='All Charity Commission', color=color1, alpha=0.75, linewidth=1.5)
    x3, y3 = ecdf(cc_adv_date)
    ax3.plot(x3, y3, label='Advancement of Health', color=color3, alpha=0.75, linewidth=1.5)
    ax3.set_ylabel("Proportion of Data", fontsize=14)
    x2, y2 = ecdf(allsups_data_regdate)
    ax3.plot(x2, y2, label='NHS Suppliers', color=color2, alpha=0.75, linewidth=1.5)
    ax3.set_xlabel("Charity Registration Years", fontsize=14)
    ax3.set_title('c.', loc='left',
                  **csfont, fontsize=titlesize+7, y=1.02)
    ax3.legend(loc='upper left', edgecolor='k', facecolor='w', frameon=True, fontsize=10, framealpha=1)
    h = sns.distplot(allsups_data_regdate, ax=ax4, kde_kws={'gridsize': 500, 'color': color1},
                     label='NHS Suppliers',
                     hist=False
                    )
    h = sns.distplot(cc_adv_date, ax=ax4, kde_kws={'gridsize': 500, 'color': color2},
                     label='Advancement of Health',
                     hist=False
                    )
    ax4.set_ylabel("Normalized Frequency", fontsize=14)
    ax4.set_xlabel("Charity Registration Year", fontsize=14)
    ax4.set_title('d.',
                  **csfont, fontsize=titlesize+6, loc='left', y=1.02)
    h.legend(loc='upper left', edgecolor='k', facecolor='w', frameon=True, fontsize=10, framealpha=1)
    ax1.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax2.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax3.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    ax4.grid(linestyle='--', linewidth=0.5, alpha=0.35, color='#d3d3d3',zorder=0)
    legend = ax1.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend = ax3.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend = ax4.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    sns.despine()
    plt.tight_layout(pad=3.0)
    plt.savefig(os.path.join(figure_path, 'age_distributions.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'age_distributions.png'),
                bbox_inches='tight', dpi=500)
    plt.savefig(os.path.join(figure_path, 'age_distributions.pdf'),
                bbox_inches='tight')



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

    print('We have ' + str(len(gdf[gdf['amount_pc_cc']!='No Data'])) +
          ' trusts in our dataset')
    print('Of them, ' + str(len(gdf[(gdf['amount_pc_cc']!='No Data') &
                               (gdf['amount_pc_cc']<2.5)])) +
          ' procure < 2.5% from CCEW by value')
    print('Of them, ' + str(len(gdf[(gdf['count_pc_cc']!='No Data') &
                                    (gdf['count_pc_cc']<2.5)])) +
          ' procure < 2.5% from CCEW by count')
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


def plot_choropleths_trusts(support_path, shape_path, figure_path,
                           trust_pay_df, pay_df_cc):
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    titlesize = 15
    colors3 = ['#41558c', '#E89818', '#CF202A']
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
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ['white', colors3[0]])
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='pc_count_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.0, 0.5),
                                           frameon=True, fontsize=titlesize-4,
                                           title='Payment Volume'),
                 alpha=1, ax=ax1, markersize=markersize)
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
#    ax1.set_title('Total Volume of Payments', **csfont, fontsize=titlesize+2,y=1.1)
    ax1.set_title('a.', **csfont, fontsize=titlesize+8, loc='left', y=0.95)

    shapefile.plot(ax=ax2, color='white', edgecolor='black', linewidth=0.35);
    shapefile.plot(ax=ax2, color='None', edgecolor='black', alpha=0.2);
    markersize = gdf['pc_amount'] / 5 * 200
    k = 6
    quantiles = mc.Quantiles(gdf.pc_amount.dropna(), k=k)
    gdf['pc_amount_cat'] = quantiles.find_bin(gdf.pc_amount).astype('str')
    #gdf.loc[gdf.pc_amount.isnull(), 'pc_amount'] = 'No Data'
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ['white', colors3[1]])
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)][2:]
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='pc_amount_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.0, 0.5),
                                           frameon=True, fontsize=titlesize-4,
                                           title='Payment Amount'),
                 alpha=1, ax=ax2, markersize=markersize)
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
#    ax2.set_title('Cumulative Payment Amount', **csfont, fontsize=titlesize+2, y=1.1)
    ax2.set_title('b.', **csfont, fontsize=titlesize+8, loc='left', y=1.0)

    count_array = gdf[gdf['pc_count']!='No Data']['pc_count'].astype(float)
    ee = sns.distplot(count_array,
                      ax=ax3,
                      kde_kws={'color': colors3[1], 'alpha':1,
                                                    'label':'KDE', 'linewidth': 1},
                      hist_kws={'color': colors3[0], 'alpha': 1,
                                'edgecolor': 'k', 'label': 'Histogram'},
                      bins=20)
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=True, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")
    print('We have ' + str(len(gdf[gdf['pc_amount']!='No Data'])) + ' trusts in our dataset')
    print('Of them, ' + str(len(gdf[(gdf['pc_amount']!='No Data') & (gdf['pc_amount']<2.5)])) + ' procure < 2.5% from CCEW by value')
    print('Of them, ' + str(len(gdf[(gdf['pc_count']!='No Data') & (gdf['pc_count']<2.5)])) + ' procure < 2.5% from CCEW by count')
    count_array = gdf[gdf['pc_amount']!='No Data']['pc_amount'].astype(float)
    ff = sns.distplot(count_array,
                      ax=ax4,
                      kde_kws={'color': colors3[0], 'alpha':1,
                               'label':'KDE', 'linewidth': 1},
                      hist_kws={'color': colors3[1], 'alpha': 1,
                                'edgecolor': 'k', 'label': 'Histogram'},
                      bins=20)
    ff.set_xlim(0, None)
    ff.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=True, fontsize=10)
    ff.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ff.set_xlabel("")



    legend = ax1.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')


    legend = ax2.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')

    legend = ee.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')

    legend = ff.get_legend()
    legend_frame = legend.get_frame()
    legend_frame.set_linewidth(0.5)
    legend_frame.set_edgecolor('k')


    for legend_handle in ax1.get_legend().legend_handles:
        legend_handle.set_markeredgecolor('black')
        legend_handle.set_markeredgewidth(0.5)

    for legend_handle in ax2.get_legend().legend_handles:
        legend_handle.set_markeredgecolor('black')
        legend_handle.set_markeredgewidth(0.5)




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


def build_charity_df(pay_df, icnpo_df, cc_fin, data_path):
    cc_pay_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_pay_df.groupby(['CharityRegNo'])['CharityRegNo'].\
        count().reset_index(name="count")
    cc_val = cc_pay_df.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='CharityRegNo')
    #cc_merge = pd.merge(cc_merge,
    #                    cc_name[['regno', 'regdate', 'remdate']].drop_duplicates(subset=['regno']),
    #                    how='left',
    #                    left_on='CharityRegNo',
    #                    right_on='regno')
    cc_merge['CharityRegNo'] = pd.to_numeric(cc_merge['CharityRegNo'],
                                             errors='coerce')
    cc_merge['CharityRegNo'] = cc_merge['CharityRegNo'].astype(float)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, left_on=['CharityRegNo'], right_on=['regno'],
                        how='left', indicator=False)
    cc_sup = pd.merge(cc_merge, cc_fin, left_on=['CharityRegNo'], right_on=['regno'],
                      how='left', indicator=False)
    missing_regno = len(cc_sup[cc_sup['CharityRegNo'].isnull()])
    print('We are missing ' + str(missing_regno) + ' registration numbers')
    print("Can't do anything about that...\n" +
          "This seems to be where two charities have the " +
          "same normalised name, and neither has been " +
          " removed from the register")
    print('This leaves us with ' +
          str(len(cc_sup[cc_sup['CharityRegNo'].notnull()])) +
          ' charities with regnos.')
    missing_income = len(cc_sup[cc_sup['income'].isnull()])
    print('We are missing ' + str(missing_income) + ' incomes')
    print("Can't do anything about that...")
    missing_icnpo_df = cc_sup[(cc_sup['icnpo_desc'].isnull()) & (cc_merge['CharityRegNo'].notnull())]#[['verif_match', 'regno']]
    missing_icnpo = len(missing_icnpo_df)
    print('We are missing ' + str(missing_icnpo) + ' ICNPO numbers which have charity numbers')
    if missing_icnpo>0:
        print('The unmapped charities are in data\\support\\unmapped_icnpo.csv')
        missing_icnpo_df[['CharityRegNo']].to_csv(os.path.join(data_path, 'data_support', 'unmapped_icnpo.csv'))
    return cc_pay_df, cc_sup


def tabulate_charities(pay_df, icnpo_df, cc_fin, tablepath, tablename, metric):
    pay_df = pay_df[~pay_df['verif_match'].str.contains('FOUNDATION TRUST')]
    cc_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_df.groupby(['CharityRegNo'])['CharityRegNo'].\
                     count().reset_index(name="count")
    cc_val = cc_df.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='CharityRegNo')

#    cc_merge = pd.merge(cc_merge, cc_name, how='left',
#                        left_on='CharityRegNo', right_on='regno')
    cc_merge['CharityRegNo'] = pd.to_numeric(cc_merge['CharityRegNo'], errors='coerce')
    cc_merge = cc_merge[cc_merge['CharityRegNo'].notnull()]
    cc_merge['CharityRegNo'] = cc_merge['CharityRegNo'].astype(int)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, left_on=['CharityRegNo'],
                        right_on=['regno'],
                        how='left', indicator=False)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].fillna(9999)
    cc_merge = pd.merge(cc_merge, cc_fin,
                        left_on=['CharityRegNo'], right_on=['regno'],
                        how='left', indicator=False)
    cc_merge = cc_merge[cc_merge['ICNPO'].notnull()]
    cc_merge['ICNPO'] = cc_merge['ICNPO'].astype(int)
    cc_merge = cc_merge.drop(columns=[#'name', 'norm_name', 'subno',
                                      #'nameno',
                                      'icnpo_desc', 'icnpo_group',
                                      #'remdate',
                                      #'remcode'
                                      'regno_x', 'regno_y'
                                      ])
    #cc_merge = cc_merge.set_index('verif_match')
    sorted_values = cc_fin.sort_values(by='income', ascending=False)['regno'].reset_index()
    cc_merge['CC Rank'] = np.nan
    cc_merge = cc_merge.sort_values(by=metric, ascending=False)[0:10]
    for index, row in cc_merge.iterrows():
        pos = sorted_values[sorted_values['regno'] == row['CharityRegNo']].index[0]
        cc_merge.at[index, 'CC Rank'] = int(pos)
    #cc_merge['regdate'] = pd.to_datetime(cc_merge['regdate']).dt.date
    cc_merge['CC Rank'] = cc_merge['CC Rank'].astype(int)
    print(cc_merge.to_string(index=False))
    cc_merge.to_csv(os.path.join(tablepath, tablename), index=False)

def icnpo_groupings(pay_df, pay_df_ccg, pay_df_trust, pay_df_nhsengland,
                    icnpo_df, icnpo_lookup, table_path):
    """This should be modularized"""

    ## full df
    pay_df = pay_df[~pay_df['verif_match'].str.contains('FOUNDATION TRUST')]
    cc_df = pay_df[pay_df['match_type'].str.contains('Charity')]
    cc_count = cc_df.groupby(['CharityRegNo'])['CharityRegNo'].\
                     count().reset_index(name="count")
    cc_val = cc_df.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_merge = pd.merge(cc_val, cc_count, how='left', on='CharityRegNo')
    #cc_merge = pd.merge(cc_merge, cc_name, how='left',
    #                    left_on='CharityRegNo', right_on='regno')
    cc_merge['CharityRegNo'] = pd.to_numeric(cc_merge['CharityRegNo'], errors='coerce')
    cc_merge = cc_merge[cc_merge['CharityRegNo'].notnull()]
    cc_merge['CharityRegNo'] = cc_merge['CharityRegNo'].astype(int)
    cc_merge['amount'] = cc_merge['amount'].astype(int)
    cc_merge = pd.merge(cc_merge, icnpo_df, left_on = ['CharityRegNo'],
                        right_on=['regno'],
                        how='left', indicator=False)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].fillna(9999)
    cc_merge['ICNPO'] = cc_merge['ICNPO'].astype(int)
    #cc_merge = cc_merge.drop(columns=['norm_name'])
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
    pay_df_ccg = pay_df_ccg[~pay_df_ccg['verif_match'].str.contains('FOUNDATION TRUST')]
    cc_df_ccg = pay_df_ccg[pay_df_ccg['match_type'].str.contains('Charity')]
    cc_count_ccg = cc_df_ccg.groupby(['CharityRegNo'])['CharityRegNo'].\
                     count().reset_index(name="count_ccg")
    cc_val_ccg = cc_df_ccg.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_val_ccg = cc_val_ccg.rename({'amount': 'amount_ccg'}, axis=1)
    cc_merge_ccg = pd.merge(cc_val_ccg, cc_count_ccg, how='left', on='CharityRegNo')

    #cc_merge_ccg = pd.merge(cc_merge_ccg, cc_name, how='left',
    #                    left_on='CharityRegNo', right_on='regno')

    cc_merge_ccg['CharityRegNo'] = pd.to_numeric(cc_merge_ccg['CharityRegNo'], errors='coerce')
    cc_merge_ccg = cc_merge_ccg[cc_merge_ccg['CharityRegNo'].notnull()]
    cc_merge_ccg['CharityRegNo'] = cc_merge_ccg['CharityRegNo'].astype(int)
    cc_merge_ccg['amount_ccg'] = cc_merge_ccg['amount_ccg'].astype(int)
    cc_merge_ccg = pd.merge(cc_merge_ccg, icnpo_df, left_on=['CharityRegNo'],
                            right_on=['regno'],
                            how='left', indicator=False)
    cc_merge_ccg['ICNPO'] = cc_merge_ccg['ICNPO'].fillna(9999)
    cc_merge_ccg['ICNPO'] = cc_merge_ccg['ICNPO'].astype(int)
    #cc_merge_ccg = cc_merge_ccg.drop(columns=[#'name',
    #
    #                                          'norm_name',
    #                                          # 'subno',
    #                                          #'nameno', 'regno', 'verif_match'
    #                                          ])
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
    pay_df_trust = pay_df_trust[~pay_df_trust['verif_match'].str.contains('FOUNDATION TRUST')]
    cc_df_trust = pay_df_trust[pay_df_trust['match_type'].str.contains('Charity')]
    cc_count_trust = cc_df_trust.groupby(['CharityRegNo'])['CharityRegNo'].\
                     count().reset_index(name="count_trust")
    cc_val_trust = cc_df_trust.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_val_trust = cc_val_trust.rename({'amount': 'amount_trust'}, axis=1)
    cc_merge_trust = pd.merge(cc_val_trust, cc_count_trust, how='left', on='CharityRegNo')
    #cc_merge_trust = pd.merge(cc_merge_trust, cc_name, how='left',
    #                    left_on='verif_match', right_on='norm_name')
    cc_merge_trust['CharityRegNo'] = pd.to_numeric(cc_merge_trust['CharityRegNo'], errors='coerce')
    cc_merge_trust = cc_merge_trust[cc_merge_trust['CharityRegNo'].notnull()]
    cc_merge_trust['CharityRegNo'] = cc_merge_trust['CharityRegNo'].astype(int)
    cc_merge_trust['amount_trust'] = cc_merge_trust['amount_trust'].astype(int)
    cc_merge_trust = pd.merge(cc_merge_trust, icnpo_df, left_on=['CharityRegNo'],
                              right_on=['regno'],
                              how = 'left', indicator=False)
    cc_merge_trust['ICNPO'] = cc_merge_trust['ICNPO'].fillna(9999)
    cc_merge_trust['ICNPO'] = cc_merge_trust['ICNPO'].astype(int)
#    cc_merge_trust = cc_merge_trust.drop(columns=[#'name',
#                                                  'norm_name',
#                                                  #'subno', 'nameno', 'regno', 'verif_match'
#        ])
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
    pay_df_trust = pay_df_trust[~pay_df_trust['verif_match'].str.contains('FOUNDATION TRUST')]
    cc_df_nhsengland = pay_df_nhsengland[pay_df_nhsengland['match_type'].str.contains('Charity')]
    cc_count_nhsengland = cc_df_nhsengland.groupby(['CharityRegNo'])['CharityRegNo'].\
                     count().reset_index(name="count_eng")
    cc_val_nhsengland = cc_df_nhsengland.groupby(['CharityRegNo'])['amount'].sum().reset_index()
    cc_val_nhsengland = cc_val_nhsengland.rename({'amount': 'amount_eng'}, axis=1)
    cc_merge_nhsengland = pd.merge(cc_val_nhsengland, cc_count_nhsengland,
                                   how='left', on='CharityRegNo')
    #cc_merge_nhsengland = pd.merge(cc_merge_nhsengland, cc_name, how='left',
    #                               left_on='CharityRegNo', right_on='regno')
    cc_merge_nhsengland['regno'] = pd.to_numeric(cc_merge_nhsengland['CharityRegNo'], errors='coerce')
    cc_merge_nhsengland = cc_merge_nhsengland[cc_merge_nhsengland['CharityRegNo'].notnull()]
    cc_merge_nhsengland['CharityRegNo'] = cc_merge_nhsengland['CharityRegNo'].astype(int)
    cc_merge_nhsengland['amount_eng'] = cc_merge_nhsengland['amount_eng'].astype(int)
    cc_merge_nhsengland = pd.merge(cc_merge_nhsengland, icnpo_df, on=['regno'],
                                   how='left', indicator=False)
    cc_merge_nhsengland['ICNPO'] = cc_merge_nhsengland['ICNPO'].fillna(9999)
    cc_merge_nhsengland['ICNPO'] = cc_merge_nhsengland['ICNPO'].astype(int)
#    cc_merge_nhsengland = cc_merge_nhsengland.drop(columns=['name', 'norm_name', 'subno',
#                                                            'nameno', 'regno', 'verif_match'])
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
    icnpo_out = icnpo_out.drop(labels = 'icnpo', axis = 1)
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc_ccg, how='left', on = 'ICNPO')
    icnpo_out = icnpo_out.rename({'ICNPO_y': 'ICNPO'}, axis=1)
    icnpo_out = icnpo_out.drop(labels = 'ICNPO_x', axis = 1)
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
    ex_char = pd.read_csv(os.path.join(cc_path, 'extract_charity.csv'),
                          on_bad_lines='skip', low_memory=False)
    print('The percent of charities without an address: ',
          len(ex_char[ex_char['postcode'].notnull()])/len(ex_char))
    cc_name = pd.read_csv(os.path.join(cc_path, 'extract_name.csv'),
                          on_bad_lines='skip')
    print('The number of unique regnos in our database: ',
          len(cc_name['regno'].unique()))
    cc_regdate = pd.read_csv(os.path.join(cc_path,
                                          'extract_registration.csv'),
                             parse_dates=['regdate', 'remdate'],
                             on_bad_lines='skip')
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
                           on_bad_lines='skip')
    class_ref = pd.read_csv(os.path.join(cc_path, 'extract_class_ref.csv'),
                            on_bad_lines='skip')
    cc_class = pd.merge(cc_class, class_ref, how='left',
                        left_on='class', right_on='classno')
    cc_class = cc_class[cc_class['class'].notnull()]
    cc_class['class'] = cc_class['class'].astype(int)
    cc_class['regno'] = cc_class['regno'].astype(int)
    cc_class = cc_class[['regno', 'class', 'classtext']]
    return cc_class


def load_ccfin(cc_path):
    cc_fin = pd.read_csv(os.path.join(cc_path, 'extract_financial.csv'),
                         on_bad_lines='skip',
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


def make_ET(merged_char, merged_notchar, data_type):
    ET_counts_notchar = merged_notchar[merged_notchar['data_type']==data_type]['expensetype'].value_counts()
    ET_counts_notchar.index = ET_counts_notchar.index.str.title()
    ET_counts_notchar = ET_counts_notchar/ET_counts_notchar.sum()
    ET_counts_notchar = ET_counts_notchar.reset_index()
    ET_counts_notchar = ET_counts_notchar.rename({'count': 'count_notchar_' + data_type}, axis=1)
    ET_counts_char = merged_char['expensetype'].value_counts()
    ET_counts_char.index = ET_counts_char.index.str.title()
    ET_counts_char = ET_counts_char/ET_counts_char.sum()
    ET_counts_char = ET_counts_char.reset_index()
    ET_counts_char = ET_counts_char.rename({'count': 'count_char_' + data_type}, axis=1)
    ET_amount_notchar = merged_notchar.groupby(['expensetype'])['amount'].sum()
    ET_amount_notchar.index = ET_amount_notchar.index.str.title()
    ET_amount_notchar = ET_amount_notchar/ET_amount_notchar.sum()
    ET_amount_notchar = ET_amount_notchar.reset_index()
    ET_amount_notchar = ET_amount_notchar.rename({'amount': 'amount_notchar_' + data_type}, axis=1)
    ET_amount_char = merged_char.groupby(['expensetype'])['amount'].sum()
    ET_amount_char.index = ET_amount_char.index.str.title()
    ET_amount_char = ET_amount_char/ET_amount_char.sum()
    ET_amount_char = ET_amount_char.reset_index()
    ET_amount_char = ET_amount_char.rename({'amount': 'amount_char_' + data_type}, axis=1)
    ET = pd.merge(ET_counts_notchar, ET_counts_char,
                  on='expensetype', how='inner')
    ET = pd.merge(ET, ET_amount_notchar,
                  on='expensetype', how='inner')
    ET = pd.merge(ET, ET_amount_char,
                  on='expensetype', how='inner')
    return ET

def make_expense_area(nhsengland_pay_df, trust_pay_df, ccg_pay_df, figure_path):
    merged_df = pd.concat([nhsengland_pay_df, trust_pay_df, ccg_pay_df])
    merged_df['expensetype'] = merged_df['expensetype'].str.title()
    merged_df['expensetype'] = merged_df['expensetype'].str.strip()
    merged_df = merged_df[merged_df['expensetype'].notnull()]
    merged_df = merged_df[merged_df['expensetype']!='']
    merged_char = merged_df[merged_df['match_type'].str.contains('Charity', regex=False)]
    merged_notchar = merged_df[~merged_df['match_type'].str.contains('Charity', regex=False)]

    ET_CCGs = make_ET(merged_char, merged_notchar, 'CCGs')
    ET_NHSE = make_ET(merged_char, merged_notchar, 'NHS_Eng')
    ET_Trusts = make_ET(merged_char, merged_notchar, 'Trusts')

    f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 11.25))
    colors = ['#001c54', '#E89818']
    for df in [ET_Trusts, ET_CCGs, ET_NHSE]:
        df['expensetype'] = df['expensetype'].str.replace('Improving Access To Psychological Therapies',
                                                          'Improving Access to\nPsychological Therapies')
        df['expensetype'] = df['expensetype'].str.replace('Commissioning - Non Acute',
                                                          'Commissioning\n(Non Acute)')
        df['expensetype'] = df['expensetype'].str.replace('Primary Care', 'Primary\nCare')
        df['expensetype'] = df['expensetype'].str.replace('Specialised Commissioning',
                                                          'Specialised\nCommissioning')
        df['expensetype'] = df['expensetype'].str.replace('Primary\nCare & Secondary Dental',
                                                          'Primary Care &\nSecondary Dental')
        df['expensetype'] = df['expensetype'].str.replace('Nhs England Central Programme Costs',
                                                          'NHS England Central\nProgramme Costs')
        df['expensetype'] = df['expensetype'].str.replace('Community Services',
                                                          'Community\nServices')
        df['expensetype'] = df['expensetype'].str.replace('Balance Sheet',
                                                          'Balance\nSheet')
        df['expensetype'] = df['expensetype'].str.replace('Primary Care',
                                                          'Primary\nCare')
        df['expensetype'] = df['expensetype'].str.replace('Public Health',
                                                          'Public\nHealth')
        df['expensetype'] = df['expensetype'].str.replace('Ambulance Services',
                                                          'Ambulance\nServices')
        df['expensetype'] = df['expensetype'].str.replace('Planned Care',
                                                          'Planned\nCare')
        df['expensetype'] = df['expensetype'].str.replace('Social Care',
                                                          'Social\nCare')
        df['expensetype'] = df['expensetype'].str.replace('Out Of Hours',
                                                          'Out Of\nHours')
        df['expensetype'] = df['expensetype'].str.replace('Health And Justice',
                                                          'Health And\nJustice')
        df['expensetype'] = df['expensetype'].str.replace('Other (Including Central Programme)',
                                                          'Other (Inc.\nCentral Programme)')
        df['expensetype'] = df['expensetype'].str.replace('Nhs England Running Costs',
                                                          'NHS England\nRunning Costs')
        df['expensetype'] = df['expensetype'].str.replace('Health & Justice',
                                                          'Health &\nJustice')
        df['expensetype'] = df['expensetype'].str.replace('Primary\nCare &\nSecondary Dental',
                                                          'Primary Care &\nSecondary Dental')
        df['expensetype'] = df['expensetype'].str.replace('End Of Life',
                                                          'End Of\nLife')
        df['expensetype'] = df['expensetype'].str.replace('Nrp Management & Admin',
                                                          'NRP Management\n& Admin',
                                                          )
        df['expensetype'] = df['expensetype'].str.replace('Fetal Medicine Serv Agreement',
                                                          'Fetal Medicine\nServ Agreement')
        df['expensetype'] = df['expensetype'].str.replace('Ncfp Contract',
                                                          'NCFP Contract')
        df['expensetype'] = df['expensetype'].str.replace('Iapt',
                                                          'IAPT')
        df['expensetype'] = df['expensetype'].str.replace('Nrp Management & Admin',
                                                          'NRP Management\n& Admin')
        df['expensetype'] = df['expensetype'].str.replace('Chc Adult Fully Funded',
                                                          'CHC Adult\nFully Funded')
        df['expensetype'] = df['expensetype'].str.replace('Mental Health Contracts',
                                                          'Mental Health\nContracts')
        df['expensetype'] = df['expensetype'].str.replace('Palliative Care',
                                                          'Palliative\nCare')
        df['expensetype'] = df['expensetype'].str.replace('Mental Health Services - Other',
                                                          'Mental Health\nServices - Other')
        df['expensetype'] = df['expensetype'].str.replace('Mental Health Services - Adults',
                                                          'Mental Health\nServices - Adults')
        df['expensetype'] = df['expensetype'].str.replace('Mental Health Contracts',
                                                          'Mental Health\nContracts')
        df['expensetype'] = df['expensetype'].str.replace('Acute Commissioning',
                                                          'Acute\nCommissioning')
        df['expensetype'] = df['expensetype'].str.replace('Prc Delegated Co-Commissioning',
                                                          'PRC Delegated\nCo-Commissioning')
        df['expensetype'] = df['expensetype'].str.replace('Local Enhanced Services',
                                                          'Local Enhanced\nServices')
        df['expensetype'] = df['expensetype'].str.replace('Secondary And Community Dental Care',
                                                          'Secondary and\nCommunity Dental Care')
    print(ET_Trusts)
    ET_Trusts.sort_values(by='amount_notchar_Trusts',
                          ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                      y=["count_notchar_Trusts",
                                                                         "amount_notchar_Trusts"],
                                                                      ax=ax1,
                                                                      legend=False,
                                                                      edgecolor='k',
                                                                      color = colors,
                                                                      width=0.75)
    ET_CCGs.sort_values(by='amount_notchar_CCGs',
                        ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                    y=["count_notchar_CCGs",
                                                                       "amount_notchar_CCGs"],
                                                                    ax=ax2,
                                                                    legend=False,
                                                                    edgecolor='k',
                                                                    color = colors,
                                                                    width=0.75)
    ET_NHSE.sort_values(by='amount_notchar_NHS_Eng',
                        ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                    y=["count_notchar_NHS_Eng",
                                                                       "amount_notchar_NHS_Eng"],
                                                                    ax=ax3,
                                                                    edgecolor='k',
                                                                    color=colors,
                                                                    legend=False,
                                                                    width=0.75)
    ET_Trusts.sort_values(by='amount_char_Trusts',
                          ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                      y=["count_char_Trusts",
                                                                         "amount_char_Trusts"],
                                                                      ax=ax4,
                                                                      legend=False,
                                                                      edgecolor='k',
                                                                      color = colors,
                                                                      width=0.75)
    ET_CCGs.sort_values(by='amount_char_CCGs',
                        ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                    y=["count_char_CCGs",
                                                                       "amount_char_CCGs"],
                                                                    ax=ax5,
                                                                    legend=False,
                                                                    edgecolor='k',
                                                                    color = colors,
                                                                    width=0.75)
    ET_NHSE.sort_values(by='amount_char_NHS_Eng',
                        ascending=False)[0:12].iloc[::-1].plot.barh(x='expensetype',
                                                                    y=["count_char_NHS_Eng",
                                                                       "amount_char_NHS_Eng"],
                                                                    ax=ax6,
                                                                    edgecolor='k',
                                                                    color = colors,
                                                                    width=0.75)
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    ax3.set_ylabel('')
    ax4.set_ylabel('')
    ax5.set_ylabel('')
    ax6.set_ylabel('')
    ax1.set_title('a.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    ax2.set_title('b.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    ax3.set_title('c.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    ax4.set_title('d.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    ax5.set_title('e.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    ax6.set_title('f.', **csfont, fontsize=14, loc='left', y=1.0, x=-0.1)
    from matplotlib.patches import Patch
    legend_elements1 = [Patch(facecolor=colors[0], edgecolor=(0,0,0,1),
                              label=r'Count'),
                        Patch(facecolor=colors[1], edgecolor=(0,0,0,1),
                              label=r'Amount (£)')]
    leg = ax6.legend(handles=legend_elements1, loc='lower right', frameon=True,
                     fontsize=10, framealpha=1, facecolor='w',
                     edgecolor=(0, 0, 0, 1))
    leg.get_frame().set_edgecolor((0, 0, 0, 1))
    leg.get_frame().set_linewidth(0.75)
    def percentage_formatter(x, pos):
        return f"{x*100:.0f}%"
    ax1.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax2.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax3.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax4.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax5.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax6.xaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax4.set_xlabel('Expense Area\n(Trusts)', fontsize=11)
    ax5.set_xlabel('Expense Area\n(CCGs)', fontsize=11)
    ax6.set_xlabel('Expense Area\n(NHS England)', fontsize=11)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'expense_area.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'expense_area.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'expense_area.png'),
                bbox_inches='tight')


def make_sic(df, ch, label):
    df = df[df['CompanyNumber'].notnull()]
    df_ch = ch[ch[' CompanyNumber'].isin(df['CompanyNumber'])]
    df_ch_long = pd.DataFrame(columns=['CompanyNumber', 'SIC'])
    counter = 0
    for index, row in df_ch.iterrows():
        for SIC in range(1, 5):
            sic_string = 'SICCode.SicText_' + str(int(SIC))
            if type(row[sic_string]) is str:
                df_ch_long.at[counter, 'CompanyNumber'] = row[' CompanyNumber']
                df_ch_long.loc[counter, 'SIC'] = row[sic_string]
                counter += 1
    df_cn_count = (df['CompanyNumber'].value_counts()/len(df['amount'])*100).round(3).reset_index()
    df_cn_amount = (df.groupby(['CompanyNumber'])['amount'].sum()/df['amount'].sum()*100).round(3).reset_index()
    df_cn = pd.merge(df_cn_count, df_cn_amount, how='left', on='CompanyNumber')
    df_merge = pd.merge(df_ch_long, df_cn, how='left', on='CompanyNumber')
    df_merge_amount = df_merge.groupby(['SIC'])['count'].sum().reset_index()
    df_merge_count = df_merge.groupby(['SIC'])['amount'].sum().reset_index()
    df_merge = pd.merge(df_merge_amount, df_merge_count, how='left', on='SIC')
    return df_merge.rename({'count': 'count_' + label,
                            'amount': 'amount_' + label},
                           axis=1)


def make_sic_outer(merged_df, ch):
    char_all = make_sic(merged_df[merged_df['match_type'].str.contains('Charit')], ch, 'char_all')
    char_nhse = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')) &
                                   (merged_df['data_type']=='NHS_Eng')], ch, 'char_nhse')
    char_trusts = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')) &
                                     (merged_df['data_type']=='Trusts')], ch, 'char_trusts')
    char_ccgs = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')) &
                                   (merged_df['data_type']=='CCGs')], ch, 'char_ccgs')


    notchar_all = make_sic(merged_df[merged_df['match_type'].str.contains('Charit')==False], ch, 'notchar_all')
    notchar_nhse = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')==False) &
                                      (merged_df['data_type']=='NHS_Eng')], ch, 'notchar_nhse')
    notchar_trusts = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')==False) &
                                        (merged_df['data_type']=='Trusts')], ch, 'notchar_trusts')
    notchar_ccgs = make_sic(merged_df[(merged_df['match_type'].str.contains('Charit')==False) &
                                      (merged_df['data_type']=='CCGs')], ch, 'notchar_ccgs')

    char_merge = pd.merge(char_all, char_nhse, how='left', on='SIC')
    char_merge = pd.merge(char_merge, char_trusts, how='left', on='SIC')
    char_merge = pd.merge(char_merge, char_ccgs, how='left', on='SIC')
    char_merge = char_merge.sort_values(by='count_char_all', ascending=False)
    char_merge.to_csv(os.path.join(os.getcwd(), '..', '..', 'papers', 'tables', 'sic_codes_charities.csv'),
                      index=False)
    print('Data on payments to Charities:')
    print(char_merge[0:20])
    print('*'*20)
    notchar_merge = pd.merge(notchar_all, notchar_nhse, how='left', on='SIC')
    notchar_merge = pd.merge(notchar_merge, notchar_trusts, how='left', on='SIC')
    notchar_merge = pd.merge(notchar_merge, notchar_ccgs, how='left', on='SIC')
    notchar_merge = notchar_merge.sort_values(by='count_notchar_all', ascending=False)
    notchar_merge.to_csv(os.path.join(os.getcwd(), '..', '..', 'papers', 'tables', 'sic_codes_noncharities.csv'),
                         index=False)
    print('Data on payments not to Charities:')
    print(notchar_merge[0:20])


def convert_to_numeric(x):
    """
    Convert x values to numeric.

    Parameters:
        x (list): List of x values (datetime objects or numpy float64).

    Returns:
        list: List of numeric values.
    """
    if isinstance(x[0], (pd.Timestamp, np.datetime64)):
        return [t.timestamp() for t in x]
    elif isinstance(x[0], np.float64):
        return x
    else:
        raise ValueError("Unsupported data type for x")

def lowess_with_confidence_bounds(x, y, eval_x, N=500, conf_interval=0.99, lowess_kw=None):
    """
    Perform Lowess regression and determine a confidence interval by bootstrap resampling

    Parameters:
        x (list): List of x-values.
        y (list): List of corresponding y-values.
        eval_x (list): List of x-values at which to evaluate the smoothing.
        N (int): Number of bootstrap resampling iterations.
        conf_interval (float): Confidence interval level.
        lowess_kw (dict): Keyword arguments for the statsmodels lowess function.

    Returns:
        tuple: A tuple containing smoothed values, lower bound, and upper bound of the confidence interval.
    """
    if lowess_kw is None:
        lowess_kw = {}

    # Convert x values to numeric
    x_numeric = convert_to_numeric(x)
    eval_x_numeric = convert_to_numeric(eval_x)

    # Lowess smoothing on the original data
    smoothed = sm.nonparametric.lowess(endog=y, exog=x_numeric, xvals=eval_x_numeric, **lowess_kw)

    # Perform bootstrap resamplings and evaluate the smoothing
    smoothed_values = np.empty((N, len(eval_x)))
    for i in range(N):
        sample_indices = np.random.choice(len(x), size=len(x), replace=True)
        sampled_x = [x_numeric[idx] for idx in sample_indices]
        sampled_y = [y[idx] for idx in sample_indices]

        smoothed_values[i] = sm.nonparametric.lowess(endog=sampled_y, exog=sampled_x, xvals=eval_x_numeric, **lowess_kw)
    # Get the confidence interval
    sorted_values = np.sort(smoothed_values, axis=0)
    bound = int(N * (1 - conf_interval) / 2)
    bottom = sorted_values[bound - 1]
    top = sorted_values[-bound]
    return smoothed[:], bottom, top

def ecdf(data):
    """ Compute ECDF """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x, y)


def plot_coverage(pay_df_cc_ccg, pay_df_cc_trust, pay_df_cc_nhsengland, rolling_df_45, figure_path):
    # Number of entities seen and Median number of contracts
    pay_df_cc_ccg = pay_df_cc_ccg[(pay_df_cc_ccg['date']>='2013-01-01') &
                                  (pay_df_cc_ccg['date']<='2019-09-30')]
    pay_df_cc_ccg = pay_df_cc_ccg.sort_values(by='date')
    date_vec = pay_df_cc_ccg['date'].unique()
    df_coverage_ccg = pd.DataFrame(columns=['number_suppliers'])
    my_set = set()
    for date in date_vec:
        temp = pay_df_cc_ccg[pay_df_cc_ccg['date']==date]
        my_set = my_set.union(set(list(temp['supplier'].unique())))
        df_coverage_ccg.at[date, 'number_suppliers'] = len(my_set)

    pay_df_cc_trust.loc[:, 'date'] = pd.to_datetime(pay_df_cc_trust['date']).apply(lambda x: x.date())
    pay_df_cc_trust = pay_df_cc_trust[(pay_df_cc_trust['date']>=datetime.date(year=2013,month=1,day=1)) &
                                      (pay_df_cc_trust['date']<=datetime.date(year=2019,month=9,day=30))]
    pay_df_cc_trust = pay_df_cc_trust.sort_values(by='date')
    date_vec = pay_df_cc_trust['date'].unique()
    df_coverage_trust = pd.DataFrame(columns=['number_suppliers'])
    my_set = set()
    for date in date_vec:
        temp = pay_df_cc_trust[pay_df_cc_trust['date']==date]
        my_set = my_set.union(set(list(temp['supplier'].unique())))
        df_coverage_trust.at[date, 'number_suppliers'] = len(my_set)
    pay_df_cc_nhsengland = pay_df_cc_nhsengland[(pay_df_cc_nhsengland['date']>='2013-01-01') &
                                                (pay_df_cc_nhsengland['date']<='2019-09-30')]
    pay_df_cc_nhsengland = pay_df_cc_nhsengland.sort_values(by='date')
    date_vec = pay_df_cc_nhsengland['date'].unique()
    df_coverage_nhsengland = pd.DataFrame(columns=['number_suppliers'])
    my_set = set()
    for date in date_vec:
        temp = pay_df_cc_nhsengland[pay_df_cc_nhsengland['date']==date]
        my_set = my_set.union(set(list(temp['supplier'].unique())))
        df_coverage_nhsengland.at[date, 'number_suppliers'] = len(my_set)
    df_coverage_ccg.index = pd.to_datetime(df_coverage_ccg.index, format="%d-%m-%Y")#.dt.date
    df_coverage_trust.index = pd.to_datetime(df_coverage_trust.index, format="%d-%m-%Y")#.dt.date
    df_coverage_nhsengland.index = pd.to_datetime(df_coverage_nhsengland.index, format="%d-%m-%Y")#.dt.date
    df_coverage_ccg['number_suppliers'] = df_coverage_ccg['number_suppliers']/df_coverage_ccg['number_suppliers'][-1]
    df_coverage_trust['number_suppliers'] = df_coverage_trust['number_suppliers']/df_coverage_trust['number_suppliers'][-1]
    df_coverage_nhsengland['number_suppliers'] = df_coverage_nhsengland['number_suppliers']/df_coverage_nhsengland['number_suppliers'][-1]#*100
    csfont = {'fontname': 'Helvetica'}
    colors = ['#41558c', '#E89818', '#CF202A']
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    fig = plt.figure(figsize=(14, 7))
    gs = gridspec.GridSpec(3,2)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[2, 1])
    df_coverage_ccg.index = pd.to_datetime(df_coverage_ccg.index, format="%d-%m-%Y")#.dt.date
    df_coverage_trust.index = pd.to_datetime(df_coverage_trust.index, format="%d-%m-%Y")#.dt.date
    df_coverage_nhsengland.index = pd.to_datetime(df_coverage_nhsengland.index, format="%d-%m-%Y")#.dt.date
    df_coverage_ccg['number_suppliers'] = df_coverage_ccg['number_suppliers']/df_coverage_ccg['number_suppliers'][-1]
    df_coverage_trust['number_suppliers'] = df_coverage_trust['number_suppliers']/df_coverage_trust['number_suppliers'][-1]
    df_coverage_nhsengland['number_suppliers'] = df_coverage_nhsengland['number_suppliers']/df_coverage_nhsengland['number_suppliers'][-1]#*100
    ax1.step(df_coverage_ccg.index, df_coverage_ccg['number_suppliers'], color=color1)
    ax1.step(df_coverage_trust.index, df_coverage_trust['number_suppliers'], color=color2)
    ax1.step(df_coverage_nhsengland.index, df_coverage_nhsengland['number_suppliers'], color3)
    ax2.plot(rolling_df_45.index, rolling_df_45['CCG_Median'],
             color=color1)
    ax3.plot(rolling_df_45.index, rolling_df_45['Trust_Median'],
             color=color2)
    ax4.plot(rolling_df_45.index, rolling_df_45['NHSEngland_Median'],
             color=color3)
    ax1.set_title('a.', loc='left', size=21, y=1.02)
    ax2.set_title('b.', loc='left', size=21, y=1.02)
    ax3.set_title('c.', loc='left', size=21, y=1.02)
    ax4.set_title('d.', loc='left', size=21, y=1.02)
    ax1.set_ylabel('Fraction Observed', **csfont, size=16)
    ax2.set_ylabel('Median Value\n   (CCGs)   ', **csfont, size=16)
    ax3.set_ylabel('Median Value\n (Trusts)  ', **csfont, size=16)
    ax4.set_ylabel('Median Value\n(NHS England)', **csfont, size=16)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax3.tick_params(axis='both', which='major', labelsize=14)
    ax4.tick_params(axis='both', which='major', labelsize=14)
    def currency_formatter(x, pos):
        return f'£{x/1000:.0f}k'
    ax2.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    ax3.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    ax4.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    max_ticks = 3
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
    ax3.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
    ax4.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks+1, integer=True))
    ax1.set_ylim(-0.01, 1.01)
    legend_elements = [(Line2D([0], [0], markersize=0,
                               color=color1, label=r'CCGs', linestyle='-')),
                        (Line2D([0], [0], markersize=0,
                                color=color2, label=r'Trusts', linestyle='-')),
                        (Line2D([0], [0], markersize=0,
                                color=color3, label='NHS England', linestyle='-'))
                      ]
    leg = ax1.legend(handles=legend_elements, loc='upper left', frameon=True,
                     fontsize=14, framealpha=1, facecolor='w',
                     edgecolor='k', handletextpad=0.25)
    leg.get_frame().set_linewidth(1)
    plt.tight_layout()
    sns.despine()
    plt.savefig(os.path.join(figure_path, 'entry_and_value.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'entry_and_value.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'entry_and_value.png'),
                bbox_inches='tight', dpi=800)


def load_token(path):
    """
    Simple function to load a hidden API token from
    disk: It should live in the `tokens` sub-directory
    :param path:    A filepath to a text file which contains
                    an API on the first line of the file only.
    :return:        The API key read in from the file
    """
    try:
        print('API key read in successfully')
        with open(path, 'r') as file:
            return str(file.readline()).strip()
    except FileNotFoundError:
        print('API Token was not found')

def make_companycategory(recomb, analysis_type):
    recomb = recomb[recomb['CompanyNumber'].notnull()]
    recomb_uniq_all = recomb.drop_duplicates(subset=['CompanyNumber'])
    recomb_uniq_all = recomb_uniq_all['CompanyCategory'].value_counts()
    recomb_uniq_all = pd.DataFrame(recomb_uniq_all)
    recomb_uniq_all = recomb_uniq_all.reset_index()
    recomb_uniq_all['Uniq. Freq. (%)'] = recomb_uniq_all['count']/\
                                         recomb_uniq_all['count'].sum()*100
    recomb_count_all = recomb['CompanyCategory'].value_counts()
    recomb_count_all = pd.DataFrame(recomb_count_all)
    recomb_count_all = recomb_count_all.reset_index()
    print(recomb_count_all)
    recomb_count_all['Pay Count (%)'] = recomb_count_all['count']/\
                                        recomb_count_all['count'].sum()*100
    recomb_amount_all = recomb.groupby(['CompanyCategory'])['amount'].sum()
    recomb_amount_all = pd.DataFrame(recomb_amount_all)
    recomb_amount_all = recomb_amount_all.reset_index()
    recomb_amount_all = recomb_amount_all.rename({'amount': 'Pay Amount'},
                                                 axis=1)
    recomb_amount_all['Pay Amount (%)'] = recomb_amount_all['Pay Amount']/\
                                          recomb_amount_all['Pay Amount'].sum()*100
    holder = pd.merge(recomb_uniq_all,
                      recomb_count_all,
                      how='left',
                      left_on='CompanyCategory',
                      right_on='CompanyCategory')

    holder = pd.merge(holder,
                      recomb_amount_all,
                      how='left',
                      left_on='CompanyCategory',
                      right_on='CompanyCategory')

    holder.to_csv(os.path.join(os.getcwd(),
                               '..',
                               '..',
                               'papers',
                               'tables',
                               'CompanyCategory_' + analysis_type + '.csv'),
                  index=False)

def load_token(path):
    """
    Simple function to load a hidden API token from
    disk: It should live in the `tokens` sub-directory
    :param path:    A filepath to a text file which contains
                    an API on the first line of the file only.
    :return:        The API key read in from the file
    """
    try:
        print('API key read in successfully')
        with open(path, 'r') as file:
            return str(file.readline()).strip()
    except FileNotFoundError:
        print('API Token was not found')


def make_ch_dict(comb_ch):
    companynumber_set = set(comb_ch[comb_ch['CompanyCategory'].isnull()]['CompanyNumber'].unique())
    api_key_path = os.path.join(os.getcwd(),
                                '..',
                                '..',
                                'tokens',
                                'ch_apikey')

    APIKey = load_token(api_key_path)


    import requests
    import json
    mydict = {}
    for Company in companynumber_set:
        CH_url = 'https://api.companieshouse.gov.uk/company/'
        query = requests.get(CH_url + str(Company),
                             auth=requests.auth.HTTPBasicAuth(APIKey, '')
                            )
        if query.status_code == 200:
            query_json = json.loads(query.text)
            if query_json['type'] == 'ltd':
                mydict[Company] = 'Private Limited Company'
            elif query_json['type'] == 'private-limited-guarant-nsc':
                mydict[Company] = 'PRI/LTD BY GUAR/NSC (Private, limited by guarantee, no share capital)'
            elif query_json['type'] == 'llp':
                mydict[Company] = 'Limited Liability Partnership'
            elif query_json['type'] == 'registered-society-non-jurisdictional':
                mydict[Company] = 'Registered Society'
            elif query_json['type'] == 'industrial-and-provident-society':
                mydict[Company] = 'Industrial and Provident Society'
            elif query_json['type'] == 'private-limited-guarant-nsc-limited-exemption':
                mydict[Company] = "PRI/LBG/NSC (Private, Limited by guarantee, no share capital, use of 'Limited' exemption)"
            elif query_json['type'] == 'converted-or-closed':
                pass
            else:
                mydict[Company] = query_json['type']
        elif (query.status_code == 404) or\
        (query.status_code == 500):
            finished_query = True
        elif (int(query.headers['X-Ratelimit-Remain']) == 0) or \
        (query.status_code == 429):
            time.sleep(30)
    return mydict


def CIC_wrangling(stack1, stack2, CIC_payments):
    recomb = pd.concat([stack1, stack2], ignore_index=True)
    CIC_2013 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2013-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2013-12-31'))]['amount'].sum()
    all_2013 = recomb[(recomb['date'] >= pd.Timestamp('2013-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2013-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2013: ', CIC_2013/all_2013*100)

    CIC_2014 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2014-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2014-12-31'))]['amount'].sum()
    all_2014 = recomb[(recomb['date'] >= pd.Timestamp('2014-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2014-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2014: ', CIC_2014/all_2014*100)

    CIC_2015 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2015-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2015-12-31'))]['amount'].sum()
    all_2015 = recomb[(recomb['date'] >= pd.Timestamp('2015-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2015-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2015: ', CIC_2015/all_2015*100)

    CIC_2016 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2016-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2016-12-31'))]['amount'].sum()
    all_2016 = recomb[(recomb['date'] >= pd.Timestamp('2016-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2016-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2016: ', CIC_2016/all_2016*100)

    CIC_2017 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2017-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2017-12-31'))]['amount'].sum()
    all_2017 = recomb[(recomb['date'] >= pd.Timestamp('2017-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2017-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2017: ', CIC_2017/all_2017*100)

    CIC_2018 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2018-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2018-12-31'))]['amount'].sum()
    all_2018 = recomb[(recomb['date'] >= pd.Timestamp('2018-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2018-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2018: ', CIC_2018/all_2018*100)

    CIC_2019 = CIC_payments[(CIC_payments['date'] >= pd.Timestamp('2019-01-01')) &
                            (CIC_payments['date'] <= pd.Timestamp('2019-12-31'))]['amount'].sum()
    all_2019 = recomb[(recomb['date'] >= pd.Timestamp('2019-01-01')) &
                      (recomb['date'] <= pd.Timestamp('2019-12-31'))]['amount'].sum()
    print('Percent of all payments by value which go to CICs in 2019: ', CIC_2019/all_2019*100)
