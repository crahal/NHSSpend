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


def NHS_AWC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'http://www.airedalewharfedalecravenccg.nhs.uk'
        abrev = 'NHS_AWC_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            list_not_proc = ['/seecmsfile/?id=1251',
                             '/seecmsfile/?id=1368',
                             '/seecmsfile/?id=1368',
                             '/seecmsfile/?id=1251']
            for a in soup.find_all("a", href=True):
                if '/seecmsfile/' in a["href"]:
                    if a["href"] not in list_not_proc:
                        try:
                            r = request_wrapper(base_url + a["href"])
                            name = re.sub(r'\W+', '', a["href"]) + '.csv'
                            if "Content-Disposition" in r.headers.keys():
                                name = re.findall("filename=(.+)",
                                                  r.headers["Content-Disposition"])[0].replace("\"", '')
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Porblem downloading: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ASH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_ASH_CCG'
        base_url = 'https://www.ashfordccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in range(1, 9):
                get_all_files_one_page(url+'p='+str(page), filepath, base_url,
                                       exceptions=['408912.xlsx', '305636.pdf',
                                                   '339282.pdf','339284.pdf',
                                                   '464870.pdf', '462204.pdf',
                                                   '404570.pdf',
                                                   'Contract Log - Ashford (All).xlsx'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_BARK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    '''' all pdfs, wait for pdf parser'''
    try:
        abrev = 'NHS_BARK_CCG'
        base_url = 'http://www.barkingdagenhamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BARNET_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    '''' all pdfs, wait for pdf parser'''
    try:
        abrev = 'NHS_BARNET_CCG'
        base_url = 'http://www.barnetccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BARNS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_BARNS_CCG'
        base_url = 'http://www.barnsleyccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=['02P%202015-2016-03.csv'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BAB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://basildonandbrentwoodccg.nhs.uk'
        abrev = 'NHS_BAB_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
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
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BASS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    abrev = 'NHS_BASS_CCG'
    try:
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.bassetlawccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if 'uploads' in str(a["href"]).lower():
                            r = request_wrapper(base_url+a["href"])
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BANE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_BANE_CCG'
        base_url = 'https://www.bathandnortheastsomersetccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BED_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.bedfordshireccg.nhs.uk/page/'
        abrev = 'NHS_BED_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'downloadFile.php' in a["href"]:
                        try:
                            r = request_wrapper(base_url + a["href"])
                            name = re.sub(r'\W+', '', a["href"]) + '.xlsx'
                            if "Content-Disposition" in r.headers.keys():
                                name = re.findall("filename=(.+)",
                                                  r.headers["Content-Disposition"])[0].replace("\"", '')
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Problem download: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BERK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    '''' all pdfs, wait for pdf parser'''
    try:
        abrev = 'NHS_BERK_CCG'
        base_url = 'https://www.berkshirewestccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BEX_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    '''' mix of various file formats'''
    try:
        abrev = 'NHS_BEX_CCG'
        base_url = 'https://www.bexleyccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['Expenditure%20over%2025k%20July%202016.xls',
                                               'Expenditure%20over%2025k_February%202015.xlsx',
                                               'Expenditure%20over%2025k%20September%202016.xls',
                                               'Expenditure%20over%2025k%20August%202016.xls',
                                               'Expenditure%20over%2025k%20June%202016.xls',
                                               'Expenditure%20over%2025k%20October%202016.xls',
                                               'Expenditure over 25k_July 2013.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BIRM_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.birminghamandsolihullccg.nhs.uk'
        abrev = 'NHS_BIRM_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: '
                                                        + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BWD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_BWD_CCG'
        base_url = 'http://www.barnetccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BLACK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        base_url = 'https://www.fyldecoastccgs.nhs.uk'
        abrev = 'NHS_BLACK_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            list_not_proc = []
            for row in soup.select('tbody')[0]: # CHANGE THIS TO 1 FOR FLYDE
                for a in row.find_all("a", href=True):
                    if (('csv' in a["href"]) or ('xls' in a["href"]) or \
                        ('pdf' in a["href"])):
                        s = request_wrapper(a["href"])
                        soup = BeautifulSoup(s.content, 'lxml')
                        for aaref in soup.find_all("a", href=True):
                            if aaref.text=='Download':
                                t = request_wrapper(aaref['href'])
                                name = str(a['href']).split('/')[-2]
                                if (name.endswith('pdf')) and (name.endswith('.pdf') is False):
                                    name = name+'.pdf'
                                elif (name.endswith('pdf')) and (name.endswith('.xls') is False):
                                    name = name+'.xls'
                                elif (name.endswith('pdf')) and (name.endswith('.xlsx') is False):
                                    name = name+'.xlsx'
                                elif (name.endswith('pdf')) and (name.endswith('.csv') is False):
                                    name = name+'.csv'
                                file = os.path.join(filepath, name)
                                with open(file, "wb") as csvfile:
                                    csvfile.write(t.content)
                                module_logger.info('Downloaded file: ' + str(file))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BOLT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_BOLT_CCG'
        base_url = 'https://www.boltonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BRAC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.bradforddistrictsccg.nhs.uk'
        abrev = 'NHS_BRAC_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            list_not_proc = ['/seecmsfile/?id=305',
                             '/seecmsfile/?id=1250',
                             '/seecmsfile/?id=1251',
                             '/seecmsfileid/?id=295',
                             '/seecmsfileid/?id=297',
                             '/seecmsfileid/?id=279',
                             '/seecmsfileid/?id=285',
                             '/seecmsfileid/?id=280'
                             '/seecmsfile/?id=285',
                             '/seecmsfile/?id=280']
            for a in soup.find_all("a", href=True):
                if '/seecmsfile/' in a["href"]:
                    if a["href"] not in list_not_proc:
                        try:
                            r = request_wrapper(base_url + a["href"])
                            name = re.sub(r'\W+', '', a["href"]) + '.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Porblem downloading: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BRAD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.bradforddistrictsccg.nhs.uk/'
        abrev = 'NHS_BRAD_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
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
                            r = request_wrapper(base_url + a["href"])
                            name = re.sub(r'\W+', '', a["href"]) + '.csv'
                            if (name != 'httpsgcityyhcsorgukseecmsfileid1250.xlsx') or\
                               (name != 'httpsgcityyhcsorgukseecmsfileid1251.xlsx'):
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Porblem downloading: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BREN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' undeclared file extensions
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'http://brentccg.nhs.uk'
        abrev = 'NHS_BREN_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_not_proc = []
            list_downloaded = []
            for split_url in url.split('|'):
                try:
                    r = request_wrapper(split_url)
                    soup = BeautifulSoup(r.content, 'lxml')
                    for a in soup.find_all("a", href=True):
                        if '25k' in a["href"]:
                            if (a["href"] not in list_not_proc) and\
                               ('tmpl=component' not in a["href"]) and\
                               (a['href'] not in list_downloaded):
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a['data-title'] + '.' + a.text.strip()
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BAH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' have to parse title properly for extension
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.brightonandhoveccg.nhs.uk'
        abrev = 'NHS_BAH_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_not_proc = ['downloadtokenttVIW7pA.xlsx',
                             'downloadtokenjmiA7Qz.xlsx']
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if 'download?token=' in a["href"]:
                    if a["href"] not in list_not_proc:
                        try:
                            r = request_wrapper(base_url + a["href"])
                            if 'officedocument' in a["type"]:
                                ext = '.xlsx'
                            elif 'csv' in a["type"]:
                                ext = '.csv'
                            name = a.text
                            with open(os.path.join(filepath, name+ext),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Porblem downloading: ' + str(e))
        if scrape is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BNSSG_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' have to iterate into each field'''
    try:
        base_url = 'https://bnssgccg.nhs.uk'
        search_url = '/search/?y=0&query=spend+over+25k&category=reports&x=0&page='
        abrev = 'NHS_BNSGSG_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(1, 4):
                r = request_wrapper(base_url + search_url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if '/library/' in a["href"]:
                        get_all_files_one_page(base_url+a["href"], filepath)
        if parse is True:
            try:
                os.remove(os.path.join(filepath, 'FOI_1920055_-_Final_Response.pdf'))
                os.remove(os.path.join(filepath, 'FOI_1920174_-_Final_Response.pdf'))
                os.remove(os.path.join(filepath, 'FOI_1920211_-_Final_Response.pdf'))
                os.remove(os.path.join(filepath, 'FOI_1920247_-_Final_Response.pdf'))
                os.remove(os.path.join(filepath, 'north_som_ccg_annual_report_2016-17.pdf'))
            except:
                pass
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BUCK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_BUCK_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BROM_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' have to iterate into each field'''
    try:
        base_url = 'https://www.bromleyccg.nhs.uk'
        abrev = 'NHS_BROM_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('/expenditure-reports/' in a["href"]) and\
                   (a["href"] != '/expenditure-reports/') and\
                   (a["href"] != url):
                    get_all_files_one_page(base_url + a["href"], filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_BURY_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    '''' note! currently www.bury.nhs.uk is down so ignore log errors'''
    try:
        abrev = 'NHS_BURY_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CALD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CALD_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            got_this = []
            for a in soup.find_all("a", href=True):
                if '/download/expenditure' in a["href"]:
                    r = request_wrapper(a["href"])
                    soup = BeautifulSoup(r.content, 'lxml')
                    for b in soup.find_all("a", href=True):
                        if ('/download/expenditure' in b["href"]) and\
                           (b["href"] not in got_this):
                            r = request_wrapper(b["href"])
                            name = b["href"].split('/')[-1]
                            name = re.sub(r'\W+', '', name) + '.pdf'
                            got_this.append(name)
                            with open(os.path.join(filepath, name), "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' + str(name))
            get_all_files_one_page(url, filepath)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAP_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CAP_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            base_url = 'https://www.cambridgeshireandpeterboroughccg.nhs.uk'
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if '/easysiteweb/getresource' in a["href"]:
                    r = request_wrapper(base_url + a["href"])
                    name = a.text
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                    module_logger.info('Downloaded file: ' + str(name))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAMD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CAMD_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            base_url = 'http://www.camdenccg.nhs.uk'
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=['NHS-Camden-CCG-Expenditure-over-30k-January-2016.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CANN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' not yet written'''
    try:
        abrev = 'NHS_CANN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.cannockchaseccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('/file' in a["href"]) and ('25k' in a["href"]):
                        try:
                            r = request_wrapper(base_url + a["href"])
                            if "data-title" in r.headers.keys():
                                name = a["data-title"]
                            else:
                                name = a["href"].split('/')[-2]
                            name = name + '.' + a['data-extension']
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                        except Exception as e:
                                module_logger.debug('Problem downloading: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CANT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CANT_CCG'
        base_url = 'https://www.canterburycoastalccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in range(1, 9):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if a.has_attr('title'):
                        if 'expenditure' in a["title"].lower():
                            r = request_wrapper(base_url + a["href"])
                            name = a["href"].split('/')[-1]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                    csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + name)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CPR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CPR_CCG'
        base_url = 'https://castlepointandrochfordccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r =request_wrapper(base_url + a["href"])
                                    name = a["title"].replace(' ', '%20')
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CLW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CLW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.centrallondonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CSR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CSR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.chorleysouthribbleccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_CAH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' seems clean (all pdfs), should update automatically,
        last updated: 1st May 2019
    '''
    try:
        abrev = 'NHS_CAH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.cityandhackneyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CWS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' seems clean, should update automatically,
        last updated: 1st May 2019 '''
    try:
        abrev = 'NHS_CWS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.coastalwestsussexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            os.rename(os.path.join(filepath, '09G_May15.csv'),
                      os.path.join(filepath, '09G_May15.tsv'))
            os.rename(os.path.join(filepath, '09G_Aug_2015.csv'),
                      os.path.join(filepath, '09G_Aug_2015.tsv'))
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_COR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    try:
        abrev = 'NHS_COR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.corbyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['03V Over 25k report Oct 17.pdf',
                                               '03V A3131. Expenditure Over Threshold MONTH 8 reviewed 26.2.18.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CAR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_CAR_CCG'
        if scrape is True: # for consistency
            print('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CRAW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    abrev = 'NHS_CRAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.crawleyccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(1, 16):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if a.has_attr('title'):
                        if '25k' in a["title"].lower():
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name = a["title"].replace(' ', '%20').lower()
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_CRO_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    try:
        abrev = 'NHS_CRO_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.croydonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            excluded = ['2017%2008%20Expenditure%20over%2025k.xlsx']
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('expenditure' in a["href"].lower()) and\
                   (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                    try:
                        r = request_wrapper(base_url+a["href"])
                        name = a["href"].split('/')[-1].replace(' ', '%20')
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Bad DL?: '
                                            + str(name) + ':' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DARL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    try:
        abrev = 'NHS_DARL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = ''
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            excluded = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('25k' in a["href"].lower()) and\
                   (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                    try:
                        r = request_wrapper(base_url+a["href"])
                        name = a["href"].split('/')[-1].replace(' ', '%20')
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Bad DL?: ' + a["href"] + ':' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DGS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DGS_CCG'
        url = get_url(ccg_df, abrev)
        base_url='https://www.dartfordgraveshamswanleyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DAD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DAD_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.derbyandderbyshireccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DEV_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DEV_CCG'
        if scrape is True:
            print('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DONC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DONC_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.doncasterccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DORS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DORS_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DUD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' need to fiddle with a search of the anchor text
        should update automatically,
        last updated: 1st May 2019
    '''
    try:
        abrev = 'NHS_DUD_CCG'
        url = get_url(ccg_df, abrev)
        base_url = ''
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            excluded = ['Dudley-CCG-Spend-Over-£25k-July-2015.csv']  # 404
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('25k' in a.text.lower()) and\
                   (a["href"].split('/')[-1].replace(' ', '%20') not in excluded):
                    try:
                        r = request_wrapper(base_url+a["href"])
                        name = a["href"].split('/')[-1].replace(' ', '%20')
                        with open(os.path.join(filepath, name), "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Bad DL?: ' + a["href"] + ':' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_DDES_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_DDES_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EAL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EAL_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            base_url = 'https://www.ealingccg.nhs.uk/'
            for page in range(1, 8):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('25k' in a["href"].lower()) and\
                       ('spend' in a["href"].lower()):
                        try:
                            r = request_wrapper(base_url+a["href"])
                            name = a["href"].split('/')[-1].replace(' ', '%20')
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded: ' + str(name))
                        except Exception as e:
                            module_logger.debug('Bad DL?: ' + a["href"] +
                                                ':' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EANH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EANH_CCG'
        base_url = 'https://www.enhertsccg.nhs.uk'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, url, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EBERK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EBERK_CCG'
        base_url = 'https://www.eastberkshireccg.nhs.uk'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=['Appendix-1-Refreshed-CCGs-Commissioning-Intentions-2018-19.pdf',
                                                   'LBBOS-Web.pdf',
                                                   'BA-December-2013.pdf',
                                                   'Bulletin-6.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EALA_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EALA_CCG'
        base_url = 'https://eastlancsccg.nhs.uk'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if ('25k' in a["href"].lower()):
                    try:
                        r = request_wrapper(base_url + a["href"])
                        name = a["href"].split('/')[-1] + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Porblem downloading: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ELAR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_ELAR_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath,
                                   exceptions=['1.2-Privacy-Notice-NHS-ELRCCG-August-2018-FINAL-ELR-Corporate-047-FINAL.pdf',
                                               'Payments-over-£25k-August-2015.xlsx',
                                               'Payments-over-25k-August-18.xlsx',
                                               'Payments-over-£25k-July-2015.xlsx',
                                               'Payments-over-25k-–-March-2018-1.xlsx',
                                               'Payments-over-25k-–-February-2018-1.xlsx',
                                               'Doc-22_PPN_0316_-_Publication_of_payment_performance_statistics__1_.pdf',
                                               'Doc-23_BPPC-Data-Published-re-PPN-17-18-1.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_ERY_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_ERY_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath,)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ESTA_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_ESTA_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://eaststaffsccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(2013, 2021):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('/file' in a["href"]) and ('25k' in a["href"]):
                        try:
                            r = request_wrapper(base_url + a["href"])
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EASU_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EASU_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.eastsurreyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(0, 6):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('.csv' in a["href"]) or ('.xls' in a["href"]):
                        try:
                            r = request_wrapper(base_url + a["href"])
                            name = re.findall("filename=(.+)",
                                              r.headers["Content-Disposition"])[0].replace("\"", '')
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' + str(name))
                        except Exception as e:
                                module_logger.debug('Porblem downloading: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EHF_CLR_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' not yet written'''
    module_logger.debug('NHS_EHF_CCG_scraper still to be written')


def NHS_EACH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EACH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.eastcheshire.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_EHS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_EHS_CCG'
        if scrape is True:
            print('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ENF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_ENF_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.enfieldccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['Clinical and non-clinical procurement corporate governance and strategic framework.pdf',
                                               'NHS-Enfield-CCG- procurement-checklist-Single-offer.pdf',
                                               'Primary care urgent access procurement decision.pdf',
                                               'Register of procurement decisions - Updated November 2019.pdf',
                                               'Seven Day Primary Care Access Service - procurement checklist.pdf',
                                               'Walk-in centre service procurement decision.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_FAG_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_FAG_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.farehamandgosportccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_FW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        base_url = 'https://www.fyldecoastccgs.nhs.uk'
        abrev = 'NHS_FW_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        url = get_url(ccg_df, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            list_not_proc = []
            for row in soup.select('tbody')[0]: # CHANGE THIS TO 1 FOR FLYDE, 0 FOR BLACK
                for a in row.find_all("a", href=True):
                    if (('csv' in a["href"]) or ('xls' in a["href"]) or \
                        ('pdf' in a["href"])):
                        s = request_wrapper(a["href"])
                        soup = BeautifulSoup(s.content, 'lxml')
                        for aaref in soup.find_all("a", href=True):
                            if aaref.text=='Download':
                                t = r = request_wrapper(aaref['href'])
                                name = str(a['href']).split('/')[-2]
                                if (name.endswith('pdf')) and (name.endswith('.pdf') is False):
                                    name = name+'.pdf'
                                elif (name.endswith('pdf')) and (name.endswith('.xls') is False):
                                    name = name+'.xls'
                                elif (name.endswith('pdf')) and (name.endswith('.xlsx') is False):
                                    name = name+'.xlsx'
                                elif (name.endswith('pdf')) and (name.endswith('.csv') is False):
                                    name = name+'.csv'
                                file = os.path.join(filepath, name)
                                with open(file, "wb") as csvfile:
                                    csvfile.write(t.content)
                                module_logger.info('Downloaded file: ' + str(file))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GLOU_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_GLOU_CCG'
        url = get_url(ccg_df, abrev)
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath,
            exceptions=['Contracts-Website-16-17.docx',
                        'Declarations-of-Interest-Register_Live-1.pdf',
                        'Hospitality-and-Gifts-Register_15.xls',
                        'AI-10-1-August-2016-IGQC-Risk-Register-App-1.xlsx',
                        'Penalties-Q1-sanctions-M3-final.pdf',
                        'Q2-sanctions-final.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GHUD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_GHUD_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.greaterhuddersfieldccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GYAW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_GYAW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.greatyarmouthandwaveneyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GPRE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_GPRE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.greaterprestonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GREE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_GREE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.greenwichccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_GAW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        exceptions = ['130531-09N_A3131_Expenditure_Over_Threshold_AP_MAY_GWCCG.pdf',
                      '130630-09N_A3131_Expenditure_Over_Threshold_AP_JUN_GWCCG.pdf',
                      '130731-09N_A3131_Expenditure_Over_Threshold_AP_JUL_GWCCG.pdf',
                      '130831-09N_A3131_Expenditure_Over_Threshold_AP_AUG_GWCCG.pdf',
                      '130930-09N_A3131_Expenditure_Over_Threshold_AP_SEP_GWCCG.pdf',
                      '131121-09N_A3131_Expenditure_Over_Threshold_AP_OCT_GWCCG.pdf',
                      '140102-09N_A3131_Expenditure_Over_Threshold_AP_NOV_GWCCG.pdf',
                      '140126-09N_A3131_Expenditure_Over_Threshold_AP_JAN_2013_GWCCG.pdf',
                      '140127-CCG_Service_Providers_Contracts_2013-14.pdf',
                      '140117-09N_A3131_Expenditure_Over_Threshold_AP_DEC2013_GWCCG.pdf',
                      '140318-09N_A3131_Expenditure_Over_Threshold_AP_FEB14_GWCCG.pdf',
                      '140415-Francis_Report_Response_GWCCG_Final.pdf',
                      '140430-09N_A3131_Expenditure_Over_Threshold_AP_Apr14_GWCCG.pdf',
                      '140515-09N_A3131_Expenditure_Over_Threshold_AP_MAR14_GWCCG.pdf',
                      '140626-09N_A3131_Expenditure_Over_Threshold_AP_May14_GWCCG.pdf',
                      '140711-Strategic_Plan_2014-15_to_2018-19_GWCCG.pdf',
                      '140717-09N_A3131_Expenditure_Over_Threshold_AP_Jun14_GWCCG.pdf',
                      '140821-CCG_Service_Provider_Contracts_2014-15.pdf',
                      '140910-09N_A3131_Expenditure_Over_Threshold_AP_Jul14_GWCCG.pdf',
                      '141020-09N_A3131_Expenditure_Over_Threshold_AP_Aug14_GWCCG.pdf',
                      '141020-09N_A3131_Expenditure_Over_Threshold_AP_Sep14_GWCCG.pdf',
                      '141128-09N_A3131_Expenditure_Over_Threshold_AP_Oct14_GWCCG.pdf',
                      '150102-09N_A3131_Expenditure_Over_Threshold_AP_Nov14_GWCCG.pdf',
                      '150130-09N_A3131_Expenditure_Over_Threshold_AP_Dec14_GWCCG.pdf',
                      '150226-09N_A3131_Expenditure_Over_Threshold_AP_Jan15_GWCCG.pdf',
                      '150331-09N_A3131_Expenditure_Over_Threshold_AP_Feb15_GWCCG.pdf',
                      '150430-09N_A3131_Expenditure_Over_Threshold_AP_Mar15_GWCCG.pdf',
                      '151016-NHSGWCCG_Anti-Bribery_Statement_GWCCG.pdf',
                      '151212-CCG_Service_Provider_Contracts_2015-16_GWCCG.pdf',
                      '161021-CCG_Service_Provider_Contracts_2016-17_GWCCG.pdf',
                      '161021-Gifts_Hospitality_Register_2015-16_GWCCG.pdf',
                      '170807-Gifts_Hospitality_Register_2016-17_75-105_GWCCG.pdf',
                      '171120-CCG_Service_Provider_Contracts_2017-18_GWCCG.pdf',
                      '180103-Gifts_Hospitality_Register_2017-18_106-113_GWCCG.pdf',
                      '180906-Gifts_Hospitality_Register_2017-18_114-127_GWCCG.pdf',
                      '181003-Clare_Stone_Biography_v1.pdf',
                      '181003-Dr_Justine_Hall_Biography_v1_2.pdf',
                      '181003-Dr_Susan_Tresman_Biography_v3.pdf',
                      '181003-GWCCG_Annual_Audit_Letter_2017-18_KPMG_GWCCG.pdf',
                      '181107-Fair_Processing_Notice_rev_Nov2018_GWCCG.pdf',
                      '181212-CCG_Service_Provider_Contracts_2018-19_GWCCG.pdf',
                      '181212-Gifts_Hospitality_Register_2018-19_128-134_GWCCG.pdf',
                      '181214-Procurement_Decisions_Contracts_Awarded_Register_rev_Sep18_GWCCG.pdf',
                      '190116-Practice_Staff_Register_of_Interest_2018-19_GWCCG.pdf',
                      '190122-Phelim_Brady_Biography_v3_1.pdf',
                      '190123-Debbie_Stubberfield_Biography_v1_1.pdf',
                      '190123-Dr_Darren_Watts_Biography_v2_2.pdf',
                      '190123-Dr_Sian_Jones_Biography_v2_1.pdf',
                      '190123-Elaine_Newton_Biography_v3_1.pdf',
                      '190123-Jacqueline_Burke_Biography_v2_1.pdf',
                      '190123-Jonathan_Perkins_Biography_v1_1.pdf',
                      '190123-Julia_Dutchman-Bailey_Biography_v1_1.pdf',
                      '190123-Karen_McDowell_Biography_v4_1.pdf',
                      '190123-Matthew_Tait_Biography_v1_1.pdf',
                      '190123-Peter_Collis_Biography_v1_1.pdf',
                      '190123-Sumona_Chatterjee_Biography_v1_1.pdf',
                      '190123-Vicky_Stobbart_Biography_v3_1.pdf',
                      '190227-09N_A3131_Expenditure_Over_Threshold_AP_Jan19_GWCCG.pdf',
                      '190301-09N_A3131_Expenditure_Over_Threshold_AP_Feb19_GWCCG.pdf',
                      '190401-09N_A3131_Expenditure_Over_Threshold_AP_Mar19_GWCCG.pdf',
                      '190618-GWCCG_Annual_Audit_Letter_2018-19_KPMG_GWCCG.pdf',
                      '190815-Mark_Byrne_Biography_v1_0.pdf',
                      '191130-Gifts_Hospitality_Register_2019-20_137-142_GWCCG.pdf',
                      '191209-Vicky_Stobbart_Biography_v4_0.pdf',
                      '191230-Privacy_Notice_GP_Practice_Data_Population_Health_CCG_1_1_SH_CCGs.pdf',
                      'My%20Surgery%20Website%20Service%20Terms%20and%20Conditions.pdf',
                      'My%20Surgery%20Website%20Site%20Terms%20and%20Conditions.pdf',
                      '191101-CCG_Staff_Register_Interests_Band_8A_2019-20_GWCCG.pdf',
                      '191101-CCG_Staff_Register_Interests_Band_8A_2019-20_GWCCG.pdf.csv',
                      'My%20Surgery%20Website%20Service%20Terms%20and%20Conditions.pdf',
                      'My%20Surgery%20Website%20Site%20Terms%20and%20Conditions.pdf']
        abrev = 'NHS_GAW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.guildfordandwaverleyccg.nhs.uk/website'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=exceptions)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_HALT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HALT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.haltonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HRAW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HRAW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hambletonrichmondshireandwhitbyccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                time.sleep(5) # this website seems slow\janky
                try:
                    get_all_files_one_page(page_url, filepath, base_url,
                                           exceptions=['AfC_tc_of_service_handbook_fb.pdf',
                                                       'ccg-model-cons-framework_version-3.2-oct-2015.pdf'])
                except:
                    module_logger.debug(abrev + ' doesnt work for ' + page_url)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAF_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hammersmithfulhamccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url,
                                       exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HARI_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HARI_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.haringeyccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HARD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HARD_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.harrogateandruraldistrictccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=['spend-over-25k-june18.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HARR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HARR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://harrowccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAST_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAST_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hartlepoolandstocktonccg.nhs.uk/'
        if scrape is True:
            createdir(ccg_data_path, abrev)
            filepath = os.path.join(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hastingsandrotherccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in range(1, 15):
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAV_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAV_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.haveringccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HERE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HERE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.herefordshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_HERT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HERT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://hillingdonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if ('spend' in str(a).lower()) and ('http' in str(a["href"])):
                    try:
                        r = request_wrapper(a["href"])
                        name = a.text
                        with open(os.path.join(filepath, abrev + '_' + name + '.xlsx'),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
                    except Exception as e:
                        module_logger.debug('Problem download: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HMR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HMR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hmr.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HWLH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HWLH_CCG'
        if scrape is True:
            print('Working on ' + abrev + '.')
            filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HILL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HILL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://hillingdonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            counter = 0
            for page in url.split('|'):
                r = request_wrapper(page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    for ext in ['.csv', '.xls', '.pdf']:
                        if ext in a["href"]:
                            counter = counter + 1
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name = abrev + '_' + str(counter) + ext
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' + str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HAMS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HAMS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.horshamandmidsussexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in range(1, 16):
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            os.remove(os.path.join(filepath, '09X_CCG_Annual_Report_2016-17_FINAL WEBSITE.pdf'))
            os.remove(os.path.join(filepath, '23.2 b HMSCCG Annual Audit Letter.pdf'))
            os.remove(os.path.join(filepath, 'AGM 2015 Q&As_FINAL.pdf'))
            os.remove(os.path.join(filepath, 'AGM Joint CCG Pres_2016_All For Website.pdf'))
            os.remove(os.path.join(filepath, 'AGM Joint CCG Pres_2017 v10.pdf'))
            os.remove(os.path.join(filepath, 'AGM Joint CCG Presentation_2015_FINAL.pdf'))
            os.remove(os.path.join(filepath, 'AGM slides - final.pdf'))
            os.remove(os.path.join(filepath, 'CS45510_summary_report_04_web.pdf'))
            os.remove(os.path.join(filepath, 'Horsham and Mid Sussex Annual Report and Accounts 14-15 (for Web).pdf'))
            os.remove(os.path.join(filepath, 'Horsham and Mid Sussex Annual Report and Accounts 2013-14.pdf'))
            os.remove(os.path.join(filepath, 'Newsletter July-August 19.pdf'))
            os.remove(os.path.join(filepath, '1.4 2018 Briefing paper Final SASH AEDB MRET READ RE April 2018.pdf'))
            os.remove(os.path.join(filepath, 'Horsham and Mid Sussex CCG Fines and Penalties (at Feb-16).pdf'))
            os.remove(os.path.join(filepath, 'Horsham Annual Report Summary 2015.pdf'))
            os.remove(os.path.join(filepath, 'Horsham Annual Review Summary 2016_FINAL.pdf'))
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_HOUN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HOUN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.hounslowccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_HULL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_HULL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.ipswichandeastsuffolkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['ccg-governance-framework-and-financial-regs-v4-apr-17.pdf',
                                                                        'ce-annual-report-2017-18-final-version.pdf',
                                                                        'comms-and-engagement-strategy.pdf',
                                                                        'GP-List-2019-with-websites.pdf',
                                                                        'gp-practice-list-hull-august-2017-1.pdf',
                                                                        'individual-funding-request-policy-final-september-2018.pdf',
                                                                        'jargon-buster-october-2017.pdf.csv',
                                                                        'the-nhs-structure-and-ccg.pdf',
                                                                        'jargon-buster-october-2017.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_IAES_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_IAES_CCG'
        base_url = 'http://www.ipswichandeastsuffolkccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if 'expenditure report' in a.text.lower():
                    r = request_wrapper(base_url + a["href"])
                    name = ''.join(ch for ch in a.text if ch.isalnum())+'.pdf'
                    with open(os.path.join(filepath, name),
                              "wb") as csvfile:
                        csvfile.write(r.content)
                    module_logger.info('Downloaded file: ' + name)
        try:
            if parse is True:
                os.remove(os.remove(os.path.join(ccg_data_path, abrev, 'Monthlyexpenditurereportover25kFebruary2020.pdf.csv')))
                parse_wrapper(ccg_data_path, filepath, abrev)
        except Exception as e:
            module_logger.debug(abrev + ' has a parsing error: ' + str(e))
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_IOW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_IOW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.isleofwightccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ISL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_ISL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.islingtonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
            os.remove(os.path.join(filepath, '2001-NHS-Islington-CCG-Expenditure-over-30k-January-2020.pdf'))
            os.remove(os.path.join(filepath, '2014-15-NHS-Islington-CCG-Expenditure-over-25k-April-2014-March-2015.pdf'))
            os.remove(os.path.join(filepath, '2015-16-NHS-Islington-CCG-Expenditure-over-30k-April-2015-March-2016.pdf'))
            os.remove(os.path.join(filepath, '2016-17-NHS-Islington-CCG-Expenditure-over-30k-April-2016-March-2017.pdf'))
            os.remove(os.path.join(filepath, '2017-18-NHS-Islington-CCG-Expenditure-over-30k-April-2017-March-2018.pdf'))
            os.remove(os.path.join(filepath, '2018-19-NHS-Islington-CCG-Expenditure-over-30k-April-2018-March-2019.pdf'))
            os.remove(os.path.join(filepath, 'FOI Disclosure Log.xlsx.xls'))
            os.remove(os.path.join(filepath, 'ICCG%20Constitution.pdf'))
            os.remove(os.path.join(filepath, 'Islington%20CCG%20Prospectus%202013.pdf'))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_KERN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_KERN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.kernowccg.nhs.uk/'
        module_logger.debug('Now working on: ' + str(abrev))
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_KING_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_KING_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.kingstonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_KNOW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_KNOW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://knowsleyccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_LAMB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LAMB_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_LEE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LEE_CCG'
        base_url = 'https://www.leedsccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in range(1, 21):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('expenditure' in a["href"].lower()) and ('page=' not in a["href"]):
                        get_all_files_one_page(a["href"], filepath, base_url, exceptions=[])
    #                        name = a["href"].split('/')[-1]
    #                        with open(os.path.join(filepath, name),
    #                                  "wb") as csvfile:
    #                                csvfile.write(r.content)
    #                        module_logger.info('Downloaded file: ' + name)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LEIC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LEIC_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.leicestercityccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                    exceptions=['Commissioning-Strategy-v20.1.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LEWI_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LEWI_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.lewishamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LINE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LINE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://lincolnshireeastccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_LINW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LINW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.lincolnshirewestccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            get_all_files_one_page(url[:-5], filepath,
                                   base_url, exceptions=[])
            for pagenumber in range(2, 10):
                get_all_files_one_page(url+str(pagenumber)+'/', filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LIVE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LIVE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.liverpoolccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in range(2013, 2021):
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LUT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LUT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.lutonccg.nhs.uk/page/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page_url in url.split('|'):
                r = request_wrapper(page_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if 'download' in str(a["href"]):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
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
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MANC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MANC_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://manchesterccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MAA_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MAA_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.mansfieldandashfieldccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in ['201920', '201819', '201718', '201617', '201516']:
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MED_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MED_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.medwayccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page_url in url.split('|'):
                r = request_wrapper(page_url)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if any(ext in a["href"] for ext in ['.csv', '.xls',
                                                        '.pdf', '.ods',
                                                        '.xlsx']):
                        if a.text not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name_file = a.text.strip()
                                if len(name_file)>0:
                                    with open(os.path.join(filepath, name_file),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name_file))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MERT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MERT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.mertonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
            dont_delete = ['01 -', '02 -', '03 -', '04 -', '05 -', '06 -',
                           '07 -', '08 -', '09 -', '10 -', '11 -', '12 -']
            for subdir, dirs, files in os.walk(filepath):
                for file in files:
                    if file[0:4] not in dont_delete:
                        os.remove(os.path.join(filepath, file))
            #print os.path.join(subdir, file)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MESS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MESS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://midessexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        list_to_ignore = []
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in ['2013-14-archive-1', '2014-15-archive-1', '2015-16',
                         '2016-17', '2017-18', '2018-19', '2019-2020']:
                r = request_wrapper(url + page)
                soup = BeautifulSoup(r.content, 'lxml')
                for table in soup.findAll('table'):
                    for a in table.find_all("a"):
                        if '25k' in a["href"]:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name = str(a["href"]).split("/")[-2]+'.csv'
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_MK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MK_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://midessexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            exceptions = ['04F Over Â£25k Report Oct 17.pdf',
                          '04F Over 25k Report - M10 18 02.02.18.pdf']
            for a in soup.find_all("a"):
                if '25' in a.text:
                    try:
                        if 'http:' in a["href"]:
                            r = request_wrapper(a["href"])
                        else:
                            r = request_wrapper(base_url+a["href"])
                        if 'content-disposition' in r.headers.keys():
                            name = r.headers['content-disposition'].split('=')[1].replace('"','')
                            if name not in exceptions:
                                with open(os.path.join(filepath, name), "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        module_logger.debug('Problem download: ' + str(e))
        if parse is True:
            os.remove(os.path.join(filepath, '04F Over Â£25k Report Oct 17.csv'))
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('The entire thing fails: ' + str(e))


def NHS_MCB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_MCB_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.morecambebayccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if a.has_attr('title'):
                    if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                         '.pdf', '.ods',
                                                         '.xlsx']):
                        if a["title"] not in list_to_ignore:
                            try:
                                r = request_wrapper(base_url + a["href"])
                                name = a["title"]
                                with open(os.path.join(filepath, name),
                                          "wb") as csvfile:
                                    csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                            except Exception as e:
                                module_logger.debug('Problem download: ' +
                                                    str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NENE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NENE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.neneccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in range(2016, 2022):
                get_all_files_one_page(url+str(pagenumber)+'.htm', filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NAS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NAS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.newarkandsherwoodccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        # needs updating over time to be more flexible
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for pagenumber in ['201920', '201819', '201718', '201617', '201516']:
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NAG_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NAG_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.newcastlegatesheadccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NEWH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NEWH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.newhamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['2016-17-NHS-Newham-CCG-Expenditure-over-30k.pdf',
                                               '2015-16-NHS-Newham-CCG-Expenditure-over-30k.pdf',
                                               '2017-18-NHS-Newham-CCG-Expenditure-over-30k.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NORC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NORC_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NDUR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NDUR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://northdurhamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NEES_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NEES_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.neessexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
            for subdir, dirs, files in os.walk(filepath):
                for file in files:
                    if file.endswith('.pdf'):
                        os.remove(os.path.join(filepath, file))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NEHF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NEHF_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_NEL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NEL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northeastlincolnshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_NH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northhampshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page_url in url.split('|'):
                get_all_files_one_page(page_url, filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NK_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northkirkleesccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://northlincolnshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['reimbursement-of-expenses.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northnorfolkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_NT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northtynesideccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_NOST_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NOST_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northstaffsccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in ['2013', '2014-1', '2015-1',
                         '2016-2', '2017-1', '2018', '2019']:
                r = request_wrapper(url + page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url + a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NWS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    abrev = 'NHS_NWS_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.nwsurreyccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in ['2014', '2015', '2016',
                         '2017', '2018-4', '2018', '2019']:
                r = request_wrapper(url + page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url + a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NORT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NORT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.northumberlandccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NORW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.norwichccg.nhs.uk/'
        abrev = 'NHS_NORW_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['0', '20', '40', '60', '80', '100', '120', '140']:
                r = request_wrapper(url + page)
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    soup = BeautifulSoup(r.content, 'lxml')
                                    for a in soup.find_all("a"):
                                        if ("/about-us/spending-over-25-000/" in a["href"]) and ("/file" in a["href"]):
                                            if 'pdf' in a["data-title"].lower():
                                                ext = '.pdf'
                                            elif 'csv' in a["data-title"].lower():
                                                ext = '.csv'
                                            elif 'xls ' in a["data-title"].lower():
                                                ext = '.xls'
                                            elif 'xlsx' in a["data-title"].lower():
                                                ext = '.xlsx'
                                            name = a["data-title"]+ext
                                            r = request_wrapper(base_url + a["href"])
                                            with open(os.path.join(filepath, name),
                                                  "wb") as csvfile:
                                                csvfile.write(r.content)
                                            module_logger.info('Downloaded file: ' +
                                                               str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: ' +
                                                        str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NOCI_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NOCI_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.nottinghamcity.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NNAE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NNAE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.nottinghamnortheastccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['FOI-Disclosure-Log-2014-15.pdf',
                                                                        'FOI-REPORT-2013-14-for-website.pdf',
                                                                        'NNE-CCC-FOI-REPORT-2015-16.pdf',
                                                                        'NNE-CCG-FOI-REPORT-2016-17.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_NW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_NW_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.nottinghamwestccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_OLD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_OLD_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.oldhamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_OXFO_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_OXFO_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.oxfordshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(1, 91, 10):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('invoices-paid' in a["href"]) and \
                       ('about-us' not in a["href"]):
                        get_all_files_one_page(base_url+a["href"], filepath,
                                               base_url,
                                               exceptions=['directions-to-jubilee-house.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_PORT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_PORT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.portsmouthccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            # needs updating over time to be more flexible
            for pagenumber in ['201920', '201819', '2017',
                               '2016', '2015', '2018', '2014']:
                get_all_files_one_page(url+str(pagenumber)+'.htm', filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RED_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_RED_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.redbridgeccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RAB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_RAB_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.redditchandbromsgroveccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                for a in soup.find_all("a", href=True):
                    if ('/EasySiteWeb/GatewayLink.aspx?' in a["href"]):
                        r = request_wrapper(base_url + a["href"])
                        name = a.text+'.csv'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
            except Exception as e:
                module_logger.debug('Problem downloading: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_RICH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_RICH_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_ROTH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_ROTH_CCG'
        base_url = 'http://www.rotherhamccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_RUSH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_RUSH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.rushcliffeccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for pagenumber in ['1355', '4925', '4693', '4344',
                               '3487', '2757', '3902', '3890']:
                get_all_files_one_page(url+str(pagenumber), filepath,
                                       base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.salfordccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in range(1, 10):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                try:
                    for a in soup.find_all("a", href=True):
                        if ('25k' in str(a.text).lower()):
                            r = request_wrapper(a["href"])
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_SCAR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SCAR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.sheffieldccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_SHEF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SHEF_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.sheffieldccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SHRO_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SHRO_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.shropshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOME_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SOME_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SCHE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SCHE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.southcheshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        list_to_ignore = []
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(1, 10):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    if ('expenditure' in str(a.text).lower()):
                        r = request_wrapper(base_url+a["href"])
                        if 'pdf' in r.headers['Content-Type']:
                            name = a.text.replace('\n','').replace(' ','') + '.pdf'
                        else:
                            name = a.text.replace('\n','').replace(' ','') + '.xlsx'
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SESASP_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SESASP_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SEH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_SEH_CCG'
        base_url = 'https://www.southeasternhampshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_SKC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    abrev = 'NHS_SKC_CCG'
    base_url = 'https://www.southkentcoastccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    if scrape is True:
        createdir(ccg_data_path, abrev)
        url = get_url(ccg_df, abrev)
        exceptions_list = ['17.pdf',
                           '2015_2016 Annual Report v20 WEBSITE VERSION.pdf',
                           'NHS-TCS-2019-pay-poster.pdf',
                           'afc_tc_of_service_handbook_fb.pdf',
                           'SKC Annual Report 14_15 FINAL - Signed and published on web site.pdf',
                           'SKC Annual Report Summary V3 .pdf']
        for page in range(0, 6):
            get_all_files_one_page(url + str(page), filepath, base_url,
                                   exceptions=[])
        for file in exceptions_list:
            os.remove(os.path.join(filepath, file))
    if parse is True:
        parse_wrapper(ccg_data_path, filepath, abrev)

def NHS_SL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://southlincolnshireccg.nhs.uk/'
        abrev = 'NHS_SL_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in range(2013, 2021):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: '
                                                        + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_SN_CCG'
        base_url = 'https://www.southnorfolkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url,
                                       exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_SS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.southseftonccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOTE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SOTE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.southteesccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['NHS-South-Tees-CCG-Payments-Over-25k-November-2017.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOTY_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SOTY_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.southtynesideccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWAR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWAR_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWOR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        base_url = 'https://southwestlincolnshireccg.nhs.uk/'
        abrev = 'NHS_SWOR_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['spend-over-25k-2020', 'spend-over-25k-2019',
                         'spend-over-25k-2018', '2017', '2016', '2015',
                         '2014', '2013']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"].lower() for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + a["href"])
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: '
                                                        + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://southwestlincolnshireccg.nhs.uk/'
        abrev = 'NHS_SWL_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['spend-over-25k-2019', 'spend-over-25k-2018',
                         '2017', '2016', '2015', '2014', '2013']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"]))
                                    name = a["title"]
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                    module_logger.info('Downloaded file: ' +
                                                       str(name))
                                except Exception as e:
                                    module_logger.debug('Problem download: '
                                                        + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SOT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.southamptoncityccg.nhs.uk/'
        abrev = 'NHS_SOT_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['422', '423', '425', '451', '484', '874', '874', '969']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["href"] for ext in ['.csv', '.xls',
                                                            '.pdf', '.ods',
                                                            '.xlsx']):
                            if a.text not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"]))
                                    name = a.text + '.pdf'
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SEND_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://southendccg.nhs.uk/'
        abrev = 'NHS_SEND_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['2013-14-archive', '2014-15-archive' '201516archive',
                         '2016-17-archive', '2017-18-archive', '2018-19',
                         '2019-20']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"]))
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAF_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.southportandformbyccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWARK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWARK_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.southwarkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['NHS Southwark CCG Bribery Statement.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_STHE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_STHE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.sthelensccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    base_url = 'https://www.staffordsurroundsccg.nhs.uk/'
    abrev = 'NHS_SAS_CCG'
    filepath = os.path.join(ccg_data_path, abrev)
    try:
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['2013-2', '2014-2', '2015-2', '2016',
                         '2017', '2018-2', '2019-2']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                r = request_wrapper(base_url + str(a["href"]))
                                name = a["title"]
                                soup = BeautifulSoup(r.content, 'lxml')
                                for a in soup.find_all("a"):
                                    if ('news-events/publications/expenditure/' in a["href"]) and\
                                       ('/file' in a["href"]):
                                        r = request_wrapper(base_url + str(a["href"]))
                                        if 'xlsx' in str(a):
                                            ext = '.xlsx'
                                        elif 'xls' in str(a):
                                            ext = '.xls'
                                        elif 'csv' in str(a):
                                            ext = '.csv'
                                        elif 'pdf' in str(a):
                                            ext = '.pdf'
                                        else:
                                            ext = '.unknown'
                                        name = a['data-title'] + ext
                                        with open(os.path.join(filepath, name),
                                                  "wb") as csvfile:
                                            csvfile.write(r.content)
                                        module_logger.info('Downloaded file: ' +
                                                       str(name))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_STOC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_STOC_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.stockportccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a"):
                if '25' in a.text:
                    try:
                        if 'http:' in a["href"]:
                            r = request_wrapper(a["href"])
                        else:
                            r = request_wrapper(base_url+a["href"])
                        if 'content-disposition' in r.headers.keys():
                            name = r.headers['content-disposition'].split('=')[1].replace('"','')
                            name = name.replace(';','')
                            with open(os.path.join(filepath, name), "wb") as csvfile:
                                csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                    except Exception as e:
                        module_logger.debug('Problem download: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_STOK_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.stokeccg.nhs.uk/'
        abrev = 'NHS_STOK_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = ['Copy-of-Stoke-on-Trent-CCG-Spend-over-25k-oct-2015.pdf']
            for page in ['2013-14-reports', '2014-reports', '2015-reports',
                         '2016-reports', '2017-reports', '2018-1', '2019-1',
                         '2020-1']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"]))
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SUN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SUN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.sunderlandccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SD_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, possibly need to
        add more files in the list_not_proc
        last updated: Monday 29th April 2019
    '''
    try:
        base_url = 'https://www.surreydownsccg.nhs.uk/'
        abrev = 'NHS_SD_CCG'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            list_to_ignore = []
            for page in ['2013', '2014', '2015', '2016', '2017',
                         '2018', '2019-1', '2020-1']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a"):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            if a["title"] not in list_to_ignore:
                                try:
                                    r = request_wrapper(base_url + str(a["href"]))
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.surreyheathccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in range(2013, 2021):
                r = request_wrapper(url + str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if ('25k' in str(a["title"]).lower()):
                            r = request_wrapper(base_url+a["href"])
                            name = a.text.replace('\n', '').replace(' ', '') + '.csv'
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SUTT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SUTT_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SAWB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SAWB_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWAL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWAL_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.swaleccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_SWIN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_SWIN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.swindonccg.nhs.uk/about-us/transparency-agenda'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if a.has_attr('title'):
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"]+'/file')
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                except Exception as e:
                    module_logger.debug('Download failed for: ' + str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TAG_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_TAG_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.tamesideandglossopccg.org/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if '25k' in str(a["href"]).lower():
                        r = request_wrapper(base_url+a["href"])
                        name = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0].replace("\"", '')
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                            module_logger.info('Downloaded file: ' +
                                               str(name))
                except Exception as e:
                    pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TAW_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    abrev = 'NHS_TAW_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://www.telfordccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in ['2013-1', '2014-1', '2015-2',
                         '2017-2', '2018-2', '2019-5']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_THAN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    abrev = 'NHS_THAN_CCG'
    base_url = 'https://www.thanetccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    if scrape is True:
        createdir(ccg_data_path, abrev)
        url = get_url(ccg_df, abrev)
        for page in range(0, 5):
            get_all_files_one_page(url + str(page), filepath, base_url,
                                   exceptions=['afc_tc_of_service_handbook_fb.pdf',
                                               'NHS-TCS-2019-pay-poster.pdf',
                                               '10E Thanet Annual Report Final Combined with Final Accounts.pdf'])
    if parse is True:
        parse_wrapper(ccg_data_path, filepath, abrev)


def NHS_THUR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    abrev = 'NHS_THUR_CCG'
    url = get_url(ccg_df, abrev)
    base_url = 'https://thurrockccg.nhs.uk/'
    filepath = os.path.join(ccg_data_path, abrev)
    list_to_ignore = []
    try:
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in ['2019-20', '2018-19', '2017-18', '2016-17',
                         '2015-16', '2013-14-1', '2013-14']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug('Something went badly wrong here: ' + str(e))


def NHS_TH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_TH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.towerhamletsccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            exceptions = ['1.5 Minutes for May Part 1.pdf',
                          '1.6 Minutes for March Part 1.pdf',
                          '13_05_07-Governing-body-papers-combinedv3.pdf',
                          '13_05_07-Minutes-of-previous-meeting.pdf',
                          '13_07_02 CCG Governing Body papers.pdf',
                          '13_07_02 Minutes of previous meeting.pdf',
                          '13_09_03 Governing Body papers.pdf',
                          '13_09_03 Minutes of previous meeting.pdf',
                          '13_11_05 Governing Body papers combined2.pdf',
                          '13_11_05  Minutes of previous meeting.pdf',
                          '14-07-01-GB-minutes-part I.pdf',
                          '14-09-02-draft-minutes-of-meeting-PartI-v2.pdf',
                          '14-09-02-Governing-body-papers.pdf',
                          '14-11-04-GB-minutes.pdf',
                          '14-11-04-Governing-Body-papers.pdf',
                          '14_01_07 governing body papers.pdf',
                          '14_01_07 Minutes of previous meeting.pdf',
                          '14_03_04 Governing Body papersv3.pdf',
                          '14_05_06-Governing-body-papers-v2.pdf',
                          '14_05_06 Minutes of previous meeting.pdf',
                          '14_07_01 GB part I combined_ipad2.pdf',
                          '15-01-27-Approved-minutes-of-meeting.pdf',
                          '15-01-27-Governing-Body-part-I.pdf',
                          '15-03-03-Approved-minutes-of-meeting-Part-I.pdf',
                          '15-03-03-Governing-body-part-1-v2.pdf',
                          '15-05-05-Approved-minutes-of meeting.pdf',
                          '15-05-05-Governing-body-part-1.pdf',
                          '15-07-07-Approved-minutes-of-meeting.pdf',
                          '15-07-07-GB-v2.pdf',
                          '15-09-01-Approved-minutes-of-meeting.pdf',
                          '15-09-01-Governing-body-part1.pdf',
                          '15-11-03-Governing-body-part-1.pdf',
                          '16-01-26-Governing-body-papers-part-1.pdf',
                          '16-03-01-Approved-minutes-of-meeting.pdf',
                          '16-03-01-Governing-body-meeting.pdf',
                          '16-05-03-Governing-body-minutes.pdf',
                          '16-05-03-Governing-body-papers-part-1.pdf',
                          '16-07-05-Approved-Minutes-of-meeting.pdf',
                          '16-07-05-Governing-body-papers-2.pdf',
                          '16-11-01-Approved-minutes.pdf',
                          '16-11-01-Governing-body-papers-part-1.pdf',
                          '17-01-24-Approved-minutes-V1.pdf',
                          '17-01-24-Governing-body-meeting-part-1.pdf',
                          '17-03-07-Governing-body-meeting-1.1.pdf',
                          'All Saints External Patient Consultation report.pdf',
                          'Annual Report Statutory Accounts 201819.pdf',
                          'Governing Body Part 1 Combined Papers 28.05.2019.pdf',
                          'KPMG-annual-audit-letter-2015-16.pdf',
                          'KPMG-Annual-audit-letter-2013-14.pdf',
                          'KPMG-Annual-audit-letter-2014-15.pdf',
                          'KPMG-Annual-audit-letter-2016-17.pdf',
                          'Minutes for September Part 1 - APPROVED.pdf',
                          'NEL-CCGs-IFR-Policy-2014-17.pdf',
                          'NEL EBI 2019-2020 v1.1.pdf',
                          'NEL EBI You Said We Did.pdf',
                          'NHS-Constitution.pdf',
                          'NHS-THCCG-360-stakeholder-survey-2017.pdf',
                          'NHS-TH-CCG-Annual-report-and-accounts-2016-17-V6.pdf',
                          'NHS-THCCG-Annual-report-and-accounts-2015-16.pdf',
                          'NHS-THCCG-Annual-report-and-accounts-2017-18-final.pdf',
                          'NHS-THCCG-CG4-Incident-reporting-policy-and-procedure.pdf',
                          'NHS-THCCG-CG0004-Working-with-pharmacy.pdf',
                          'NHS-THCCG-CG6-Gifts-and-hospitality-policy-v2-August-2013.pdf',
                          'NHS-THCCG-CG0044-Whistleblowing-policy-v0d6-Sept-2013.pdf',
                          'NHS-THCCG-Clinical-procurement-corporate-governance-strategic-framework-2015-16.pdf',
                          'NHS-THCCG-Commissioning-intentions-2017-19.pdf',
                          'NHS-THCCG-Constitution-v5d3-revised-210616.pdf',
                          'NHS-THCCG-Equality-and-Diversity-Strategy-2016-2020.pdf',
                          'NHS-TH-CCG-Fertility-policy-December-2014.pdf',
                          'NHS-THCCG-FI2-Procurement-strategy-v6.pdf',
                          'NHS-THCCG-IG9-Information-governance-strategy-November-2015.pdf',
                          'NHS-THCCG-Patient-and-Public-Involvement-Strategy-updated-2015-18.pdf',
                          'NHS-THCCG-PPI-Report-2015-16.pdf',
                          'NHS-THCCG-Prospectus-2013-v8.pdf',
                          'NHS-THCCG-Q134-Safeguarding-for-adults-policy-April-2013.pdf',
                          'NHS-THCCG-Quality-in-general-practice-strategy-2014-15-2016-17.pdf',
                          'NHS-Tower-Hamlets-CCG-Annual-report-2013-14-V8.pdf',
                          'NHS-Tower-Hamlets-CCG-auditor-2017-2020.pdf',
                          'NHS-Tower-Hamlets-Exec-Annual-Report-2014-15-V7.pdf',
                          'NHS-Tower-Hamlets-Service-user-and-carer-incentive-policy-2016.pdf',
                          'Part I Governing Body Papers - 24th July 2018.pdf',
                          'THCCG-GB-papers-part-1-2-July-2019.pdf',
                          'THCCG-GC3-Conflict-of-interest-policy-December-2016-v3.P.pdf',
                          'THCCG Governing Body 22 May Part 1 Papers.pdf',
                          'THCCG Governing Body Meeting 26th September 2017 Papers FINAL.pdf',
                          'THCCG Governing Body Papers 23rd Jan v2.pdf',
                          'THCCG Governing Body Papers  Part 1 27th March 2018 v1.pdf',
                          'THCCG Governing Body Papers Part 1 25th July V2.pdf',
                          'THCCG Governing Body Papers Part I 10th May 2017 V2.pdf',
                          'THCCG Governing Body Part 1 Papers 22nd Jan.pdf',
                          'THCCG Part 1 25th September Papers 2018.pdf',
                          'THCCG Part 1 Papers.pdf',
                          'THCCG Part 1 Papers 26th March 2019.pdf',
                          'THCCG-Q133-Safeguarding-through-commissioning-policy-January-2016.pdf',
                          'THT Vision v7.pdf',
                          'WELC-PoLCV-2014-15-2015-16.pdf',
                          'WEL DS  Appendix A.pdf']
            get_all_files_one_page(url, filepath, base_url, exceptions=exceptions)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_TRAF_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_TRAF_CCG'
        base_url = 'https://www.traffordccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in range(2013, 2021):
                new_url = url.replace('YYYY', str(page))
                get_all_files_one_page(new_url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_VOY_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_VOY_CCG'
        base_url = 'https://www.valeofyorkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                if '/seecmsfile/' in a["href"]:
                    r = request_wrapper(a["href"])
                    name = a["href"][-5:] + '.csv'
                    with open(os.path.join(filepath, name), "wb") as csvfile:
                        csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' + str(name))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_VOR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_VOR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.valeroyalccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in range(0, 10):
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if 'uploads' in str(a["href"]).lower():
                            r = request_wrapper(base_url+a["href"])
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
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WAKE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WAKE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.wakefieldccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WALS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WALS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://walsallccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(2013, 2020):
                get_all_files_one_page(url+str(page)+'-publications',
                                       filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WALT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WALT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.walthamforestccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            exceptions = ['Annual_Audit_Letter_2013_14.pdf',
                          'Annual_Audit_Letter_2015_16.pdf',
                          'Annual_Audit_Letter_2016_17.pdf',
                          'Annual_Audit_Letter_2017_18.pdf',
                          'Annual_Audit_Letter_2018_19.pdf',
                          'Bengali-Personal-Health-Budgets-leaflet-October-2014.pdf',
                          'Diabetes XPERT flyer A5.pdf',
                          'Enc 4 2 B Report on MH Strategy Consultation.pdf',
                          'Equality and Diversity Strategy 2013-2107.pdf',
                          'Healthier-Together-Winter-2019-2020.pdf',
                          'Introduction-to-Personal-Health-Budgets-leaflet-August-2014.pdf',
                          'Joint Children and Adults Autism Strategy 2013-15.pdf',
                          'Joint Dementia Care Strategy 2010-2015.pdf',
                          'LBWF-MPS-registered-care-market-July-2016.pdf',
                          'NELCA-Safeguarding-through-commissioning-Policy.pdf',
                          'NEL EBI 2019-2020 v1.1.pdf',
                          'NEL EBI You Said We Did.pdf',
                          'NEL-Evidence-Based-Interventions-Policy.pdf',
                          'NEL-Primary-Care-Strategy.pdf',
                          'NHS-Waltam-Forest-CCG-Complaints-policy-.pdf',
                          'NHS-Waltham-Forest-CCG-Annual-audit-letter-2014-15.pdf',
                          'NHS Waltham Forest CCG Annual Report 2013-14.pdf',
                          'NHS_Waltham_Forest_CCG_Annual_Report_2016-17.pdf',
                          'NHS_Waltham_Forest_CCG_Annual_Report_2017_18.pdf',
                          'NHS-Waltham-Forest-CCG-Annual-report-and-accounts-2015-16.pdf',
                          'NHS Waltham Forest CCG - Annual Report and Accounts 2014-15.pdf',
                          'NHS-Waltham-Forest-CCG-Anti-fraud-policy-December-2015.pdf',
                          'NHS-Waltham-Forest-CCG-CHC-protocol-policy-v16-2015.pdf',
                          'NHS-Waltham-Forest-CCG-Communications-strategy-2015-18.pdf',
                          'NHS-Waltham-Forest-CCG-Community-participation-strategy-2015-18.pdf',
                          'NHS-Waltham-Forest-CCG-Confidentiality-and-disclosure-of-information-policy-October-2015-v3.pdf',
                          'NHS-Waltham-Forest-CCG-End-of-Life-Care-Strategic-Framework-June-2015.pdf',
                          'NHS-Waltham-Forest-CCG-EPRR-policy-November-2016.pdf',
                          'NHS-Waltham-Forest-CCG-Falls-Prevention-and-Bone-Health-Strategy-May-2015.pdf',
                          'NHS-Waltham-Forest-CCG-FAQ-Personal-Health-Budgets-adults-December-2015.pdf',
                          'NHS-Waltham-Forest-CCG-FAQ-Personal-Health-Budgets-children-and-young-people-December-2015.pdf',
                          'NHS_Waltham_Forest_CCG_GP_member_practices_April_2017.pdf',
                          'NHS-Waltham-Forest-CCG-Information-governance-strategy-October-2015-v4.pdf',
                          'NHS-Waltham-Forest-CCG-Mobile-devices-policy-April-2014-Final.pdf',
                          'NHS-Waltham-Forest-CCG-Publications-scheme.pdf',
                          'NHS-Waltham-Forest-CCG-Standards-of-business-conduct-Conflicts-of-interest-policy-v5.pdf',
                          'NHS-Waltham-Forest-Procurement-strategy-for-commissioning-framework-July-2015.pdf',
                          'NHS-WF-CCG-Business-continuity-plan-August-2017.pdf',
                          'NHS-WF-CCG-CSP-2016-17-2019-20.pdf',
                          'NHS-WF-CCG-Fertility-policy-final-2018.pdf',
                          'NHS-WF-CCG-Safeguarding-declaration-statement.pdf',
                          'NHS-WF-CCG-Whistleblowing-policy-February-2017.pdf',
                          'Polish-Personal-Health-Budgets-leaflet-October-2014.pdf',
                          'Prescribing_recommendations_for_medication.pdf',
                          'Prescribing_recommendations_for_medicines_used_in_children.pdf',
                          'Primary_Care_Strategy.pdf',
                          'Quality_and_Patient_Safety_Strategy.pdf',
                          'Safefeguarding-adult-policy.pdf',
                          'Scheme of delegation and waiver authorisation FINAL.pdf',
                          'Suicide Prevention Strategy for Waltham Forest 2013-16.pdf',
                          'Summary of independent review - WF CCG Aug 2019.pdf',
                          'TST information leaflet.pdf',
                          'Turkish-Personal-Health-Budget-leaflet-October-2014.pdf',
                          'Urdu-Personal-Health-Budgets-leaflet-August-2014.pdf',
                          'Waltham Forest CCG Calendar Email and Internet Policy_v4_March 2019.pdf',
                          'Waltham Forest CCG IG Policy Final v4_ March 2019.pdf',
                          'Waltham Forest CCG Information Management Policy_ March 2019.pdf',
                          'Waltham Forest CCG IT Strategy.pdf',
                          'Waltham Forest CCG Non-medical Prescribing Policy.pdf',
                          'Waltham-Forest-Mental-health-and-well-being-directory-October-2015.pdf',
                          'Waltham Forest Patient Prospectus.pdf',
                          'WELC-CCGs-Procedures-not-routinely-funded-2014-16-22-September-2015.pdf',
                          'WEL_Slavery_Human_Trafficking_Statement_2019-2020.pdf',
                          'WF-CAMHS-Transformation-Plan-Refresh-2019.pdf',
                          'WFCCG-AnnualReport2018-19 May.pdf',
                          'WFCCG constitution.pdf',
                          'WFCCG-list-of-attendees-Governing-body-Committee-meetings-2014-15.pdf',
                          'WFCCG-Safeguarding-children-policy-and-procedures-2016-19.pdf',
                          'WFCEPN_Annual_Report_2016-17.pdf',
                          'WF Information Quality Policy_March 2019.pdf',
                          'Workforce_Race_Equality_Standard_2018_19.pdf']
            get_all_files_one_page(url, filepath, base_url, exceptions=exceptions)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WAND_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WAND_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))



def NHS_WARR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WARR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.warringtonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['15 16_AcuteContracts.pdf',
                                                                        '15 16_CareHomeContracts.pdf',
                                                                        '15 16_CommunityContracts.pdf',
                                                                        '15 16_DiagnosticContracts.pdf',
                                                                        '15 16_GPContracts.pdf',
                                                                        '15 16_MentalHealthContracts.pdf',
                                                                        '15 16_PalliativeContracts.pdf',
                                                                        '16.17_AllContracts.pdf',
                                                                        '15 16_ThirdSectorContracts.pdf',
                                                                        '201819 All Contracts.xlsx',
                                                                        'All contracts 1718.pdf',
                                                                        'All Contracts 2015-16 amended.pdf',
                                                                        'Copy of 2019 2020_All Contract Values_v2.xlsx'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WARN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' not yet written'''
    try:
        abrev = 'NHS_WARN_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WC_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WC_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.westcheshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WESS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WESS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://westessexccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in ['2012-1', '2013-1', '2014-1', '2015-1', '2016-2',
                         '2017-2', '2018-1', '2019-1', '2020-1']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WHAM_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WHAM_CCG'
        module_logger.info('Working on ' + abrev + '.')
        filepath = os.path.join(ccg_data_path, abrev)
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WKEN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WKEN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.westkentccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            for page in range(1, 9):
                get_all_files_one_page(url+str(page),
                                       filepath, base_url, exceptions=['16) 130423 Commissioning Plan.pdf',
                                                                       '85.18%20ii%20Annual%20Audit%20Letter%20-%20WKCCG%202017-18.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WLAN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WLAN_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.westlancashireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WLEI_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WLEI_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.westleicestershireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in ['2013', '2014', '2015', '2016',
                         '2017', '2018', '2019-1']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"])
                            name = a["title"]
                            with open(os.path.join(filepath, name),
                                      "wb") as csvfile:
                                csvfile.write(r.content)
                                module_logger.info('Downloaded file: ' +
                                                   str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WL_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_WL_CCG'
        base_url = 'https://www.westlondonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['Annual-Accounts-2016-17-v2.pdf',
                                               'Annual-report-2016-web.pdf',
                                               'Annual-report-2017-lowres.pdf',
                                               'ANNUAL-REPORT-2017_18.pdf',
                                               'Y56_RKL_Annual-Accounts-201516.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WN_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    ''' should update automatically, maybe increase the range or add
        more exclusions etc (and check for other filetypes
        last updated: Monday 29th April 2019
    '''
    try:
        abrev = 'NHS_WN_CCG'
        base_url = 'https://www.westnorfolkccg.nhs.uk'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            url = get_url(ccg_df, abrev)
            for page in url.split('|'):
                get_all_files_one_page(page, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WS_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WS_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.westsuffolkccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=[])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WAB_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WAB_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.wiganboroughccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        list_to_ignore = []
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if 'phocadownload' in str(a["href"]).lower():
                        r = request_wrapper(base_url+a["href"])
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WILT_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WILT_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.wiltshireccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url, exceptions=['Final-1.pdf',
                                                                        'Sanc_Q3_1415.pdf',
                                                                        'Sanc_Q4_1415.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WIRR_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WIRR_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.wirralccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            get_all_files_one_page(url, filepath, base_url,
                                   exceptions=['final-5-year-strategic-plan-14-to-19.pdf',
                                               'final-ccg-governance-handbook-february-2020.pdf',
                                               'master-ccg-constitution-v110-january-2020.pdf',
                                               'wirral_ccg1.pdf',
                                               'wirral_ccg-2016-1.pdf'])
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))

def NHS_WOLV_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WOLV_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://wolverhamptonccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            list_to_ignore = []
            for page in ['2013-14', '2014-15', '2015-16', '2016-17',
                         '2017-18', '2018-19', '2019-20']:
                r = request_wrapper(url+str(page))
                soup = BeautifulSoup(r.content, 'lxml')
                for a in soup.find_all("a", href=True):
                    try:
                        if any(ext in a["title"] for ext in ['.csv', '.xls',
                                                             '.pdf', '.ods',
                                                             '.xlsx']):
                            r = request_wrapper(base_url+a["href"])
                            soup = BeautifulSoup(r.content, 'lxml')
                            for a in soup.find_all("a", href=True):
                                if '/file' in a["href"]:
                                    r = request_wrapper(base_url+a["href"])
                                    name = a["data-title"] + a["data-extension"] + '.pdf'
                                    with open(os.path.join(filepath, name),
                                              "wb") as csvfile:
                                        csvfile.write(r.content)
                                        module_logger.info('Downloaded file: ' +
                                                           str(name))
                    except Exception as e:
                        pass
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_WYRE_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_WYRE_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'http://www.wyreforestccg.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if ('25k' in str(a["title"]).lower()) or ('exp' in str(a["title"]).lower()):
                        r = request_wrapper(base_url + a["href"])
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
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def NHS_LUH_CCG_scraper(ccg_df, ccg_data_path, scrape, parse):
    try:
        abrev = 'NHS_LUH_CCG'
        url = get_url(ccg_df, abrev)
        base_url = 'https://www.rlbuht.nhs.uk/'
        filepath = os.path.join(ccg_data_path, abrev)
        if scrape is True:
            createdir(ccg_data_path, abrev)
            r = request_wrapper(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for a in soup.find_all("a", href=True):
                try:
                    if ('upload' in str(a["title"]).lower()):
                        r = request_wrapper(base_url + a["href"])
                        if "Content-Disposition" in r.headers.keys():
                            name = re.findall("filename=(.+)",
                                              r.headers["Content-Disposition"])[0].replace("\"", '')
                        else:
                            name = a["href"].split('/')[-1]
                        with open(os.path.join(filepath, name),
                                  "wb") as csvfile:
                            csvfile.write(r.content)
                        module_logger.info('Downloaded file: ' +
                                           str(name))
                except Exception as e:
                    module_logger.debug('Porblem downloading: ' +
                                        str(e))
        if parse is True:
            parse_wrapper(ccg_data_path, filepath, abrev)
    except Exception as e:
        module_logger.debug(abrev + ' fails entirely: ' + str(e))


def scrape_ccg(ccg_df, scrape, parse):
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
    for scraper in ccg_df['abrev'].tolist()[138:139]:
#        try:
        globals()[scraper+'_scraper'](ccg_df, ccg_data_path, scrape, parse)
#        except Exception as e:
#            module_logger.debug(str(scraper) + ' fails at the globals() level.')
