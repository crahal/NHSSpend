import pandas as pd
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
mpl.font_manager._rebuild()
from reconciliation import normalizer

np.warnings.filterwarnings('ignore')
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25

#github_url = 'https://github.com/google/roboto/blob/master/src/hinted/Helvetica.ttf'
#url = github_url + '?raw=true'  # You want the actual file, not some html
#response = urlopen(url)
#f = NamedTemporaryFile(delete=False, suffix='.ttf')
#f.write(response.read())
#f.close()
#
#mpl.rc('font', family='sans-serif')
#mpl.rc('font', serif=f.name)
#mpl.rc('text', usetex='false')


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


def plot_temporal(ts_plot):
    fig = plt.figure(figsize=(12, 10))
    ax1 = plt.subplot2grid((4, 2), (0, 0), colspan=1)
    ax2 = plt.subplot2grid((4, 2), (1, 0), colspan=1)
    ax3 = plt.subplot2grid((4, 2), (0, 1), colspan=1)
    ax4 = plt.subplot2grid((4, 2), (1, 1), colspan=1)
    # ax5 = plt.subplot2grid((2, 2), (1, 0), colspan=4)
    ts_plot['Amount'][3:].plot(ax=ax1)
    ts_plot['Count'][3:].plot(ax=ax2) # need to x-share with ax1
    ts_plot[3:].boxplot(column=['Amount'], by=['Year'], ax=ax3)
    ts_plot[3:].boxplot(column=['Count'], by=['Year'], ax=ax4) # need to x-share with ax3
    plt.tight_layout(True)


def plot_heatmap(ts_icnpo_plot, figure_path):
    ts_icnpo_plot['ICNPO'] = ts_icnpo_plot['ICNPO'].astype(float)
    csfont = {'fontname': 'Helvetica'}
    hfont = {'fontname': 'Helvetica'}
    ts_icnpo_plot = ts_icnpo_plot[ts_icnpo_plot['ICNPO'].notnull()]
    ts_icnpo_plot['ICNPO'] = ts_icnpo_plot['ICNPO'].astype(int)
    sns.set_style('white')
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1,
                                   sharex=True, figsize=(16, 10))
    heatmap_data = pd.pivot_table(ts_icnpo_plot, values='Count',
                                   index=['Year-Month'],
                                   columns='ICNPO')
    my_cmap = mpl.cm.get_cmap('Oranges')
    my_cmap.set_under('w')
    ee = sns.heatmap(heatmap_data, ax=ax1, cmap=my_cmap,
                     xticklabels=True,cbar_kws={'format': '%.2f%%',
                                                 'pad': 0.03},
                     vmin=0.0000000001)
    cbar = ax1.collections[0].colorbar
    cbar.set_label('Number of Payments', labelpad=-65, fontsize=12)

    ee.set_xlabel('')
    ee.set_ylabel('')
    heatmap_data = pd.pivot_table(ts_icnpo_plot[5:], values='Amount',
                                  index=['Year-Month'],
                                  columns='ICNPO')
    my_cmap = mpl.cm.get_cmap('Blues')
    my_cmap.set_under('w')
    ff = sns.heatmap(heatmap_data, ax=ax2, cmap=my_cmap, vmin=0.0000000001,
                     xticklabels=True, cbar_kws={'format': '%.2f%%',
                                                 'pad': 0.03})
    cbar = ax2.collections[0].colorbar
    cbar.set_label('Total Value of Payments', labelpad=-65, fontsize=12)
    ff.set_xlabel('')
    ff.set_ylabel('')
    ax1.text(x=0.5, y=1.03, s='Total Number of Payments Across ICNPO and Time',
             fontsize=16, ha='center', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax1.text(x=0.0, y=1.0, s='A.',
             fontsize=30, ha='left', va='bottom', transform=ax1.transAxes,
             **csfont)
    ax2.text(x=0.5, y=1.03, s='Total Payment Amount Per Month Across ICNPO and Time',
             fontsize=16, ha='center', va='bottom', transform=ax2.transAxes,
             **csfont)
    ax2.text(x=0.0, y=1.0, s='B.',# weight='bold',
             fontsize=30, ha='left', va='bottom', transform=ax2.transAxes,
             **csfont)
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'heatmaps.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'heatmaps.png'),
                bbox_inches='tight')


def class_groupings(pay_df, cc_name, cc_class):
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
    cc_merge = pd.merge(cc_merge, cc_class, how='left',
                        left_on='regno', right_on='regno')
    cc_class_count = cc_merge.groupby(['classtext'])['classtext'].\
        count().reset_index(name="count")
    cc_class_val = cc_merge.groupby(['classtext'])['amount'].\
        sum().reset_index()
    cc_class_merge = pd.merge(cc_class_count, cc_class_val, how='left',
                              left_on='classtext', right_on='classtext')
    cc_class_merge['amount_pc'] = (cc_class_merge['amount'] /
                                   cc_class_merge['amount'].sum())*100
    cc_class_merge['count_pc'] = (cc_class_merge['count'] /
                                  cc_class_merge['count'].sum())*100
    print(cc_class_merge[['classtext', 'amount_pc', 'count_pc']].round(3))


def charity_age(cc_pay_df, cc_sup, cc_name, cc_class, figure_path):
    titlesize = 14
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
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 9))
    g = sns.distplot(ccgdata_regdate, ax=ax1, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#377eb8', 'alpha': 0.35,
                               'edgecolor': 'k'}, label='CCG Suppliers',
                     bins=np.arange(1950, 2020, 3))
    g = sns.distplot(cc_regdate, ax=ax1, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.35,
                               'edgecolor': 'k'},
                     label='All CC', bins=np.arange(1950, 2020, 3))
    ax1.set_ylabel("Normalized Frequency", fontsize=12)
    ax1.set_xlabel("Charity Registration Year", fontsize=12)
    ax1.set_title('Distributions of Registration Years',
                  **csfont, fontsize=titlesize, y=1.02)
    ax1.set_title('A.', **csfont, fontsize=titlesize+5, loc='left')
    sns.despine()
    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)

    a = cc_sup[cc_sup['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    b = cc_name[cc_name['regdate'].notnull()]['regdate'].\
        astype(str).str[0:4].astype(float)
    percs = np.linspace(0, 100, 40)
    qn_a = np.percentile(a, percs)
    qn_b = np.percentile(b, percs)
    ax2.plot(qn_a, qn_b, ls="", marker="o", color='#377eb8',
             markersize=9, fillstyle='none')
    x = np.linspace(np.min((qn_a.min(), qn_b.min())),
                    np.max((qn_a.max(), qn_b.max())))
    ax2.plot(x, x, color='#d3d3d3', ls="--")
    ax2.set_ylabel("CCG Supplier Registration Years",
                   fontsize=12)
    ax2.set_xlabel("All CC Registration Years",
                   fontsize=12)
    ax2.set_title('Q-Q Plot of Registration Years',
                  **csfont, fontsize=titlesize, y=1.02)
    ax2.set_title('B.', loc='left',
                  **csfont, fontsize=titlesize+5)

    def ecdf(data):
        """ Compute ECDF """
        x = np.sort(data)
        n = x.size
        y = np.arange(1, n+1) / n
        return(x, y)

    x1, y1 = ecdf(cc_regdate)
    ax3.plot(x1, y1, label='All Charity Commission',
             color='#ff7f00', alpha=0.8)
    x2, y2 = ecdf(ccgdata_regdate)
    ax3.plot(x2, y2, label='CCG Suppliers', color='#377eb8', alpha=0.8)
    x3, y3 = ecdf(cc_adv_date)
    ax3.plot(x3, y3, label='Advancement of Health',
             color='#228B22', alpha=0.8)
    ax3.set_ylabel("Proportion of Data", fontsize=12)
    ax3.set_xlabel("Charity Registration Years", fontsize=12)
    ax3.set_title('Empirical Cumulative Distribution',
                  **csfont, fontsize=titlesize, y=1.02)
    ax3.set_title('C.', loc='left',
                  **csfont, fontsize=titlesize+5)
    ax3.legend(loc='upper left', edgecolor='k',
               frameon=False, fontsize=10)
    h = sns.distplot(ccgdata_regdate, ax=ax4, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#377eb8', 'alpha': 0.35,
                               'edgecolor': 'k'}, label='CCG Suppliers',
                     bins=np.arange(1950, 2020, 3))
    h = sns.distplot(cc_adv_date, ax=ax4, kde_kws={'gridsize': 500},
                     hist_kws={'color': '#ff7f00', 'alpha': 0.35,
                               'edgecolor': 'k'},
                     label='Health Charity', bins=np.arange(1950, 2020, 3))
    ax4.set_ylabel("Normalized Frequency", fontsize=12)
    ax4.set_xlabel("Charity Registration Year", fontsize=12)
    ax4.set_title('Comparison with Healthcare Charities',
                  **csfont, fontsize=titlesize, y=1.02)
    ax4.set_title('D.',
                  **csfont, fontsize=titlesize+5, loc='left')
    h.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'age_distributions.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'age_distributions.png'),
                bbox_inches='tight')


def plot_choropleths(gdf, figure_path):
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
    cmap = plt.cm.get_cmap('Blues', k)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)]
    cmap_list.append('#ededed')
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='count_pc_cc_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
             alpha=0.8, ax=ax1)
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
    cmap = plt.cm.get_cmap('OrRd', k)
    cmap_list = [rgb2hex(cmap(i)) for i in range(cmap.N)]
    cmap_list.append('#ededed')
    cmap_with_grey = colors.ListedColormap(cmap_list)
    gdf.plot(column='amount_pc_cc_cat', edgecolor='k', cmap=cmap_with_grey,
             legend=True, legend_kwds=dict(loc='center left',
                                           bbox_to_anchor=(0.035, 0.5),
                                           frameon=False, fontsize=titlesize-4),
             alpha=0.8, ax=ax2)
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
                      hist_kws={'color': '#377eb8', 'alpha': 0.35,
                               'edgecolor': 'k', 'label': 'Histogram'})
    ee.set_xlim(0, None)
    ee.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ee.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ee.set_xlabel("")

#    g.legend(loc='upper left', edgecolor='k', frameon=False, fontsize=10)
    count_array = gdf[gdf['amount_pc_cc']!='No Data']['amount_pc_cc'].astype(float)
    ff = sns.distplot(count_array, ax=ax4, kde_kws={'color': '#ff7f00', 'alpha':0.9,
                                                    'label':'KDE'},
                      hist_kws={'color': '#ff7f00', 'alpha': 0.35,
                               'edgecolor': 'k', 'label': 'Histogram'})
    ff.set_xlim(0, None)
    ff.legend(loc='upper right', bbox_to_anchor=(1, 1.3),
              edgecolor='k', frameon=False, fontsize=10)
    ff.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ff.set_xlabel("")

    sns.despine()
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.65, right=.6)
    plt.savefig(os.path.join(figure_path, 'choropleth_map.svg'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'choropleth_map.png'),
                bbox_inches='tight', dpi=600)


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


def tabulate_charities(pay_df, cc_name, icnpo_df, cc_fin):
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
    cc_merge


def icnpo_groupings(pay_df, cc_name, icnpo_df, icnpo_lookup):
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
    icnpo_out = pd.merge(icnpo_lookup, count_icnpo_pc, how='left', left_on = 'icnpo',
                         right_on = 'ICNPO')
    icnpo_out = pd.merge(icnpo_out, sum_icnpo_pc, how='left', on = 'ICNPO')
    icnpo_out = icnpo_out.drop(columns=['icnpo_desc', 'icnpo_desc', 'in_original_spec', 'ICNPO'])
    icnpo_out = icnpo_out[icnpo_out['icnpo'].notnull()]
    icnpo_out['icnpo'] = icnpo_out['icnpo'].astype(int)
    icnpo_out['icnpo'] = icnpo_out['icnpo'].fillna(9999)
    icnpo_out['count'] = icnpo_out['count'].fillna(0)
    icnpo_out['amount'] = icnpo_out['amount'].fillna(0)
    print(icnpo_out.round(3))


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
