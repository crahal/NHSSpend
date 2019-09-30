from bs4 import BeautifulSoup
# import traceback
import time
import requests
import os
import re
import logging
from parsing_tools import parse_data, parse_wrapper
from scraping_tools import get_url, createdir, get_all_files_one_page
# import pandas as pd
module_logger = logging.getLogger('nhsspend_application')


def NHS_AWC_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'http://www.airedalewharfedalecravenccg.nhs.uk'
    abrev = 'NHS_AWC_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        list_not_proc = ['/seecmsfile/?id=1251',
                         '/seecmsfile/?id=1368',
                         '/seecmsfile/?id=1368',
                         '/seecmsfile/?id=1251']
        for a in soup.find_all("a", href=True):
            if '/seecmsfile/' in a["href"]:
                if a["href"] not in list_not_proc:
                    try:
                        r = requests.get(base_url + a["href"])
                        name = re.sub(r'\W+', '', a["href"]) + '.csv'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Porblem downloading: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_ASH_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_ASH_CCG'
    base_url = 'https://www.ashfordccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in range(1, 9):
        get_all_files_one_page(url+'p='+str(page), filepath, base_url,
                               exceptions=['408912.xlsx'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BARK_CCG_scraper(ccg_df, ccg_data_path):
    '''' all pdfs, wait for pdf parser'''
    abrev = 'NHS_BARK_CCG'
    createdir(ccg_data_path, abrev)
    base_url = 'http://www.barkingdagenhamccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BARNET_CCG_scraper(ccg_df, ccg_data_path):
    '''' all pdfs, wait for pdf parser'''
    abrev = 'NHS_BARNET_CCG'
    createdir(ccg_data_path, abrev)
    base_url = 'http://www.barnetccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BARNS_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_BARNS_CCG'
    base_url = 'http://www.barnsleyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url,
                               exceptions=['02P%202015-2016-03.csv'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BAB_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://basildonandbrentwoodccg.nhs.uk'
    abrev = 'NHS_BAB_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = ['99E M03 over £25k report June 2017 v2.xlsx',
                      '99E M11 over £25k report February 2018 (1).xlsx',
                      '99E M06 over £25k report September 2018.xlsx',
                      '99E M08 over 25k report November 2017.xlsx',
                      '99E M05 over £25k report August 2017.xlsx',
                      '99E M07 over 25k report October 2017.xlsx',
                      '99E M09 over £25k report December 2017.xlsx',
                      '99E M05 over £25k report August 2018.xlsx',
                      '99E M07 over 25k report October 2018.xlsx',
                      'Month 01 Basildon and Brentwood CCG transactions over £25k report 2017 18.xlsx',
                      '99E M12 over 25k report March 2019.xlsx',
                      '99E M12 over £25k report March 2018.xlsx',
                      '99E M07 over 25k report October 2017 (2).xlsx',
                      '99E M08 over £25k report November 2018.xlsx',
                      '99E M02 over £25k report May 2017 v4.xlsx',
                      '99E M06 over £25k report September 2017 (1)',
                      '99E M10 over £25k report January 2018 (1).xlsx',
                      '99E M09 over 25k report December 2018.xlsx',
                      'Copy of 99E M10 over 25k report January 2019 final.xlsx',
                      '99E M03 over £25k report June 2018.xlsx',
                      '99E M02 over £25k report May 2018.xlsx',
                      '99E M02 over £25k report February 2019.xlsx',
                      '99E M01 over £25k report April 2018.xlsx',
                      '99E M04 over £25k report July 2017 v2.xlsx']
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BED_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.bedfordshireccg.nhs.uk/page/'
    abrev = 'NHS_BED_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if 'downloadFile.php' in a["href"]:
                    try:
                        r = requests.get(base_url + a["href"])
                        name = re.sub(r'\W+', '', a["href"]) + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BERK_CCG_scraper(ccg_df, ccg_data_path):
    '''' all pdfs, wait for pdf parser'''
    abrev = 'NHS_BERK_CCG'
    createdir(ccg_data_path, abrev)
    base_url = 'https://www.berkshirewestccg.nhs.uk'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BEX_CCG_scraper(ccg_df, ccg_data_path):
    '''' mix of various file formats'''
    abrev = 'NHS_BEX_CCG'
    createdir(ccg_data_path, abrev)
    base_url = 'https://www.bexleyccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath, base_url,
                           exceptions=['Expenditure%20over%2025k%20July%202016.xls',
                                       'Expenditure%20over%2025k_February%202015.xlsx',
                                       'Expenditure%20over%2025k%20September%202016.xls',
                                       'Expenditure%20over%2025k%20August%202016.xls',
                                       'Expenditure%20over%2025k%20June%202016.xls',
                                       'Expenditure%20over%2025k%20October%202016.xls'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BIRM_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.birminghamandsolihullccg.nhs.uk'
    abrev = 'NHS_BIRM_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BWD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_BWD_CCG'
    createdir(ccg_data_path, abrev)
    # base_url = 'http://www.barnetccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BOLT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_BOLT_CCG'
    createdir(ccg_data_path, abrev)
    # base_url = 'http://www.barnetccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.boltonccg.nhs.uk/'
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BRAC_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.bradforddistrictsccg.nhs.uk'
    abrev = 'NHS_BRAC_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        list_not_proc = ['/seecmsfile/?id=305',
                         '/seecmsfile/?id=1250',
                         '/seecmsfile/?id=1251',
                         '/seecmsfileid/?id=295',
                         '/seecmsfileid/?id=297',
                         '/seecmsfileid/?id=279',
                         '/seecmsfileid/?id=285',]
        for a in soup.find_all("a", href=True):
            if '/seecmsfile/' in a["href"]:
                if a["href"] not in list_not_proc:
                    try:
                        r = requests.get(base_url + a["href"])
                        name = re.sub(r'\W+', '', a["href"]) + '.csv'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Porblem downloading: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BRAD_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.bradforddistrictsccg.nhs.uk/'
    abrev = 'NHS_BRAD_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        list_not_proc = ['/seecmsfile/?id=136',
                         '/seecmsfile/?id=1250',
                         '/seecmsfile/?id=208',
                         '/seecmsfile/?id=237',
                         '/seecmsfile/?id=242',
                         '/seecmsfile/?id=220',
                         '/seecmsfile/?id=221',
                         '/seecmsfile/?id=1251']
        for a in soup.find_all("a", href=True):
            if '/seecmsfile/' in a["href"]:
                if a["href"] not in list_not_proc:
                    try:
                        r = requests.get(base_url + a["href"])
                        name = re.sub(r'\W+', '', a["href"]) + '.csv'
                        if (name != 'httpsgcityyhcsorgukseecmsfileid1250.xlsx') or\
                           (name != 'httpsgcityyhcsorgukseecmsfileid1251.xlsx'):
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Porblem downloading: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BREN_CCG_scraper(ccg_df, ccg_data_path):
    ''' undeclared file extensions
        last updated: Monday 29th April 2019
    '''
    base_url = 'http://brentccg.nhs.uk'
    abrev = 'NHS_BREN_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_not_proc = []
    list_downloaded = []
    for split_url in url.split('|'):
        try:
            r = requests.get(split_url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if '25k' in a["href"]:
                    if (a["href"] not in list_not_proc) and\
                       ('tmpl=component' not in a["href"]) and\
                       (a['href'] not in list_downloaded):
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a["href"].split('/')[-1] + '.unknown'
                            list_downloaded.append(a["href"])
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Porblem downloading: ' +
                                                str(e))
        except Exception as e:
            module_logger.debug('Problem downloading: ' + str(e))
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BAH_CCG_scraper(ccg_df, ccg_data_path):
    ''' have to parse title properly for extension
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.brightonandhoveccg.nhs.uk'
    abrev = 'NHS_BAH_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_not_proc = ['downloadtokenttVIW7pA.xlsx',
                     'downloadtokenjmiA7Qz.xlsx']
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if 'download?token=' in a["href"]:
                if a["href"] not in list_not_proc:
                    try:
                        r = requests.get(base_url + a["href"])
                        if 'officedocument' in a["type"]:
                            ext = '.xlsx'
                        elif 'csv' in a["type"]:
                            ext = '.csv'
                        name = re.sub(r'\W+', '', (a["href"].split('/')[-1]))
                        with open(os.path.join(filepath, name+ext),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Porblem downloading: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BNSGSG_CCG_scraper(ccg_df, ccg_data_path):
    ''' have to iterate into each field'''
    base_url = 'https://bnssgccg.nhs.uk'
    search_url = '/search/?y=0&query=spend+over+25k&category=reports&x=0&page='
    abrev = 'NHS_BNSGSG_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        for page in range(1, 4):
            r = requests.get(base_url + search_url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if '/library/' in a["href"]:
                    get_all_files_one_page(base_url+a["href"], filepath)
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BROM_CCG_scraper(ccg_df, ccg_data_path):
    ''' have to iterate into each field'''
    base_url = 'https://www.bromleyccg.nhs.uk'
    abrev = 'NHS_BROM_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    for a in soup.find_all("a", href=True):
        if ('/expenditure-reports/' in a["href"]) and\
           (a["href"] != '/expenditure-reports/') and\
           (a["href"] != url):
            get_all_files_one_page(base_url + a["href"], filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_BURY_CCG_scraper(ccg_df, ccg_data_path):
    '''' note! currently www.bury.nhs.uk is down so ignore log errors'''
    abrev = 'NHS_BURY_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    get_all_files_one_page(url, filepath,
                           exceptions=['25k_expenditure_April_2016.csv',
                                       'july-2013.csv',
                                        '25k_Expenditure_January_2017.csv',
                                        '25k_Expenditure_September_2016.csv',
                                        'January-2015.csv',
                                        'May-2014.csv',
                                        'November_2015_transaction_analysis.csv',
                                        '25k_Expenditure_January_2018.csv',
                                        'transactions_analysis_October_2015.csv',
                                        '25k_Expenditure_June_2016.csv',
                                        'april-2013.csv'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_CALD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CALD_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    got_this = []
    try:
        for a in soup.find_all("a", href=True):
            if '/download/expenditure' in a["href"]:
                r = requests.get(a["href"])
                soup = BeautifulSoup(r.content, 'lxml')
                for b in soup.find_all("a", href=True):
                    if ('/download/expenditure' in b["href"]) and\
                       (b["href"] not in got_this):
                        r = requests.get(b["href"])
                        name = b["href"].split('/')[-1]
                        name = re.sub(r'\W+', '', name) + '.pdf'
                        got_this.append(name)
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
        get_all_files_one_page(url, filepath)
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Everything failed: ' + str(e))


def NHS_CAP_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CAP_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    base_url = 'https://www.cambridgeshireandpeterboroughccg.nhs.uk'
    url = get_url(ccg_df, abrev)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        for a in soup.find_all("a", href=True):
            if '/easysiteweb/getresource' in a["href"]:
                r = requests.get(base_url + a["href"])
                name = a.text
                with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                module_logger.info('Downloaded file: ' + str(name))
        try:
            df = parse_data(ccg_data_path, abrev)
            df.to_csv(os.path.join(filepath, '../../..', 'cleaned',
                                   'merged', 'ccg',
                                   abrev + '.csv'), index=False)
            module_logger.info('Successfully parsed: ' + abrev)
        except Exception as e:
            module_logger.debug('Parsing the files failed: ' + str(e))
    except Exception as e:
        module_logger.debug('Something serious has goine wrong: ' + str(e))


def NHS_CAMD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CAMD_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.camdenccg.nhs.uk'
    try:
        for page in url.split('|'):
            get_all_files_one_page(page, filepath, base_url)
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something serious has goine wrong: ' + str(e))


def NHS_CANT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CANT_CCG'
    base_url = 'https://www.canterburycoastalccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    try:
        for page in range(1, 9):
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if a.has_attr('title'):
                    if 'expenditure' in a["title"].lower():
                        r = requests.get(base_url + a["href"])
                        name = a["href"].split('/')[-1]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                                csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + name)
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something bad going on: ' + str(e))


def NHS_CPR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CPR_CCG'
    base_url = 'https://castlepointandrochfordccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"].replace(' ', '%20')
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_CLW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_CLW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.centrallondonccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_CAH_CCG_scraper(ccg_df, ccg_data_path):
    ''' seems clean (all pdfs), should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_CAH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.cityandhackneyccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_CWS_CCG_scraper(ccg_df, ccg_data_path):
    ''' seems clean, should update automatically,
        last updated: 1st May 2019 '''
    abrev = 'NHS_CWS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.coastalwestsussexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_COR_CCG_scraper(ccg_df, ccg_data_path):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_COR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://corbyccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if ('/downloads/' in a["href"]) and\
               ('excel' in a.text.lower()):
                try:
                    r = requests.get(base_url + a["href"])
                    name = a.text.replace(' ', '%20')+'.csv'
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                    i_see_you = 0
                    with open(os.path.join(filepath, name), "r",
                              encoding="ISO-8859-1") as input:
                        with open(os.path.join(filepath, 'cleaned_' + name),
                                  "w") as output:
                            for line in input:
                                if "department family" in line.lower():
                                    i_see_you = 1
                                if i_see_you == 1:
                                    output.write(line)
                    os.remove(os.path.join(filepath, name))
                    module_logger.info('deleted lines til good: ' + str(name))
                    time.sleep(0.5)
                except Exception as e:
                    module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something seriously wrong: ' + str(e))


def NHS_CRAW_CCG_scraper(ccg_df, ccg_data_path):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_CRAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.crawleyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        for page in range(1, 14):
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if a.has_attr('title'):
                    if '25k' in a["title"].lower():
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a["title"].replace(' ', '%20')
                            if '.csv' in a["href"]:
                                ext = '.csv'
                            elif '.pdf' in a["href"]:
                                ext = '.pdf'
                            elif '.xlsx' in a["href"]:
                                ext = '.xlsx'
                            elif '.xls' in a["href"]:
                                ext = '.xls'
                            else:
                                ext = '.unknown'
                            with open(os.path.join(filepath, name+ext),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded: ' +
                                               str(name + ext))
                        except Exception as e:
                            module_logger.debug('Bad DL?: '
                                                + str(name) + ':' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_CRO_CCG_scraper(ccg_df, ccg_data_path):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_CRO_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.croydonccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    excluded = ['2017%2008%20Expenditure%20over%2025k.xlsx']
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if ('expenditure' in a["href"].lower()) and\
               (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                try:
                    r = requests.get(base_url+a["href"])
                    name = a["href"].split('/')[-1].replace(' ', '%20')
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded: ' + str(name))
                except Exception as e:
                    module_logger.debug('Bad DL?: '
                                        + str(name) + ':' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_DARL_CCG_scraper(ccg_df, ccg_data_path):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_DARL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = ''
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    excluded = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if ('25k' in a["href"].lower()) and\
               (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                try:
                    r = requests.get(base_url+a["href"])
                    name = a["href"].split('/')[-1].replace(' ', '%20')
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded: ' + str(name))
                except Exception as e:
                    module_logger.debug('Bad DL?: ' + a["href"] + ':' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_DGS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_DGS_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_DONC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_DONC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.doncasterccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev, base_url)
    get_all_files_one_page(url, filepath, url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_DUD_CCG_scraper(ccg_df, ccg_data_path):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_DUD_CCG'
    url = get_url(ccg_df, abrev)
    base_url = ''
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    excluded = ['Dudley-CCG-Spend-Over-£25k-July-2015.csv']  # 404
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if ('25k' in a.text.lower()) and\
               (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                try:
                    r = requests.get(base_url+a["href"])
                    name = a["href"].split('/')[-1].replace(' ', '%20')
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded: ' + str(name))
                    time.sleep(0.5)
                except Exception as e:
                    module_logger.debug('Bad DL?: ' + a["href"] + ':' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_DDES_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_DDES_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_EAL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_EAL_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    base_url = 'https://www.ealingccg.nhs.uk/'
    try:
        for page in range(1, 8):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('25k' in a["href"].lower()) and\
                   ('spend' in a["href"].lower()):
                    try:
                        r = requests.get(base_url+a["href"])
                        name = a["href"].split('/')[-1].replace(' ', '%20')
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded: ' + str(name))
                        time.sleep(0.5)
                    except Exception as e:
                        module_logger.debug('Bad DL?: ' + a["href"] +
                                            ':' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_EANH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_EANH_CCG'
    base_url = 'https://www.enhertsccg.nhs.uk'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, url, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_EALA_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_EALA_CCG'
    base_url = 'https://eastlancsccg.nhs.uk'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if ('25k' in a["href"].lower()):
                try:
                    r = requests.get(base_url + a["href"])
                    name = a["href"].split('/')[-1] + '.unknown'
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded file: ' + str(name))
                except Exception as e:
                    module_logger.debug('Porblem downloading: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_ELAR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_ELAR_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath,
                           exceptions=['1.2-Privacy-Notice-NHS-ELRCCG-August-2018-FINAL-ELR-Corporate-047-FINAL.pdf',
                                       'Payments-over-£25k-August-2015.xlsx',
                                       'Payments-over-25k-August-18.xlsx',
                                       'Payments-over-£25k-July-2015.xlsx',
                                       'Payments-over-25k-–-March-2018-1.xlsx',
                                       'Payments-over-25k-–-February-2018-1.xlsx'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_ERY_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_ERY_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath,)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_ESTA_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_ESTA_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    base_url = 'http://eaststaffsccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        for page in range(2013, 2020):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('/file' in a["href"]) and ('25k' in a["href"]):
                    try:
                        r = requests.get(base_url + a["href"])
                        if "Content-Disposition" in r.headers.keys():
                            name = re.findall("filename=(.+)",
                                              r.headers["Content-Disposition"])[0].replace("\"", '')
                        else:
                            if '.csv' in str(a).lower():
                                ext = '.csv'
                            elif '.pdf' in str(a).lower():
                                ext = '.pdf'
                            elif '.xlsx' in str(a).lower():
                                ext = '.xlsx'
                            elif '.xls' in str(a).lower():
                                ext = '.xls'
                            else:
                                ext = '.unknown'
                            name = a["href"].split('/')[-2] + ext
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                    except Exception as e:
                            module_logger.debug('Porblem downloading: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_EASU_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_EASU_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    base_url = 'https://www.eastsurreyccg.nhs.uk'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        for page in range(0, 6):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('.csv' in a["href"]) or ('.xls' in a["href"]):
                    try:
                        r = requests.get(base_url + a["href"])
                        name = re.findall("filename=(.+)",
                                          r.headers["Content-Disposition"])[0].replace("\"", '')
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                            module_logger.debug('Porblem downloading: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_EACH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_EACH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.eastcheshire.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url)
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_ENF_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_ENF_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.enfieldccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_FAG_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_FAG_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.farehamandgosportccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GYAW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GYAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.greatyarmouthandwaveneyccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GLOU_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GLOU_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath,
    exceptions=['Contracts-Website-16-17.docx',
                'Declarations-of-Interest-Register_Live-1.pdf',
                'Hospitality-and-Gifts-Register_15.xls',
                'AI-10-1-August-2016-IGQC-Risk-Register-App-1.xlsx',
                'Penalties-Q1-sanctions-M3-final.pdf',
                'Q2-sanctions-final.pdf'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GHUD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GHUD_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.greaterhuddersfieldccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GYAW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GYAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.greatyarmouthandwaveneyccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GPRE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GPRE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.greaterprestonccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_GREE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_GREE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.greenwichccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HALT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HALT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.haltonccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HRAW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HRAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.hambletonrichmondshireandwhitbyccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url,
                               exceptions=['AfC_tc_of_service_handbook_fb.pdf',
                                           'ccg-model-cons-framework_version-3.2-oct-2015.pdf'])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HARI_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HARI_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.haringeyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HARD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HARD_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.harrogateandruraldistrictccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HARR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HARR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://harrowccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HAST_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HAST_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.hartlepoolandstocktonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HAR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HAR_CCG'
    url = get_url(ccg_df, abrev)
    print
    base_url = 'https://www.hastingsandrotherccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in range(1,14):
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HAV_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HAV_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.haveringccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HERE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HERE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.herefordshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HERT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HERT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://hillingdonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        for a in soup.find_all("a"):
            if ('spend' in str(a).lower()) and ('http' in str(a["href"])):
                try:
                    r = requests.get(a["href"])
                    name = a.text
                    with open(os.path.join(filepath, abrev + '_' + name + '.xlsx'),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded file: ' + str(name))
                except Exception as e:
                    module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
            module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HMR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HMR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.hmr.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HILL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HILL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://hillingdonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    counter = 0
    try:
        for page in url.split('|'):
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                for ext in ['.csv', '.xls', '.pdf']:
                    if ext in a["href"]:
                        counter = counter + 1
                        try:
                            r = requests.get(base_url + a["href"])
                            name = abrev + '_' + str(counter) + ext
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_HAMS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HAMS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.horshamandmidsussexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in range(1,15):
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HOUN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HOUN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.hounslowccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_HULL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_HULL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.ipswichandeastsuffolkccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_IAES_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_IAES_CCG'
    base_url = 'https://www.canterburycoastalccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    for a in soup.find_all("a", href=True):
        if 'expenditure report' in a.text.lower():
            r = requests.get(base_url + a["href"])
            print(base_url + a["href"])
            name = a.text.replace(' ', '').replace('£', '')+'.pdf'
            with open(os.path.join(filepath, name),
                      "wb") as csvfile:
                csvfile.write(r.content)
            module_logger.info('Downloaded file: ' + name)
    try:
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something bad going on: ' + str(e))


def NHS_IOW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_IOW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.isleofwightccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_ISL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_ISL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.islingtonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_KERN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_KERN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.kernowccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_KING_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_KING_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.kingstonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_KNOW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_KNOW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://knowsleyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LAMB_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LAMB_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.lambethccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LEIC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LEIC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.leicestercityccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LEWI_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LEWI_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.lewishamccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LINE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LINE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://lincolnshireeastccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a"):
            if a.has_attr('title'):
                if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                     '.pdf', '.ods',
                                                     '.xlsx']):
                    if a["title"] not in list_to_ignore:
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LINW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LINW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.lincolnshirewestccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in range(1, 10):
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LIVE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LIVE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.liverpoolccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in range(2013, 2020):
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_LUT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_LUT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.lutonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page_url in url.split('|'):
            r = requests.get(page_url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if 'download' in str(a["href"]):
                    if a.text not in list_to_ignore:
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a.text
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MANC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MANC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://manchesterccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_MAA_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MAA_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.mansfieldandashfieldccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in ['201920', '201819', '201718', '201617', '201516']:
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_MED_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MED_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.medwayccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page_url in url.split('|'):
            r = requests.get(page_url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if any(ext in a["href"] for ext in ['.csv', '.xls',
                                                    '.pdf', '.ods',
                                                    '.xlsx']):
                    if a.text not in list_to_ignore:
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a.text
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MERT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MERT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.mertonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_MESS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MESS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://midessexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    for page in ['2013-14-archive-1', '2014-15-archive-1', '2015-16',
                 '2016-17', '2017-18', '2018-19', '2019-2020']:
        try:
            r = requests.get(url + page)
            soup = BeautifulSoup(r.content, 'lxml')
            for table in soup.findAll('table'):
                for a in table.find_all("a"):
                    if '25k' in a["href"]:
                        try:
                            r = requests.get(base_url + a["href"])
                            name = str(a["href"]).split("/")[-2]+'.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
            parse_wrapper(ccg_data_path, filepath, abrev)
        except Exception as e:
            module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MK_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MK_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://midessexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a"):
            if '25' in a.text:
                try:
                    if 'http:' in a["href"]:
                        r = requests.get(a["href"])
                    else:
                        r = requests.get(base_url+a["href"])
                    if 'content-disposition' in r.headers.keys():
                        name = r.headers['content-disposition'].split('=')[1].replace('"','')
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                except Exception as e:
                    module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MCB_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_MCB_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.morecambebayccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a"):
            if a.has_attr('title'):
                if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                     '.pdf', '.ods',
                                                     '.xlsx']):
                    if a["title"] not in list_to_ignore:
                        try:
                            r = requests.get(base_url + a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' +
                                                str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NAS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NAS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.newarkandsherwoodccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in ['201920', '201819', '201718', '201617', '201516']:
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NENE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NAS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.neneccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in range(2016, 2020):
        get_all_files_one_page(url+str(pagenumber)+'.htm', filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NAG_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NAG_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.newcastlegatesheadccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NEWH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NEWH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.newhamccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NORC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NORC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.northcumbriaccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NDUR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NDUR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://northdurhamccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NEES_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NEES_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.neessexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NEHF_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NEHF_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northeasthampshireandfarnhamccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in ['2013', '2014', '2015-2', '2016-1', '2017', '2018', '2019-1']:
        print(url+str(pagenumber))
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NEL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NEL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northeastlincolnshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northhampshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page_url in url.split('|'):
        get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NK_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NK_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northkirkleesccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://northlincolnshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northnorfolkccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northtynesideccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NOST_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NOST_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northstaffsccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    for page in ['2013', '2014-1', '2015-1',
                 '2016-2', '2017-1', '2018', '2019']:
        try:
            r = requests.get(url + page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url + a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                except Exception as e:
                    pass
            parse_wrapper(ccg_data_path, filepath, abrev)
        except Exception as e:
            module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NWS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NWS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.nwsurreyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2014', '2015', '2016',
                     '2017', '2018-4', '2018', '2019']:
            r = requests.get(url + page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url + a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NORT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NORT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.northumberlandccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NNAE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NNAE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.nottinghamnortheastccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NORW_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.norwichccg.nhs.uk/'
    abrev = 'NHS_NORW_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['0', '20', '40', '60', '80', '100', '120', '140']:
            r = requests.get(url + page)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_NOCI_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NOCI_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.nottinghamcity.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_NW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_NW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.nottinghamwestccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_OLD_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_OLD_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.oldhamccg.nhs.uk/Publications/25k'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_PORT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_PORT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.portsmouthccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    # needs updating over time to be more flexible
    for pagenumber in ['201920', '201819', '2017',
                       '2016', '2015', '2018', '2014']:
        get_all_files_one_page(url+str(pagenumber)+'.htm', filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_RED_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_RED_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.redbridgeccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)



def NHS_RAB_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_RAB_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    base_url = 'http://www.redditchandbromsgroveccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        for page in range(2013, 2020):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                for a in soup.find_all("a", href=True):
                    if ('25k' in a["title"]):
                        r = requests.get(base_url + a["href"])
                        if "Content-Disposition" in r.headers.keys():
                            name = re.findall("filename=(.+)",
                                              r.headers["Content-Disposition"])[0].replace("\"", '')
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
            except Exception as e:
                module_logger.debug('Problem downloading: ' +
                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_ROTH_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_ROTH_CCG'
    base_url = 'http://www.rotherhamccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url,
                               exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_RUSH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_RUSH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.rushcliffeccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for pagenumber in ['1355', '4925', '4693', '4344',
                       '3487', '2757', '3902', '3890']:
        get_all_files_one_page(url+str(pagenumber), filepath,
                               base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SAL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SAL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.salfordccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in range(1, 9):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                for a in soup.find_all("a", href=True):
                    if ('25k' in str(a.text).lower()):
                        r = requests.get(a["href"])
                        if any(ext in str(a.text).lower() for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                            name = a.text
                        else:
                            name = a.text + '.csv'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
            except Exception as e:
                module_logger.debug('Problem downloading: ' +
                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_SHEF_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SHEF_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.sheffieldccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SHRO_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SHRO_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.shropshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SCHE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SCHE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.southcheshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in range(1, 9):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('expenditure' in str(a.text).lower()):
                    r = requests.get(base_url+a["href"])
                    if 'pdf' in r.headers['Content-Type']:
                        name = a.text.replace('\n','').replace(' ','') + '.pdf'
                    else:
                        name = a.text.replace('\n','').replace(' ','') + '.xlsx'
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_SEH_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_SEH_CCG'
    base_url = 'https://www.southeasternhampshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url,
                               exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SL_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://southlincolnshireccg.nhs.uk/'
    abrev = 'NHS_SL_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in range(2013,2020):
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SN_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_SN_CCG'
    base_url = 'https://www.southnorfolkccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url,
                               exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://data.gov.uk/dataset/030d9db2-f7d8-496a-b343-7f31844d9823/spend-over-25-000-in-nhs-south-sefton-ccg'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SOTE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SOTE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.southteesccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SOTY_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SOTY_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.southtynesideccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SWL_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://southwestlincolnshireccg.nhs.uk/'
    abrev = 'NHS_SWL_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['spend-over-25k-2019', 'spend-over-25k-2018',
                     '2017', '2016', '2015', '2014', '2013']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SOT_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.southamptoncityccg.nhs.uk/'
    abrev = 'NHS_SOT_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['422', '423', '425', '451', '484', '874', '874', '969']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["href"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a.text not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a.text
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
                except:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SEND_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://southendccg.nhs.uk/'
    abrev = 'NHS_SEND_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['2013-14-archive', '2014-15-archive' '201516archive',
                     '2016-17-archive', '2017-18-archive', '2018-19',
                     '2019-20']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
                except:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SAF_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SAF_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.southportandformbyccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_STHE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_STHE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.sthelensccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SAS_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.staffordsurroundsccg.nhs.uk/'
    abrev = 'NHS_SAS_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['2013-2', '2014-2', '2015-2', '2016',
                     '2017', '2018-2', '2019-2']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
                except:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_STOC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_STOC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.stockportccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a"):
            if '25' in a.text:
                try:
                    if 'http:' in a["href"]:
                        r = requests.get(a["href"])
                    else:
                        r = requests.get(base_url+a["href"])
                    if 'content-disposition' in r.headers.keys():
                        name = r.headers['content-disposition'].split('=')[1].replace('"','')
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                except Exception as e:
                    module_logger.debug('Problem download: ' + str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_STOK_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.stokeccg.nhs.uk/'
    abrev = 'NHS_STOK_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['2013-14-reports', '2014-reports', '2015-reports',
                     '2016-reports', '2017-reports', '2018-1', '2019-1']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
                except:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SD_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.surreydownsccg.nhs.uk/'
    abrev = 'NHS_SD_CCG'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    list_to_ignore = []
    try:
        for page in ['2013', '2014', '2015', '2016', '2017', '2018', '2019-1']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = requests.get(base_url + str(a["href"]))
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: '
                                                    + str(e))
                except:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_SUN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SUN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.sunderlandccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.surreyheathccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in range(2013, 2020):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if ('25k' in str(a["title"]).lower()):
                        r = requests.get(base_url+a["href"])
                        if 'pdf' in r.headers['Content-Type']:
                            name = a.text.replace('\n', '').replace(' ', '') + '.pdf'
                        else:
                            name = a.text.replace('\n', '').replace(' ', '') + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_SWAL_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SWAL_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.swaleccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    print(url)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_SWIN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SWIN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.swindonccg.nhs.uk/about-us/transparency-agenda'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            try:
                if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                     '.pdf', '.ods',
                                                     '.xlsx']):
                    r = requests.get(base_url+a["href"])
                    name = a["title"]
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
            except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_SH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_SH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.surreyheathccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in range(2013, 2020):
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if ('25k' in str(a["title"]).lower()):
                        r = requests.get(base_url+a["href"])
                        if 'pdf' in r.headers['Content-Type']:
                            name = a.text.replace('\n', '').replace(' ', '') + '.pdf'
                        else:
                            name = a.text.replace('\n', '').replace(' ', '') + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_TAG_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_TAG_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.tamesideandglossopccg.org/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            try:
                if '25k' in str(a["href"]).lower():
                    r = requests.get(base_url+a["href"])
                    name = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0].replace("\"", '')
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
            except Exception as e:
                pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_TAW_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_TAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.telfordccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2013-1', '2014-1', '2015-2',
                     '2017-2', '2018-2', '2019-5']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url+a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_THAN_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_THAN_CCG'
    base_url = 'https://www.thanetccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in range(0, 6):
        get_all_files_one_page(url + str(page), filepath, base_url,
                               exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_THUR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_THUR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://thurrockccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2019-20', '2018-19', '2017-18', '2016-17',
                     '2015-16', '2013-14-1', '2013-14']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url+a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_VOY_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_VOY_CCG'
    base_url = 'https://www.valeofyorkccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_TH_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_TH_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.towerhamletsccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_VOR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_VOR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.valeroyalccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in range(0, 10):
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if 'uploads' in str(a["href"]).lower():
                        r = requests.get(base_url+a["href"])
                        if 'pdf' in r.headers['Content-Type']:
                            name = a.text.replace('\n','').replace(' ','') + '.pdf'
                        else:
                            name = a.text.replace('\n','').replace(' ','') + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    print(e)
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_WAKE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WAKE_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.wakefieldccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WALS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WALS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://walsallccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page in range(2013, 2020):
        get_all_files_one_page(url+str(page)+'-publications',
                               filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WALT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WALT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.walthamforestccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WARR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WARR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.warringtonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WC_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WC_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.westcheshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WESS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WESS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://westessexccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2012-1', '2013-1', '2014-1', '2015-1', '2016-2',
                     '2017-2', '2018-1', '2019-1']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url+a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_WKEN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WKEN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.westkentccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    for page in range(1, 10):
        get_all_files_one_page(url+str(page),
                               filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WLAN_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WLAN_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.westlancashireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WLEI_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WLEI_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.westleicestershireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2013', '2014', '2015', '2016', '2017', '2018', '2019-1']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url+a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_WL_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_WL_CCG'
    base_url = 'https://www.westlondonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WN_CCG_scraper(ccg_df, ccg_data_path):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_WN_CCG'
    base_url = 'https://www.westnorfolkccg.nhs.uk'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    url = get_url(ccg_df, abrev)
    for page in url.split('|'):
        get_all_files_one_page(page, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WS_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.westsuffolkccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WAB_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WAB_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.wiganboroughccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            try:
                if 'phocadownload' in str(a["href"]).lower():
                    r = requests.get(base_url+a["href"])
                    if any(ext in a["href"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        name = a["href"]
                    elif 'pdf' in r.headers['Content-Type']:
                        name = str(a["href"]).split(':')[-1].replace('\n','').replace(' ','') + '.pdf'
                    else:
                        name = str(a["href"]).split(':')[-1].replace(' ','') + '.xlsx'
                    if '/' in name:
                        name = name.split("/")[-1]
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
            except Exception as e:
                pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_WILT_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WILT_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'http://www.wiltshireccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WIRR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WIRR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.wirralccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WIRR_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WIRR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.wirralccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    get_all_files_one_page(url, filepath, base_url, exceptions=[])
    parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_WOLV_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WOLV_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://wolverhamptonccg.nhs.uk/'
    createdir(ccg_data_path, abrev)
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        for page in ['2013-14', '2014-15', '2015-16', '2016-17',
                     '2017-18', '2018-19', '2019-20']:
            r = requests.get(url+str(page))
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        r = requests.get(base_url+a["href"])
                        name = a["title"]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_WYRE_CCG_scraper(ccg_df, ccg_data_path):
    abrev = 'NHS_WYRE_CCG'
    url = get_url(ccg_df, abrev)
    createdir(ccg_data_path, abrev)
    base_url = 'http://www.wyreforestccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            try:
                if ('25k' in str(a["title"]).lower()) or ('exp' in str(a["title"]).lower()):
                    print(base_url + a["href"])
                    r = requests.get(base_url + a["href"])
                    if "Content-Disposition" in r.headers.keys():
                        name = re.findall("filename=(.+)",
                                          r.headers["Content-Disposition"])[0].replace("\"", '')
                    else:
                        if '.csv' in str(a).lower():
                            ext = '.csv'
                        elif '.pdf' in str(a).lower():
                            ext = '.pdf'
                        elif '.xlsx' in str(a).lower():
                            ext = '.xlsx'
                        elif '.xls' in str(a).lower():
                            ext = '.xls'
                        else:
                            ext = '.unknown'
                        name = a["href"].split('/')[-2] + ext
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded file: ' +
                                       str(name))
            except Exception as e:
                module_logger.debug('Porblem downloading: ' +
                                    str(e))
        parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def scrape_ccg(ccg_df):
    ''' master ccg scraping function '''
    print('Working on building a Clinical Comissioning Group Dataset!')
    if os.path.exists(os.path.abspath(
                      os.path.join(__file__, '../..', 'data', 'data_nhsccgs',
                                   'raw'))) is False:
        os.makedirs(os.path.abspath(
                    os.path.join(__file__, '../..', 'data', 'data_nhsccgs',
                                 'raw')))
    ccg_data_path = os.path.abspath(
                    os.path.join(__file__, '../..', 'data', 'data_nhsccgs',
                                 'raw'))
    NHS_AWC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ASH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BARK_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BARNET_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BARNS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BAB_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BED_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BERK_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BEX_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BIRM_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BWD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BOLT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BRAC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BRAD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BREN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BAH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BNSGSG_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BROM_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_BURY_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CALD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CAP_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CAMD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CANT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CPR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CLW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CAH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CWS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_COR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CRAW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_CRO_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_DARL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_DGS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_DONC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_DUD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_DDES_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_EAL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_EANH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ELAR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ERY_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ESTA_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_EASU_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_EACH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ENF_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_FAG_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_GYAW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_GHUD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_GLOU_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_GPRE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_GREE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HALT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HRAW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HAF_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HARI_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HARD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HARR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HAST_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HAR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HAV_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HERE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HERT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HMR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HWLH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HILL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HAMS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HOUN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_HULL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_IAES_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_IOW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ISL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_KERN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_KING_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_KNOW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LAMB_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LEIC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LEWI_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LINE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LINW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LIVE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_LUT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MANC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MAA_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MED_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MERT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MESS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MK_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_MCB_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NENE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NAS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NAG_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NEWH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NORC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NDUR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NEES_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NEHF_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NEL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NK_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NOST_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NWS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NORT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NORW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NOCI_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NNAE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_NW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_OLD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_PORT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_RED_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_ROTH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_RUSH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SAL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SHEF_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SHRO_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SCHE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SEH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SOTE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SOTY_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SWL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SOT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SEND_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SAF_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_STHE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SAS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_STOC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_STOK_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SUN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SD_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SH_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SWAL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_SWIN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_TAG_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_TAW_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_THAN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_THUR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_VOY_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_VOR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_VOR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WAKE_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WALS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WALT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WARR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WC_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WESS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WKEN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WLAN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WLEI_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WL_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WN_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WS_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WAB_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WILT_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WIRR_CCG_scraper(ccg_df, ccg_data_path)
#    NHS_WYRE_CCG_scraper(ccg_df, ccg_data_path)
