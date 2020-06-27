from bs4 import BeautifulSoup
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import pandas as pd
import time
import re
import logging
from parsing_tools import parse_wrapper
from scraping_tools import get_url, createdir, get_all_files_one_page, request_wrapper
module_logger = logging.getLogger('nhsspend_application')
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def NHS_AIR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.airedale-trust.nhs.uk'
        abrev = 'NHS_AIR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['Airedale-Values-and-Behaviours-Booklet.pdf',
                          'CQC-Certificate-of-Registration.pdf',
                          'SCT_D_FY2018-19_M01_RCF.pdf',
                          'WAYFINDER-INFORMATION-POINT-T2-v11-Staff.pdf',
                          'Wayfinding-FAQs.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ALD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://alderhey.nhs.uk/'
        abrev = 'NHS_ALD_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if 'download_file' in str(a["href"]):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_AaW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.awp.nhs.uk/'
        abrev = 'NHS_AaW_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if 'expenditure' in str(a.text.lower()):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a.text+'.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ASH_Trust(trust_df, trust_data_path, scrape, parse):
    """ no data"""


def NHS_BAR_Trust(trust_df, trust_data_path, scrape, parse):
    """ no data"""


def NHS_BHR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bhrhospitals.nhs.uk'
        abrev = 'NHS_BHR_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download.' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                if '.csv' in str(a['href']):
                                    ext = '.csv'
                                elif 'xlsx' in str(a['href']):
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']):
                                    ext = '.xls'
                                else:
                                    ext = '.unknown'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BEH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.beh-mht.nhs.uk/'
        abrev = 'NHS_BEH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BTS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bartshealth.nhs.uk'
        abrev = 'NHS_BTS_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())) &\
                   ('xls' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BAT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.basildonandthurrock.nhs.uk/'
        abrev = 'NHS_BAT_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            counter = 0
            createdir(trust_data_path, abrev)
            for page in url.split(';'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                if counter==67:
                    break # not sure exactly whats going on here
                for a in soup.find_all("a"):
                    if counter==67:
                        break
                    if a.has_attr('href'):
                        if 'download' in str(a["href"]):
                            if a.text not in exceptions:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = 'file_' + str(counter) + '.xlsx'
                                    counter = counter + 1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BED_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bedfordshirehospitals.nhs.uk/'
        abrev = 'NHS_BED_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        url = get_url(trust_df, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('spending' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))



def NHS_BER_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.berkshirehealthcare.nhs.uk'
        abrev = 'NHS_BER_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BCP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.bcpft.nhs.uk'
        abrev = 'NHS_BCP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BTH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bfwh.nhs.uk'
        abrev = 'NHS_BTH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BOL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.boltonft.nhs.uk/'
        abrev = 'NHS_BOL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BRD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bdct.nhs.uk'
        abrev = 'NHS_BRD_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['Supplies-procurement-dashboard-summary-2014-15.pdf',
                          'Supplies-procurement-dashboard-summary-2015-2016-Q1.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BRA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bradfordhospitals.nhs.uk/'
        abrev = 'NHS_BRA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['03-04_Annual_Report_Quality_and_Accounts_Final_MASTER.pdf',
                          'Annual-Report-Accounts-2008-09-reduced.pdf',
                          'annual_report_and_accounts_2013-14.pdf',
                          'annual_report_and_accounts_2014-15.pdf',
                          'annual_report_and_accounts_2015-16.pdf',
                          'Annual-Report-and-Accounts-2007-08.pdf',
                          'Annual-Report-and-Accounts-2009-10.pdf',
                          'Annual-Report-and-Accounts-2010-11.pdf',
                          'Annual-Report-and-Accounts-2011-12.pdf',
                          'Annual-Report-and-Accounts-2017-18.pdf',
                          'Bradford-Hospitals-Charity-Annual-Report-2017.pdf',
                          'BTHFT-Annual-Report-and-Accounts-2012-13-reduced.pdf',
                          'final_annual_report-2017.pdf',
                          '19060403-04_Annual_Report_Quality_and_Accounts_Final_MASTER.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BRI_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://bridgewater.nhs.uk/'
        abrev = 'NHS_BRI_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BSH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.bsuh.nhs.uk/'
        abrev = 'NHS_BSH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BUC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.buckshealthcare.nhs.uk/'
        abrev = 'NHS_BUC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cht.nhs.uk/'
        abrev = 'NHS_CAH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cuh.nhs.uk/'
        abrev = 'NHS_CUH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for page in range(1, 5):
                get_all_files_one_page(url+str(page), filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cpft.nhs.uk/'
        abrev = 'NHS_CAP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CCS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cambscommunityservices.nhs.uk/'
        abrev = 'NHS_CCS_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('25k' in str(a["href"].lower())) & \
                   ('csv' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = str(a["href"]).split('/')[-1]+'.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_CAI_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.candi.nhs.uk/'
        abrev = 'NHS_CAI_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CNW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cnwl.nhs.uk/'
        abrev = 'NHS_CNW_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                print(a['href'])
                if ('expenditure' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = str(a["href"]).split('/')[-1]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_CLC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://clch.nhs.uk/'
        abrev = 'NHS_CLC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for page in range(1, 5):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'download' in str(a["href"]):
                            if a.text not in exceptions:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.strip()
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CHE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.chelwest.nhs.uk/'
        abrev = 'NHS_CHE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CWP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.cwp.nhs.uk/'
        abrev = 'NHS_CWP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CRH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_CRH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CHS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_CHS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_COP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_COP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BWC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_BWC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CWP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.cwp.nhs.uk/'
        abrev = 'NHS_CWP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_COC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.coch.nhs.uk/'
        abrev = 'NHS_COC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DaD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.cddft.nhs.uk/'
        abrev = 'NHS_DaD_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for page in url.split(';'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.covwarkpt.nhs.uk'
        abrev = 'NHS_CAW_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())) &\
                   ('csv' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a.text+'.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_CRO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.croydonhealthservices.nhs.uk/'
        abrev = 'NHS_CRO_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for page in url.split(';'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CNT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_CNT_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DGT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.dgt.nhs.uk/'
        abrev = 'NHS_DGT_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            counter = 0
            for a in soup.find_all("a"):
                if ('download_file' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text + str(counter) + '.csv'
                            counter = counter + 1
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.dgt.nhs.uk/about-us/'
        abrev = 'NHS_DCH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download_file' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text + '.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DHC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.derbyshirehealthcareft.nhs.uk/'
        abrev = 'NHS_DHC_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download_file' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text + '.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DPT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_DPT_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text.strip().split('return')[0] + '.xls'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DAB_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.dbth.nhs.uk/'
        abrev = 'NHS_DAB_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DOR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.dchft.nhs.uk/'
        abrev = 'NHS_DOR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DHU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_DHU_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text.strip().split('return')[0] + '.xls'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DAW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_DAW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ENH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.enherts-tr.nhs.uk/'
        abrev = 'NHS_ENH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['9.-ENH-NHST-Annual-Audit-Letter-2016-17.pdf',
                          'East-and-North-Hertfordshire-NHST-Annual-Audit-Letter-2018-19.pdf',
                          'combined-annual-report-and-accounts-2018-19-2.pdf',
                          'East-and-North-Herts-NHST-Annual-Audit-Letter-2017-18.pdf',
                          'ENHT-G6_Declaration-1-2017-18-2.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ECH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.eastcheshire.nhs.uk/'
        abrev = 'NHS_ECH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EKH_Trust(trust_df, trust_data_path, scrape, parse):
    """ no data"""


def NHS_ELH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://elht.nhs.uk/'
        abrev = 'NHS_ELH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if 'download_file' in str(a["href"]):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ELF_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nelft.nhs.uk/'
        abrev = 'NHS_ELF_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())) &\
                   ('xls' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_EMA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.emas.nhs.uk'
        abrev = 'NHS_EMA_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if ('25000' in str(a["title"].lower())):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                name = a['title'].replace('/', '') + '.csv'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_EOE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.eastamb.nhs.uk/'
        abrev = 'NHS_EOE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SNE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.esneft.nhs.uk/'
        abrev = 'NHS_SNE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ESH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.surreyandsussex.nhs.uk/'
        abrev = 'NHS_ESH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_EAS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EPU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://eput.nhs.uk/'
        abrev = 'NHS_EPU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_FHF_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_FHF_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            r = request_wrapper(url)
            name = 'FHF_Master.xlsx'
            with open(os.path.join(filepath, name),
                      "wb") as csvfile:
                csvfile.write(r.content)
            module_logger.info('Downloaded file: ' + str(name))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GHF_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.qegateshead.nhs.uk/'
        abrev = 'NHS_GHF_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GEH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.geh.nhs.uk/'
        abrev = 'NHS_GEH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for page in range(1, 11):
                get_all_files_one_page(url+str(page), filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GHC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.ghc.nhs.uk/'
        abrev = 'NHS_GHC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GCS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.gloshospitals.nhs.uk'
        abrev = 'NHS_GCS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GOS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.gosh.nhs.uk/'
        abrev = 'NHS_GOS_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('href'):
                    if 'download' in str(a["href"]):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                name = a.text+'.xls'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_GWH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_GWH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GMM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.gmmh.nhs.uk/'
        abrev = 'NHS_GMM_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('download' in str(a["href"].lower())) &\
                   ('xls' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a.text+'.xlsx'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_GUY_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.guysandstthomas.nhs.uk'
        abrev = 'NHS_GUY_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAM_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(a["href"])
                                if '.csv' in str(a.text.lower()):
                                    ext = '.csv'
                                elif '.pdf' in str(a.text.lower()):
                                    ext = '.pdf'
                                elif 'xlsx' in str(a.text.lower()):
                                    ext = '.xlsx'
                                elif 'xls' in str(a.text.lower()):
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HAD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.hdft.nhs.uk/'
        abrev = 'NHS_HAD_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HER_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.hct.nhs.uk/'
        abrev = 'NHS_HER_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HPU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.hpft.nhs.uk/'
        abrev = 'NHS_HPU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HOM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_HOM_Trust'
        base_url = 'https://www.homerton.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a['href']).lower():
                                    ext = '.csv'
                                elif '.pdf' in str(a['href']).lower():
                                    ext = '.pdf'
                                elif 'xlsx' in str(a['href']).lower():
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']).lower():
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HUL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_HUL_Trust'
        base_url = 'https://www.hey.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a['href']).lower():
                                    ext = '.csv'
                                elif '.pdf' in str(a['href']).lower():
                                    ext = '.pdf'
                                elif 'xlsx' in str(a['href']).lower():
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']).lower():
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HUM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.humber.nhs.uk/'
        abrev = 'NHS_HUM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_IMP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_IMP_Trust'
        base_url = 'https://www.imperial.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'expenditure' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a['href']).lower():
                                    ext = '.csv'
                                elif '.pdf' in str(a['href']).lower():
                                    ext = '.pdf'
                                elif 'xlsx' in str(a['href']).lower():
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']).lower():
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_IOW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_IOW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_JPU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_JPU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_KAM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.kmpt.nhs.uk/'
        abrev = 'NHS_KAM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_KGH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_KGH_Trust'
        base_url = 'https://www.kgh.nhs.uk'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a['href']).lower():
                                    ext = '.csv'
                                elif '.pdf' in str(a['href']).lower():
                                    ext = '.pdf'
                                elif 'xlsx' in str(a['href']).lower():
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']).lower():
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_KIN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_KIN_Trust'
        base_url = 'https://www.kch.nhs.uk'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'DATA' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(a["href"])
                                name = a.text+'.csv'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_KNG_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_KNG_Trust'
        base_url = 'https://www.kingstonhospital.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if '25k' in a.text.lower():
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                name = a.text+'.xlsx'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
            cleanpath = os.path.join(filepath, '../..', 'cleaned', 'NHS_KNG_Trust.csv')
            df = pd.read_csv(cleanpath)
            supsplit=df['supplier'].str.split(' : ', expand=True)#.rename('Supplier')
            supsplit.rename({1:'supplier'},axis=1,inplace=True)
            df['supplier'] = supsplit['supplier']
            df.to_csv(cleanpath)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LSC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.lscft.nhs.uk/'
        abrev = 'NHS_LSC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_KCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.kentcht.nhs.uk/'
        abrev = 'NHS_KCH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
            cleaned = os.path.join(trust_data_path, '..',
                                   'cleaned', abrev+'.csv')
            with open(cleaned, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(cleaned, 'w') as fout:
                fout.writelines(data[1:])
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LTH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LTH_Trust'
        base_url = 'https://www.lancsteachinghospitals.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = ['201901 Expenditure Over Threshold Report Jan 2019 [xlsx] 23KB']
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text.strip() not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a['href']).lower():
                                    ext = '.csv'
                                elif '.pdf' in str(a['href']).lower():
                                    ext = '.pdf'
                                elif 'xlsx' in str(a['href']).lower():
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']).lower():
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LAY_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.leedsandyorkpft.nhs.uk/'
        abrev = 'NHS_LAY_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LCH_Trust'
        base_url = 'https://www.leedscommunityhealthcare.nhs.uk'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'seecms' in str(a['href']):
                        if a.text.strip() not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                ext = '.xlsx'
                                name = a.text+str(counter)+ext
                                counter = counter+1
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LEE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.leedsth.nhs.uk/'
        abrev = 'NHS_LEE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['3_11-February-Summary3', '3_11-February-Summary3.pdf',
                          '3_11-february-summary3.pdf', '3_11-february-summary3.pdf',
                          '02-May-Summary-Report', '02-May-Summary-Report.pdf',
                          '4_12-March-Summary2.pdf', '4_12-March-Summary2',
                          '03-June-Summary-Report', '03-June-Summary-Report.pdf',
                          '5_01-April-Summary3.pdf', '5_01-April-Summary3',
                          '5_01-april-summary3.pdf', '5_01-april-summary3']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        os.remove(os.path.join(filepath, '6_01-april-summary3.pdf'))
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LAG_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LAG_Trust'
        base_url = 'https://www.lewishamandgreenwich.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download.' in str(a['href']).lower()) &\
                           ('xls' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    ext = '.xlsx'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LIN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LIN_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LIP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LIP_Trust'
        base_url = 'https://www.lpft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text+'.xls'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LHC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.lhch.nhs.uk/'
        abrev = 'NHS_LHC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.rlbuht.nhs.uk/'
        abrev = 'NHS_LUH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LIW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.liverpoolwomens.nhs.uk/'
        abrev = 'NHS_LIW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LAS_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.split(':')[0].replace('\n','').replace('\t','').replace('  ','').strip()+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LNW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LNW_Trust'
        url = get_url(trust_df, abrev)
        base_url = 'https://www.lnwh.nhs.uk/'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a.text.split('[csv]')[0]+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LAD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_LAD_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('document' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text +'.xlsx'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MAT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.mtw.nhs.uk/'
        abrev = 'NHS_MAT_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['NoPOnoPaySep16.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MED_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.medway.nhs.uk/'
        abrev = 'NHS_MED_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['NoPOnoPaySep16.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MER_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.merseycare.nhs.uk/'
        abrev = 'NHS_MER_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MYO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MYO_Trust'
        base_url='https://www.midyorks.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                if '.csv' in str(a.text.lower()):
                                    ext = '.csv'
                                elif '.pdf' in str(a.text.lower()):
                                    ext = '.pdf'
                                elif 'xlsx' in str(a.text.lower()):
                                    ext = '.xlsx'
                                elif 'xls' in str(a.text.lower()):
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MIP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MIP_Trust'
        base_url = 'https://www.mpft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href'])) &\
                           ('spend' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MKU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MKU_Trust'
        base_url = 'https://www.mpft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('document' in str(a['href'])) &\
                           ('spend' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.split(':')[0].replace('\n','').replace('\t','').replace('  ','').strip()+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MOO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.moorfields.nhs.uk/'
        abrev = 'NHS_MOO_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
            cleanpath = os.path.join(filepath, '../..', 'cleaned',
                                     abrev + '.csv')
            df = pd.read_csv(cleanpath)
            df = df.drop(['amount'], axis=1)
            df['amount'] = df['grossvalue']
            df = df.drop(['grossvalue'], axis=1)
            df.to_csv(cleanpath)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nsft.nhs.uk/'
        abrev = 'NHS_NAS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            os.remove(os.path.join(filepath, '98_over 25k oracle feb 2020.csv'))
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://data.gov.uk/'
        abrev = 'NHS_NCH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NBR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nbt.nhs.uk/'
        abrev = 'NHS_NBR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NCU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NCU_Trust'
        base_url = 'https://data.gov.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('trust-expenditure' in str(a['href'])):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.split(':')[0].replace('\n','').replace('\t','').replace('  ','').strip()+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NEA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.neas.nhs.uk/'
        abrev = 'NHS_NEA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NEL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nelft.nhs.uk/'
        abrev = 'NHS_NEL_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download.' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                if '.csv' in str(a['href']):
                                    ext = '.csv'
                                elif 'xlsx' in str(a['href']):
                                    ext = '.xlsx'
                                elif 'xls' in str(a['href']):
                                    ext = '.xls'
                                else:
                                    ext = '.unknown'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NSC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://combined.nhs.uk/'
        abrev = 'NHS_NSC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NMU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.northmid.nhs.uk/'
        abrev = 'NHS_NMU_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'payment' in str(a['href']).lower():
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+str(counter)+ext
                                    counter = counter+1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NTH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nth.nhs.uk/'
        abrev = 'NHS_NTH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
            cleanpath = os.path.join(filepath, '../..', 'cleaned',
                                     abrev + '.csv')
            df = pd.read_csv(cleanpath)
            df = df.drop(['invoicepaymentamount'], axis=1)
            df.to_csv(cleanpath)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NWE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NWE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NWB_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NWB_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NGH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.northamptongeneral.nhs.uk//'
        abrev = 'NHS_NGH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            for root, dirs, files in os.walk(os.path.join(trust_data_path,
                                                          abrev)):
                for currentFile in files:
                    if currentFile.lower().endswith('.pdf'):
                        os.remove(os.path.join(root, currentFile))
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NOR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nhft.nhs.uk/'
        abrev = 'NHS_NOR_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'download.' in str(a['href']):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))



def NHS_NDE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.northdevonhealth.nhs.uk/'
        abrev = 'NHS_NDE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NLG_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nlg.nhs.uk/'
        abrev = 'NHS_NLG_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nuh.nhs.uk/'
        abrev = 'NHS_NUH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'download.' in str(a['href']):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NOT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.nottinghamshirehealthcare.nhs.uk/'
        abrev = 'NHS_NOT_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'download.' in str(a['href']):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_OXH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_OXH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_OUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.ouh.nhs.uk/'
        abrev = 'NHS_OUH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if '25k' in str(a['href']).lower():
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_OXL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://oxleas.nhs.uk/'
        abrev = 'NHS_OXL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_PEN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.pat.nhs.uk/'
        abrev = 'NHS_PEN_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_PEC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_PEC_Trust'
        base_url = 'https://www.penninecare.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href'])):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.split(':')[0].replace('\n','').replace('\t','').replace('  ','').strip()+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_POO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.poole.nhs.uk/'
        abrev = 'NHS_POO_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_POR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://data.gov.uk/'
        abrev = 'NHS_POR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_QEV_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_QEV_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RJA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.rjah.nhs.uk/'
        abrev = 'NHS_RJA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RDS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.rdash.nhs.uk/'
        abrev = 'NHS_RDS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RBE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.royalberkshire.nhs.uk/'
        abrev = 'NHS_RBE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['Contracts awarded 2014-15.xlsx',
                          'Royal Berkshire Charity 2015-16 Annual Report and Financial Statements.pdf',
                          'Capital Programmes 2018-19.xls']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RBH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.rbht.nhs.uk/'
        abrev = 'NHS_RBH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://data.gov.uk/'
        abrev = 'NHS_RCH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RDE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.rdehospital.nhs.uk/'
        abrev = 'NHS_RDE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RFL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.royalfree.nhs.uk/'
        abrev = 'NHS_RFL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RNO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_RNO_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('spend over' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text+'.xlsx'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_RPH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_RPH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('transactions' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text+'.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ROY_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.royalsurrey.nhs.uk/'
        abrev = 'NHS_ROY_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.ruh.nhs.uk/'
        abrev = 'NHS_RUH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAL_Trust'
        base_url = 'https://www.srft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('getresource' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = 'file_' + str(counter) + '.xlsx'
                                    counter = counter+1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SAI_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.salisbury.nhs.uk/'
        abrev = 'NHS_SAI_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.swbh.nhs.uk/'
        abrev = 'NHS_SAW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SHE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SHE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SFH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.sfh-tr.nhs.uk/'
        abrev = 'NHS_SFH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAT_Trust'
        base_url = 'https://www.srft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('uploads' in str(a['href']).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    if '.csv' in a["href"]:
                                        name = a.text + '.csv'
                                    elif '.xlsx' in a["href"]:
                                        name = a.text + '.xlsx'
                                    elif '.xls' in a["href"]:
                                        name = a.text + '.xls'
                                    else:
                                        name = a.text + '.unknown'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SHR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.shropscommunityhealth.nhs.uk/'
        abrev = 'NHS_SHR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.solent.nhs.uk/'
        abrev = 'NHS_SOL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://somersetft.nhs.uk/'
        abrev = 'NHS_SOM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SCA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.scas.nhs.uk/'
        abrev = 'NHS_SCA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SLA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SLA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_STE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.southtees.nhs.uk//'
        abrev = 'NHS_STE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWA_Trust'
        base_url = 'https://www.swft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download_file' in str(a['href']).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text + '.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SWY_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWY_Trust'
        base_url = 'https://www.southwestyorkshire.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('uploads' in str(a['href']).lower()) & \
                           ('20' in str(a["href"]).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text + '.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SOU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.swast.nhs.uk/'
        abrev = 'NHS_SOU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SUH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.southend.nhs.uk/'
        abrev = 'NHS_SUH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['standing_financial_instructions.pdf',
                          'scheme_of_delegation.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.southportandormskirk.nhs.uk/'
        abrev = 'NHS_SAO_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['standing_financial_instructions.pdf',
                          'scheme_of_delegation.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SGU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.stgeorges.nhs.uk/'
        abrev = 'NHS_SGU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SHK_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://data.gov.uk/'
        abrev = 'NHS_SHK_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_STO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_STO_Trust'
        base_url = 'https://www.stockport.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('expenditure over' in str(a.text).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"])[3:])
                                    name = a.text + '.xlsx'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SAB_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAB_Trust'
        base_url = 'https://www.sabp.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = ['Every Person, Every Story - Our Digital Journey (2020)',
                              'October 2019.pdf', 'October 2019', 'June 2019']
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download_file' in str(a["href"]).lower()) & \
                           (' 20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text + '.pdf'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.surreyandsussex.nhs.uk/'
        abrev = 'NHS_SAS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SUP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SUP_Trust'
        base_url = 'https://www.sussexpartnership.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('attachment' in str(a["href"]).lower()) & \
                           (' 20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.replace('\n','').replace('/','') + '.csv'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_TAM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://data.gov.uk/'
        abrev = 'NHS_TAM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TAV_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://tavistockandportman.nhs.uk/'
        abrev = 'NHS_TAV_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TEE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_TEE_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CHR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.christie.nhs.uk/'
        abrev = 'NHS_CHR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CLA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_CLA_Trust'
        base_url = 'https://www.clatterbridgecc.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter=0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download_file' in str(a["href"]).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text.replace('/', '') + str(counter) + '.xlsx'
                                    counter = counter+1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_DUD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.dgft.nhs.uk/'
        abrev = 'NHS_DUD_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ["Transparecyaugust-2013.pdf"]
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            os.remove(os.path.join(filepath, '78_transparecyaugust-2013.pdf'))
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HIL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.thh.nhs.uk/'
        abrev = 'NHS_HIL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['FOI_PublicationScheme_2019.pdf',
                          'Freedom_of_Information_Act_2000.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NEW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.newcastle-hospitals.org.uk'
        abrev = 'NHS_NEW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_PAL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_PAL_Trust'
        url = get_url(trust_df, abrev)
        base_url = 'https://www.pah.nhs.uk'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a.text.lower()):
                                    ext = '.csv'
                                elif '.pdf' in str(a.text.lower()):
                                    ext = '.pdf'
                                elif 'xlsx' in str(a.text.lower()):
                                    ext = '.xlsx'
                                elif 'xls' in str(a.text.lower()):
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_QEH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.qehkl.nhs.uk/'
        abrev = 'NHS_QEH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ROT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_ROT_Trust'
        base_url = 'http://www.therotherhamft.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if '25k' in str(a['href']).lower():
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url+a["href"])
                                name = a.text+'.xlsx'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ROB_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_ROB_Trust'
        base_url = 'https://www.rbch.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('data-from' in str(a['href']).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a.text + '.pdf'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ROM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.royalmarsden.nhs.uk/'
        abrev = 'NHS_ROM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['Annual%20Report%202018-19.pdf',
                          'Annual_Report_2018.pdf#page=86.pdf'
                          'RMH%202019%20prospectus%20web.pdf',
                          'Trust%20Org%20Charts%20-%20Sep%202019%20v1.pdf',
                          'Board%20of%20Directors%20Register%20of%20Interests%20Sep%202019.pdf',
                          'Business-conduct-policy.pdf',
                          'DPIA%20register%202018-19.pdf',
                          'Freedom-of-information-policy-and-procedure.pdf',
                          'Governors%20register%20-%202019.pdf',
                          'Leadership%20Team%20Register%20of%20Interests%20July%202019.pdf',
                          'Membership-recruitment-and-engagement-strategy.pdf',
                          'Sphere-fact-sheet.pdf',
                          'The%20Royal%20Marsden%20Five-Year-Strategic-Plan_040518.pdf',
                          'Trust%20Org%20Charts%20-%20Sep%202019%20v1.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ROW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_ROW_Trust'
        base_url = 'https://www.royalwolverhampton.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('easysiteweb' in str(a['href']).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a.text + '.xls'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WAL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WAL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TOR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.torbayandsouthdevon.nhs.uk/'
        abrev = 'NHS_TOR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LIC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.ulh.nhs.uk/'
        abrev = 'NHS_LIC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UCL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.uclh.nhs.uk/'
        abrev = 'NHS_UCL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HOD_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_HOD_Trust'
        base_url = 'https://www.uhdb.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_UHS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.uhs.nhs.uk/'
        abrev = 'NHS_UHS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UHB_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://hgs.uhb.nhs.uk/'
        abrev = 'NHS_UHB_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BAW_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.uhbristol.nhs.uk/'
        abrev = 'NHS_BAW_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['june_18_uhb_trust_site_map_a4_d4_revised_v2_june_2018.pdf',
                          'uhb_welcome_guide_oct19.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_COV_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.uhcw.nhs.uk/'
        abrev = 'NHS_COV_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UHL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.library.leicestershospitals.nhs.uk/'
        abrev = 'NHS_UHL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UHM_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_UHM_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UHN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'http://www.uhnm.nhs.uk/'
        abrev = 'NHS_UHN_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_UHP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_UHP_Trust'
        base_url = 'https://www.plymouthhospitals.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    if '.csv' in str(a['href']):
                                        ext = '.csv'
                                    elif 'xlsx' in str(a['href']):
                                        ext = '.xlsx'
                                    elif 'xls' in str(a['href']):
                                        ext = '.xls'
                                    else:
                                        ext = '.unknown'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WAH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WAH_Trust'
        base_url = 'https://whh.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('download' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(a["href"])
                                    name = a.text+'.pdf'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WHT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.walsallhealthcare.nhs.uk/'
        abrev = 'NHS_WHT_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WHH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.westhertshospitals.nhs.uk/foi_publication_scheme/'
        abrev = 'NHS_WHH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WLO_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.westlondon.nhs.uk/'
        abrev = 'NHS_WLO_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = ['Expenditure-over-%C2%A325k-Nov-2019.pdf',
                          'Expenditure-over-%C2%A325k-Dec-2019.pdf',
                          'Expenditure-over-%C2%A325k-Jan-2020.pdf',
                          'Annual-report-2016-web.pdf',
                          'Annual-report-2017-lowres.pdf',
                          'ANNUAL-REPORT-2017_18.pdf',
                          'Y56_RKL_Annual-Accounts-201516.pdf',
                          'Annual-Accounts-2016-17-v2.pdf',
                          'RKL_Y56-Annual-Accounts-201718.pdf']
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WSU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.wsh.nhs.uk'
        abrev = 'NHS_WSU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WSH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.westernsussexhospitals.nhs.uk/'
        abrev = 'NHS_WSH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WHI_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WHI_Trust'
        url = get_url(trust_df, abrev)
        base_url = 'https://www.whittington.nhs.uk/'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = ['Annual Audit Letter 2017-18.csv'
                              'Annual Audit Letter 2018-19.csv']
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('document' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    if len(a.text)>0:
                                        name = a.text + '.csv'
                                        with open(os.path.join(filepath, name),
                                                  "wb") as csvfile:
                                            csvfile.write(r.content)
                                        module_logger.info('Downloaded file: ' +
                                                           str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WIR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.wirralct.nhs.uk'
        abrev = 'NHS_WIR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WIU_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WIU_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WOR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WOR_Trust'
        url = get_url(trust_df, abrev)
        base_url = 'https://www.worcsacute.nhs.uk/'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            counter = 0
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('/file' in str(a['href']).lower()):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = 'file_' + str(counter) + '.csv'
                                    counter = counter + 1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WHC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_WHC_Trust'
        url = get_url(trust_df, abrev)
        base_url = 'https://www.hacw.nhs.uk/'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a['href']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                if '.csv' in str(a.text.lower()):
                                    ext = '.csv'
                                elif '.pdf' in str(a.text.lower()):
                                    ext = '.pdf'
                                elif 'xlsx' in str(a.text.lower()):
                                    ext = '.xlsx'
                                elif 'xls' in str(a.text.lower()):
                                    ext = '.xls'
                                else:
                                    ext = '.xlsx'
                                name = a.text+ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_WWL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.wwl.nhs.uk/'
        abrev = 'NHS_WWL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WYE_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.wyevalley.nhs.uk/'
        abrev = 'NHS_WYE_Trust'
        if scrape is True:
            filepath = os.path.join(trust_data_path, abrev)
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_YDH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://yeovilhospital.co.uk/'
        abrev = 'NHS_YDH_Trust'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('25k' in str(a["href"].lower())) & \
                   ('xls' in str(a["href"].lower())):
                    if a.text not in list_to_ignore:
                        try:
                            r = request_wrapper(a["href"])
                            name = str(a["href"]).split('/')[-1]+'.xls'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_YTH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_YTH_Trust'
        base_url = 'https://www.yorkhospitals.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if 'seecms' in str(a['href']):
                            if a.text.strip() not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    ext = '.csv'
                                    name = a.text+ext
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
            if parse is True:
                parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_YAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        base_url = 'https://www.yas.nhs.uk/'
        abrev = 'NHS_YAS_Trust'
        if scrape is True:
            filepath = os.path.join(trust_data_path, abrev)
            exceptions = []
            url = get_url(trust_df, abrev)
            createdir(trust_data_path, abrev)
            for split_url in url.split(';'):
                get_all_files_one_page(split_url, filepath, base_url,
                                       exceptions=exceptions)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BAS_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_BAS_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BCH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_BCH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_COP_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_COP_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EKH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_EKH_Trust'
        base_url = 'https://www.ekhuft.nhs.uk'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('easysiteweb' in str(a['href']).lower()) & \
                           ('20' in str(a.text).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a.text + '.xls'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HAR_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAR_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MIN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MIN_Trust'
        base_url = 'https://www.mcht.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        counter = 0
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for split_url in url.split(';'):
                r = request_wrapper(split_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('easysiteweb' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a.text + '_' + str(counter) + '.xls'
                                    counter = counter +1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MAN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MAN_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MES_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_MES_Trust'
        base_url = 'https://www.meht.nhs.uk/'
        url = get_url(trust_df, abrev)
        filepath = os.path.join(trust_data_path, abrev)
        counter = 0
        if scrape is True:
            createdir(trust_data_path, abrev)
            list_to_ignore = []
            for page in range(1,11):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('href'):
                        if ('getresource' in str(a['href']).lower()):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url+a["href"])
                                    name = 'file_' + str(counter) + '.csv'
                                    counter = counter +1
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NCI_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NCI_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NWA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NWA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ROH_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_ROH_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SFT_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SFT_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWL_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWL_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_STA_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_STA_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SEC_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_SEC_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NAN_Trust_scraper(trust_df, trust_data_path, scrape, parse):
    try:
        abrev = 'NHS_NAN_Trust'
        filepath = os.path.join(trust_data_path, abrev)
        if parse is True:
            parse_wrapper(trust_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def scrape_trust(trust_df, scrape, parse):
    ''' master trust scraping function '''
    print('Working on building a Trust Dataset!')
    if os.path.exists(os.path.abspath(
                      os.path.join(__file__, '../..', 'data', 'data_nhstrusts',
                                   'raw'))) is False:
        os.makedirs(os.path.abspath(
                    os.path.join(__file__, '../..', 'data', 'data_nhstrusts',
                                 'raw')))
    trust_data_path = os.path.abspath(
                      os.path.join(__file__, '../..', 'data', 'data_nhstrusts',
                                   'raw'))
    for scraper in trust_df['abrev'].tolist()[203:204]:
        try:
            globals()[str(scraper)+'_scraper'](trust_df, trust_data_path,
                                               scrape, parse)
        except Exception as e:
            module_logger.debug(str(scraper) + ' fails at the global level.')
