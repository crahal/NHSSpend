from bs4 import BeautifulSoup
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import time
import re
import logging
from parsing_tools import parse_wrapper
from scraping_tools import get_url, createdir, get_all_files_one_page, request_wrapper
module_logger = logging.getLogger('nhsspend_application')
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_nhsengland(scrape, parse):
#    try:
    abrev = 'NHS_England'
    url = 'https://www.england.nhs.uk/'
    get_all = [url + 'publication/payments-over-25k-reports-2019/',
               url + 'publication/payments-over-25k-reports-2018/',
               url + 'publication/payments-over-25k-reports-2017/',
               url + 'publication/payments-over-25k-report-2016/',
               url + 'publication/payments-over-25k-report-2015/',
               url + 'publication/payments-over-25k-reports-2014/']
    data_2013 = url + 'wp-content/uploads/2014/11/payments-greater-25k-report-1314.xlsx'
    nhsengland_data_path = os.path.abspath(
                           os.path.join(__file__, '../..', 'data',
                                        'data_nhsengland', 'raw'))
    filepath = os.path.join(nhsengland_data_path, abrev)
    if scrape is True:
#        try:
        for page in get_all:
            get_all_files_one_page(page, filepath, url)
            r = request_wrapper(data_2013)
            with open(os.path.join(filepath, 'data_2013.xls'), "wb") as csvfile:
                    csvfile.write(r.content)
#            module_logger.info('Downloaded file: NHS England 2013')
#        except Exception as e:
#            module_logger.debug('Problem downloading NHS England data')
    if parse is True:
        parse_wrapper(nhsengland_data_path, filepath, abrev)
#    except Exception as e:
#        module_logger.debug('NHSEngland fails entirely: ' + str(e))
