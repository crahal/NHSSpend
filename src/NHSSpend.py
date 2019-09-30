'''
Options:    scrapetrusts    :   scrape only data from NHS trusts
            scrapeccgs      :   scrape only data from ccgs
            scrapenationals :   scrape only national bodies\SHAs
            noscrape        :   dont scrape anything (default: scrape all)
            cleanrun        :   delete existing cache of data
            OCAPI           :   reconcilewith the OpenCorporatesAPI

Links last updated: constantly.
Links next updated: constantly.

To do:
    brackets indicate minus in amount field
    unknown file extensions
    add small sleeps
    should flush out directory
'''

import os
import sys
import shutil
import logging
import pandas as pd
from datetime import datetime
from scrape_ccgs import scrape_ccg


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
    #start_banner()
    rawpath = os.path.abspath(os.path.join(__file__, '../..', 'data',
                                           'data_nhsccgs', 'raw'))
    logpath = os.path.abspath(os.path.join(__file__, '../..', 'logging'))
    logger = setup_logging(logpath)
    if 'cleanrun' in sys.argv:
        try:
            for body in ['nationals', 'trusts', 'ccgs']:
                shutil.rmtree(os.path.join(rawpath, body))('25k' in a["href"].lower())
            print('*** Doing a clean run! Lets go! ***')
        except OSError:
            logger.info('cleanrun option passed, but cannot delete folders.')
    if os.path.exists(rawpath) is False:
        os.makedirs(rawpath)

#    ins_dict = pd.read_csv(os.path.abspath(
#        os.path.join(
#            __file__, '../..', 'data', 'support',
#            'institution_dict.csv')))
#    scrape_nationals(ins_dict, rawpath)
    #    if ('scrapetrusts' not in sys.argv) and
    #        ('scrapeccgs' not in sys.argv) and
    #        ('noscrape' not in sys.argv):
    # scrape_shas(institution_dict)
    # if ('scrapetrusts' not in sys.argv) and
    #   ('scrapeshas' not in sys.argv) and
    #   ('scrapenationals' not in sys.argv) and
    #   ('noscrape' not in sys.argv):
    # scrape_ccgs(institution_dict)
    # if ('scrapeccgs' not in sys.argv) and
    #   ('scrapeshas' not in sys.argv) and
    #   ('scrapenationals' not in sys.argv) and
    #   ('noscrape' not in sys.argv):
    # scrape_trusts(institution_dict)
    ccg_df = pd.read_csv(os.path.abspath(
                         os.path.join(__file__,'../..', 'data',
                                      'data_support', 'ccg_list.txt')),
                         sep=';')
    scrape_ccg(ccg_df)
