import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib_venn import venn3, venn3_circles
import matplotlib.patches as patches
np.warnings.filterwarnings('ignore')
from matplotlib import rc
#rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
#rc('text', usetex=True)
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.25


def load_suppliers(sup_path):
    sup_df = pd.read_csv(sup_path, sep='\t')
    return sup_df


def load_payments(pay_path):
    pay_df = pd.read_csv(pay_path, sep='\t',
                         usecols=['expensetype', 'supplier', 'date', 'dept',
                                  'amount', 'file', 'expensearea',
                                  'transactionnumber', 'verif_match',
                                  'query_string', 'query_string_n',
                                  'match_type'],
                         dtype={'query_string': str,
                                'query_string_n': str,
                                'verif_match': str,
                                'match_type': str,
                                'transactionnumber': str},
                         parse_dates=['date'])
    return pay_df


def summarize_suppliers(sup_df, pay_df):
    print('Length of supplier dataset:', len(sup_df))
    print('Total unique suppliers in supplier dataset:',
          len(sup_df['query_string'].unique()))
    if len(sup_df) != len(sup_df['query_string'].unique()):
        print('\nDanger! These two numbers should be the same! ' +
              'Possible duplicates in manual verification file...\n')
    print('Total unique normalized suppliers in supplier dataset:',
          len(sup_df['query_string_n'].unique()))
    print('Total unique verified suppliers in supplier dataset:',
          len(sup_df['verif_match'].unique()))
    print('Total verified suppliers dataset:',
          len(sup_df[sup_df['verif_match'].notnull()]))
    print('Total unverified suppliers in the suppliers dataset:',
          len(sup_df[sup_df['verif_match'].isnull()]))


def scoring_figures(sup_df, figure_path, figsizetuple):
    legend_fontsize = 10
    fig = plt.figure(figsize=figsizetuple)
    ax1 = plt.subplot2grid((3, 12), (0, 0), colspan=4)
    ax2 = plt.subplot2grid((3, 12), (0, 4), colspan=4)
    ax3 = plt.subplot2grid((3, 12), (0, 8), colspan=4)
    ax4 = plt.subplot2grid((3, 12), (1, 0), colspan=3)
    ax5 = plt.subplot2grid((3, 12), (1, 3), colspan=3)
    ax6 = plt.subplot2grid((3, 12), (1, 6), colspan=3)
    ax7 = plt.subplot2grid((3, 12), (1, 9), colspan=3)
    ax8 = plt.subplot2grid((3, 12), (2, 0), colspan=4)
    ax9 = plt.subplot2grid((3, 12), (2, 4), colspan=4)
    ax10 = plt.subplot2grid((3, 12), (2, 8), colspan=4)

    ax1.scatter(sup_df['score_0'], sup_df['score_0_n'],
                alpha=0.2, s=8, marker='o', edgecolor='#377eb8',
                color='w', linewidth=1)
    ax1.set_xlabel('$ES^1_r$', fontsize=legend_fontsize)
    ax1.set_ylabel('$ES^1_n$', fontsize=legend_fontsize)
    ax1.set_ylim(0, 40)
    ax1.set_xlim(0, 40)
    ax2.scatter(sup_df['match_0_lev'], sup_df['match_0_n_lev'],
                alpha=0.2, s=8, marker='o', edgecolor='#377eb8',
                color='w', linewidth=1)
    ax2.set_xlabel(r'$\mathcal{L}^1_r$', fontsize=legend_fontsize)
    ax2.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize)
    ax2.set_ylim(0, 60)
    ax3.scatter(sup_df['score_0_n'], sup_df['match_0_n_lev'],
                alpha=0.2, s=8, marker='o', edgecolor='#377eb8',
                color='w', linewidth=1)
    ax3.set_xlabel(r'$ES^1_n$', fontsize=legend_fontsize)
    ax3.set_ylabel(r'$\mathcal{L}^1_n$', fontsize=legend_fontsize)
    a = sns.distplot(sup_df[sup_df['score_0'].notnull()]['score_0'], ax=ax4,
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'alpha': 0.8},
                     hist=False, label='$ES^1_r$', bins=np.arange(0, 60, 1))
    a = sns.distplot(sup_df[sup_df['score_0_n'].notnull()]['score_0_n'],
                     ax=ax4, hist=False, label='$ES^1_n$',
                     kde_kws={'gridsize': 500,
                              'color': '#377eb8', 'alpha': 0.8},
                     bins=np.arange(0, 60, 1))
    a.set_xlim(0, 50)
    ax4.set_xlabel('Elasticsearch Score', fontsize=legend_fontsize)
    ax4.set_ylabel('Probability Density', fontsize=legend_fontsize)
    b = sns.distplot(sup_df[sup_df['match_0_lev'].notnull()]['match_0_lev'],
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'alpha': 0.8},
                     hist=False, label=r'$\mathcal{L}^1_r$',
                     bins=np.arange(0, 100, 1), ax=ax5)
    b = sns.distplot(sup_df[sup_df['match_0_n_lev'].notnull()]['match_0_n_lev'],
                     ax=ax5, kde_kws={'gridsize': 500,
                                      'color': '#377eb8', 'alpha': 0.8},
                     hist=False, label=r'$\mathcal{L}^1_n$',
                     bins=np.arange(0, 100, 1))
    b.set_xlim(0, 150)
    ax5.set_xlabel('Levenshtein Distance', fontsize=legend_fontsize)
    ax5.set_ylabel('Probability Density', fontsize=legend_fontsize)
    c = sns.distplot(sup_df[sup_df['score_1'].notnull()]['score_1'],
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'alpha': 0.8},
                     hist=False, ax=ax6, label=r'$ES^2_r$',
                     bins=np.arange(0, 60, 1))
    c = sns.distplot(sup_df[sup_df['score_1_n'].notnull()]['score_1_n'],
                     kde_kws={'gridsize': 500, 'color': '#377eb8',
                              'alpha': 0.8},
                     hist=False, ax=ax6, label='$ES^2_n$',
                     bins=np.arange(0, 60, 1))
    c.set_xlim(0, 40)
    ax6.set_xlabel('Elasticsearch Score', fontsize=legend_fontsize)
    ax6.set_ylabel('Probability Density', fontsize=legend_fontsize)
    d = sns.distplot(sup_df[sup_df['match_1_lev'].notnull()]['match_1_lev'],
                     kde_kws={'gridsize': 500,
                              'color': '#ff7f00', 'alpha': 0.8},
                     hist=False, ax=ax7, label=r'$\mathcal{L}^2_r$',
                     bins=np.arange(0, 100, 1))
    d = sns.distplot(sup_df[sup_df['match_2_n_lev'].notnull()]['match_1_n_lev'],
                     kde_kws={'gridsize': 500,
                              'color': '#377eb8', 'alpha': 0.8},
                     hist=False, ax=ax7, label=r'$\mathcal{L}^2_n$',
                     bins=np.arange(0, 100, 1))
    ax7.set_xlabel('Levenshtein Distance', fontsize=legend_fontsize)
    ax7.set_ylabel('Probability Density', fontsize=legend_fontsize)
    d.set_xlim(0, 175)
    ax8.scatter(sup_df['score_1'], sup_df['score_1_n'],
                alpha=0.2, s=8, marker='o', edgecolor='#ff7f00',
                color='w', linewidth=1)
    ax8.set_xlabel('$ES^2_r$', fontsize=legend_fontsize)
    ax8.set_ylabel('$ES^2_n$', fontsize=legend_fontsize)
    ax9.scatter(sup_df['match_1_lev'], sup_df['match_1_n_lev'],
                alpha=0.2, s=8, marker='o', edgecolor='#ff7f00',
                color='w', linewidth=1)
    ax9.set_xlabel(r'$\mathcal{L}^2_r$', fontsize=legend_fontsize)
    ax9.set_ylabel(r'$\mathcal{L}^2_n$', fontsize=legend_fontsize)
    ax9.set_xlim(0, 150)
    ax10.scatter(sup_df['score_1_n'], sup_df['match_1_n_lev'],
                 alpha=0.2, s=8, marker='o', edgecolor='#ff7f00',
                 color='w', linewidth=1)
    ax10.set_ylabel('$ES^2_n$', fontsize=legend_fontsize)
    ax10.set_xlabel(r'$\mathcal{L}^2_n$', fontsize=legend_fontsize)
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]:
        ax.grid(linestyle='--', linewidth='1',
                color='gray', alpha=0.1)
    for ax in [ax1, ax2, ax3, ax8, ax9, ax10]:
        ax.set_ylim(0,)
        ax.set_xlim(0,)
    for ax in [a, b, c, d]:
        ax.legend(edgecolor='w', fontsize=legend_fontsize)
    sns.despine()
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'matching_summary.png'), dpi=600)
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
              set_labels=('Suppliers on\nCharity Commission',
                          'Suppliers on\nCompanies House',
                          'Suppliers on\nNHS Digital'), alpha=0.5, ax=ax2)
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
    ax2.annotate(str(char_num_three) + ' suppliers on\nall three registers',
                 xy=v.get_label_by_id('111').get_position(),
                 fontsize=8, xytext=(+120, -70),
                 ha='center', textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.5', ec='k', fc='w', alpha=1),
                 arrowprops=dict(arrowstyle='->', color='k', linewidth=0.75,
                                 connectionstyle='arc3,rad=-0.4'))
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
    a = short_df['NHS'].plot(kind='bar', color=colors, alpha=0.5,
                             linewidth=1, width=0.65, edgecolor='k', ax=ax3)
    b = short_df['No Match'].plot(kind='bar', color=colors, alpha=0.5,
                                  linewidth=1, width=0.65, edgecolor='k',
                             ax=ax4)
    c = short_df['Company'].plot(kind='bar', color=colors, alpha=0.5,
                                 linewidth=1, width=0.65, edgecolor='k',
                                 ax=ax5)
    d = short_df['Doctor'].plot(kind='bar', color=colors, alpha=0.5,
                                linewidth=1, width=0.65, edgecolor='k',
                                ax=ax6)
    e = short_df['Charity'].plot(kind='bar', color=colors, alpha=0.5,
                                 linewidth=1, width=0.65, edgecolor='k',
                                 ax=ax7)
    f = short_df['Person'].plot(kind='bar', color=colors, alpha=0.5,
                                linewidth=1, width=0.65, edgecolor='k',
                                ax=ax8)
    sup = patches.Patch(facecolor=colors[0], label='Number Suppliers',
                       alpha=0.5,edgecolor='k',linewidth=1)
    val = patches.Patch(facecolor=colors[1], label='Payment Value',
                          alpha=0.5,edgecolor='k',linewidth=1)
    count = patches.Patch(facecolor=colors[2], label='Number Payments',
                          alpha=0.5,edgecolor='k',linewidth=1)
    plt.legend(handles=[sup, val, count], loc=2,fontsize=11, edgecolor='k',
               frameon=True)
    a.set_xlabel("NHS",fontsize=12,labelpad=10)
    b.set_xlabel("No Match",fontsize=12,labelpad=10)
    c.set_xlabel("Company",fontsize=12,labelpad=10)
    d.set_xlabel("Doctor",fontsize=12,labelpad=10)
    e.set_xlabel("Charity",fontsize=12,labelpad=10)
    f.set_xlabel("Person",fontsize=12,labelpad=10)
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
            vals = axy.get_yticks()/100
            axy.set_yticklabels(['{:,.0%}'.format(x) for x in vals],fontsize=12)

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
    wedges = [patch for patch in ax1.patches if isinstance(patch, patches.Wedge)]
    for w in wedges:
        w.set_linewidth(0.52)
        w.set_edgecolor('k')
    centre_circle = plt.Circle((0,0), 0.75, color='black', fc='white',linewidth=.25)

    ax1.axis('equal')
    plt.tight_layout(True)
    plt.savefig(os.path.join(figure_path, 'match_distribution.png'), dpi=600)
    plt.savefig(os.path.join(figure_path, 'match_distribution.pdf'))
    plt.show()
