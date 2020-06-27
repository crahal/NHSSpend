import requests
import time
import traceback
import os
import ntpath
import re
from bs4 import BeautifulSoup
import logging
import shutil
module_logger = logging.getLogger('nhsspend_application')


def createdir(filepath, institution):
    ''' check if the necessary subdirectory, and if not, make it'''
    shutil.rmtree(os.path.join(filepath, institution))
    os.makedirs(os.path.join(filepath, institution))
    print('Working on ' + institution + '.')
    module_logger.info('Working on ' + institution + '.')


def get_url(df, abrev):
    df = df[df['abrev'] == abrev]
    url = df['url'].tolist()[0]
    return url


def request_wrapper(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, verify=True)
    except requests.exceptions.SSLError:
        r = requests.get(url, headers=headers, verify=False)
        module_logger.warn('Bad SSL certs for: ' + str(url))
    return r


def get_all_files_one_page(loading_url, filepath, base_url='', exceptions=[]):
    r = request_wrapper(loading_url)
    try:
        counter = 0
        soup = BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all("a", href=True):
            if not any(x in a["href"] for x in ['.csv',
                                                '.xls',
                                                '.xlsx',
                                                '.ods',
                                                '.pdf']):
                continue
            name = a["href"].rsplit('/', 1)[-1]
            if ('.csv' in a["href"]) and (a["href"].endswith('.csv') is False):
                name = name + '.csv'
            elif ('.xlsx' in a["href"]) and (a["href"].endswith('.xlsx') is False):
                name = name + '.xlsx'
            elif ('.xls' in a["href"]) and (a["href"].endswith('.xls') is False):
                name = name + '.xls'
            elif ('.pdf' in a["href"]) and (a["href"].endswith('.pdf') is False):
                name = name + '.pdf'
            name = str(counter) + '_' + name
            temp = a["href"].replace(' ', '%20').replace('../', '')
            if name not in exceptions:
                time.sleep(.5)
                if 'http' in temp:
                    r = request_wrapper(temp)
                else:
                    r = request_wrapper(base_url + temp)
                if "Content-Disposition" in r.headers.keys():
                    name = str(counter) + '_' + re.findall("filename=(.+)",
                        r.headers["Content-Disposition"])[0].replace("\"", '')
                if name not in exceptions:
                    if os.path.exists(os.path.join(filepath, name.split('.')[0]+'.csv')) is False and \
                       os.path.exists(os.path.join(filepath, name.split('.')[0]+'.xlsx')) is False and \
                       os.path.exists(os.path.join(filepath, name.split('.')[0]+'.xls')) is False:
                        with open(os.path.join(filepath, name.lower()), "wb") as csvfile:
                            csvfile.write(r.content)
                            counter = counter+1
                        module_logger.info('Downloaded file: ' + str(name))
    except Exception:
        module_logger.debug('Problem downloading: ' +
                            traceback.format_exc())


def get_data(datalocations, filepath, abrev, exclusions=[]):
    ''' send data.gov.uk or gov.uk data through here. '''
    for datalocation in datalocations:
        r = requests.get(datalocation)
        listcsvs = []
        listxls = []
        listxlsx = []
        listods = []
        soup = BeautifulSoup(r.content, 'lxml')
        for link in soup.find_all("a", href=True):
            if link.get('href').lower().endswith('.csv'):
                if 'data.gov.uk' in datalocation:
                    listcsvs.append(link.get('href'))
                else:
                    listcsvs.append('https://www.gov.uk/' + link.get('href'))
            elif link.get('href').lower().endswith('.xlsx'):
                if 'data.gov.uk' in datalocation:
                    listxlsx.append(link.get('href'))
                else:
                    listxlsx.append('https://www.gov.uk/' + link.get('href'))
            elif link.get('href').lower().endswith('.xls'):
                if 'data.gov.uk' in datalocation:
                    listxls.append(link.get('href'))
                else:
                    listxls.append('https://www.gov.uk/' + link.get('href'))
            elif link.get('href').lower().endswith('.ods'):
                if 'data.gov.uk' in datalocation:
                    listods.append(link.get('href'))
                else:
                    listods.append('https://www.gov.uk/' + link.get('href'))
        if len([listcsvs, listxls, listxlsx, listods]) > 0:
            for filelocation in set(sum([listcsvs, listxls,
                                         listxlsx, listods], [])):
                if 'https://assets' in filelocation:
                    filelocation = filelocation.replace(
                        'https://www.gov.uk/', '')
                try:
                    breakout = 0
                    for exclusion in exclusions:
                        if exclusion in str(filelocation):
                            module_logger.info(
                                os.path.basename(filelocation) +
                                ' is excluded! Verified problem.')
                            breakout = 1
                    if breakout == 1:
                        continue
                except Exception as e:
                    module_logger.debug(os.path.basename(filelocation) +
                                        ' exclusion problem.' + str(e))
                    pass
                filename = os.path.basename(
                    filelocation).replace('?', '').lower()
                while filename[0].isalpha() is False:
                    filename = filename[1:]
                if ('gpc' not in filename.lower()) \
                        and ('procurement' not in filename.lower()) \
                        and ('card' not in filename.lower()):
                    if os.path.exists(os.path.join(filepath, abrev,
                                                   filename)) is False:
                        try:
                            r = requests.get(filelocation)
                            module_logger.info('File downloaded: ' +
                                               ntpath.basename(filelocation))
                            with open(os.path.join(
                                      os.path.join(filepath, abrev),
                                      filename), "wb") as csvfile:
                                csvfile.write(r.content)
                        except Exception as e:
                            module_logger.debug('Problem downloading ' +
                                                ntpath.basename(filelocation) +
                                                ': ' + str(e))
