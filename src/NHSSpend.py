'''
Options: New options here.

Links last updated: constantly.
Links next updated: constantly.

To do: New todo here

next to fix bury,  haf, sthe
'''

import os
import logging
import pandas as pd
from datetime import datetime
from scrape_and_parse_ccgs import scrape_ccg
from merge_and_evaluate_tools import merge_eval_scrape, merge_eval_recon
from generate_output import output_for_dashboard
from reconciliation import reconcile_general, reconcile_general_norm


def start_banner():
    print('**************************************************')
    print('*********Welcome to NHSSpend v.0.0.1!*********')
    print('**********************************************')
    print('** This is an extremely preliminary version **')
    print('**       Please raise issues on GitHub!     **')
    print('**       Started at ' +
          str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '     **')
    print('**********************************************')


def end_banner():
    print('\n**************************************************')
    print('**** Program finished at ' +
          str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '  ****')
    print('**************************************************')


def setup_logging(logpath):
    if os.path.exists(logpath):
        if os.path.isfile(os.path.abspath(
                          os.path.join(logpath, 'nhsspend.log'))):
            os.remove(os.path.abspath(
                      os.path.join(logpath, 'nhsspend.log')))
    else:
        os.makedirs(logpath)
    logger = logging.getLogger('nhsspend_application')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler((os.path.abspath(
        os.path.join(logpath, 'nhsspend.log'))))
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    start_banner()
    datapath = os.path.abspath(os.path.join(__file__, '../..', 'data'))
    rawpath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                           'data_nhsccgs', 'raw'))
    datasummarypath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                                   'data_summary'))
    dashboardpath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                                 'data_dashboard'))
    cleanpath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                             'data_nhsccgs', 'cleaned'))
    mergepath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                             'data_nhsccgs', 'merge'))
    reconcilepath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                                 'data_nhsccgs', 'reconciled'))
    norm_path = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                             'data_support', 'norm_dict.tsv'))
    logpath = os.path.abspath(os.path.join(__file__, '../..', 'logging'))
    htmlpath = os.path.abspath(os.path.join(__file__, '../..', 'html_files'))
    for path in [rawpath, cleanpath, mergepath, logpath,
                 htmlpath, dashboardpath]:
        if os.path.exists(path) is False:
            os.makedirs(path)
    logger = setup_logging(logpath)
    ccg_df = pd.read_csv(os.path.abspath(
                         os.path.join(__file__, '../..', 'data',
                                      'data_support', 'ccg_list.txt')),
                         sep=';')
#    scrape_ccg(ccg_df)
#    merge_eval_scrape(cleanpath, mergepath, htmlpath,
#                              datasummarypath, logpath)
    uniq_name = 'unique_unmatched_suppliers.tsv'
#    reconcile_general(mergepath, reconcilepath, uniq_name)
#    reconcile_general_norm(mergepath, reconcilepath, uniq_name, norm_path)
    merge_eval_recon(reconcilepath, norm_path, datapath, mergepath, logpath)
#    output_for_dashboard(mergepath, dashboardpath) # @TODO: add in reconciles
#    output_for_analysis() # @TODO
