"""
    Run this module to download and ingest all data into an elastic cluster.
    Remember to start ES service: sudo systemctl start elasticsearch.service
"""

import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
import shutil
import urllib.request
import requests
import zipfile
from datetime import datetime
from elasticsearch_dsl import (Document, Keyword, Text, Index)
from elasticsearch_dsl.connections import connections
from reconciliation import normalizer
from charity_parser import ImportCC

file_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.normpath(os.path.join(file_path))
data_path = os.path.join(project_path, 'data')
connections.create_connection(hosts=['localhost'])


def get_ch_data(url, path):
    ''' get all companies house data'''
    print('Getting the raw CH data...')
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.text, features="html.parser")
        for a in soup.find_all('a', href=True):
            if 'BasicCompanyDataAsOneFile' in a['href']:
                filename = a['href']
                url = 'http://download.companieshouse.gov.uk/' + filename
                if os.path.exists(os.path.join(path, filename)) is False:
                    with urllib.request.urlopen(url) as response, open(os.path.join(path, filename), 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
    return os.path.join(path, filename)


def get_cc_data(cc_url, outputpath):
    ''' get all charity commission data'''
    print('Getting the raw CC data...')
    r = requests.get(cc_url)
    zip_counter = 0
    list_of_zips = []
    if r.ok:
        soup = BeautifulSoup(r.text, features="html.parser")
        for a in soup.find_all('a', href=True):
            if '.zip' in str(a['href']):
                filename = str(a['href']).split('/')[-1]
                list_of_zips.append(filename)
                zip_counter += 1
                if zip_counter < 4:
                    if os.path.exists(os.path.join(outputpath,
                                                   filename)) is False:
                        with urllib.request.urlopen(a['href']) as response,\
                            open(os.path.join(outputpath,
                                              filename), 'wb') as out_file:
                            shutil.copyfileobj(response, out_file)
                else:
                    break
    ImportCC.import_zip(os.path.join(outputpath, list_of_zips[0]), outputpath)
    return os.path.join(outputpath, 'extract_name.csv')


def grab_nhsdigital_file(url, org_type, path):
    ''' wrapper to get specific types of nhs data'''
    filename = url.split('/')[-1]
    if os.path.exists(os.path.join(path, filename)) is False:
        with urllib.request.urlopen(url) as response,\
             open(os.path.join(path, filename), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    zf = zipfile.ZipFile(os.path.join(path, filename))
    df = pd.read_csv(zf.open(filename.replace('.zip', '.csv')),
                     header=None)
    df['name'] = df.iloc[:, 1]
    df['org_type'] = org_type
    return df[['name', 'org_type']]


def grab_all_nhsdigital(nhs_url, nhsdigital_path):
    ''' master function for getting all types of NHS data'''
    print('Getting the raw NHS data...')
    digital_dict = {'sha': nhs_url+'espha.zip',
                    'csu': nhs_url+'ecsu.zip',
                    'execagency': nhs_url+'eother.zip',
                    'sass': nhs_url+'ensa.zip',
                    'gppra': nhs_url+'epraccur.zip',
                    'nhstrusts': nhs_url+'etr.zip',
                    'caretrusts': nhs_url+'ect.zip',
                    'wlhb': nhs_url+'wlhb.zip',
                    'schools': nhs_url+'eschools.zip',
                    'localauths': nhs_url+'Lauth.zip',
                    'prisons': nhs_url+'eprison.zip'}
    master_df = pd.DataFrame()
    for org_type, url in digital_dict.items():
        master_df = master_df.append(grab_nhsdigital_file(url, org_type,
                                                          nhsdigital_path))
    master_df = master_df.reset_index()
    master_df[['name', 'org_type']].to_csv(os.path.join(nhsdigital_path,
                                                        'all_subdatasets.csv'))
    return os.path.join(nhsdigital_path, 'all_subdatasets.csv')


def make_master_list(datapath, cc_path, ch_path, nhs_path):
    ''' make a master list of the three different types of data'''
    norm_file = os.path.join(datapath, 'data_support', 'norm_dict.tsv')
    norm_df = pd.read_csv(norm_file, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    ch_df = pd.read_csv(ch_path, error_bad_lines=False,
                        usecols=['CompanyName'], index_col=None)
    ch_df = ch_df.rename(columns={"CompanyName": "name"})
    ch_df['name_norm'] = ch_df['name'].apply(lambda x:
                                             normalizer(x, norm_dict))
    pd.DataFrame(ch_df['name'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(ch_path, '..',
                                                        'ch_uniq.csv')))
    pd.DataFrame(ch_df['name_norm'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(ch_path, '..',
                                                        'ch_uniq_norm.csv')))
    cc_df = pd.read_csv(cc_path, error_bad_lines=False,
                        usecols=['name'], index_col=None)
    cc_df['name_norm'] = cc_df['name'].apply(lambda x:
                                             normalizer(x, norm_dict))
    pd.DataFrame(cc_df['name'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(cc_path, '..',
                                                        'cc_uniq.csv')))
    pd.DataFrame(cc_df['name_norm'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(cc_path, '..',
                                                        'cc_uniq_norm.csv')))
    nhs_df = pd.read_csv(nhs_path, error_bad_lines=False,
                         usecols=['name'], index_col=None)
    nhs_df['name_norm'] = nhs_df['name'].apply(lambda x:
                                               normalizer(x, norm_dict))
    pd.DataFrame(nhs_df['name'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(nhs_path, '..',
                                                        'nhs_uniq.csv')))
    pd.DataFrame(nhs_df['name_norm'].
                 drop_duplicates()).to_csv(os.path.abspath(
                                           os.path.join(nhs_path, '..',
                                                        'nhs_uniq_norm.csv')))
    combined_unique_list = list(set(ch_df['name'].tolist() +
                                    cc_df['name'].tolist() +
                                    nhs_df['name'].tolist()))
    df = pd.DataFrame(data={"name": combined_unique_list})
    df = df.sort_values(by=['name'], ascending=True)
    df.to_csv(os.path.join(datapath, 'data_masteringest',
                           'combined_unique_list.csv'), sep=',',
              index=False)
    df_norm = ch_df.append(cc_df).append(nhs_df)
    df_norm['name'] = df_norm['name'].apply(lambda x: normalizer(x, norm_dict))
    df_norm = df_norm[df_norm['name'].notnull()]
    df_norm = df_norm.sort_values(by=['name'], ascending=True)
    df_norm = df_norm.drop_duplicates()
    df_norm.to_csv(os.path.join(datapath, 'data_masteringest',
                                'combined_unique_list_norm.csv'),
                   sep=',', index=False)
    return os.path.join(datapath, 'data_masteringest',
                        'combined_unique_list.csv'),\
        os.path.join(datapath, 'data_masteringest',
                     'combined_unique_list_norm.csv')


class General(Document):
    """Class representing the searchable raw entities"""
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    number = Keyword()

    class Index:
        """The index that all instances of this metadata will be saved to"""
        name = 'general'
        settings = {"number_of_shards": 1, "mapping.ignore_malformed": True}

    def save(self, **kwargs):
        """Saves the current item to the index"""
        return super(General, self).save(**kwargs)


def general_ingest(filepath):
    """Ingest raw list into the cluster"""
    General.init()
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        general = csv.DictReader(csvin, skipinitialspace=True)
        for row in general:
            try:
                for key in row:
                    if not row[key]:
                        row[key] = None
                general = General(name=row['name'])
                general.save()
                row_count += 1
                if (row_count % 1000) == 0:
                    print('{time} Ingested {x}'.format(x=row_count,
                                                       time=datetime.now()))
            except UnicodeDecodeError:
                print('{time} unicode error on row {x}, {name}'.format(
                    time=datetime.now(), x=row_count, name=row['name']))
    print(connections.get_connection().cluster.health())


class General_Norm(Document):
    """Class representing the searchable normalised entities"""
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    number = Keyword()

    class Index:
        """The index that all instances of this metadata will be saved to"""
        name = 'general_norm'
        settings = {"number_of_shards": 1, "mapping.ignore_malformed": True}

    def save(self, **kwargs):
        """Saves the current item to the index"""
        return super(General_Norm, self).save(**kwargs)


def general_norm_ingest(filepath):
    """Ingest normalised list into the cluster"""
    General_Norm.init()
    import time
    time.sleep(2)
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        general_norm = csv.DictReader(csvin, skipinitialspace=True)
        for row in general_norm:
            try:
                for key in row:
                    if not row[key]:
                        row[key] = None
                general_norm = General_Norm(name=row['name'])
                general_norm.save()
                row_count += 1
                if (row_count % 1000) == 0:
                    print('{time} Ingested {x}'.format(x=row_count,
                                                       time=datetime.now()))
            except UnicodeDecodeError:
                print('{time} unicode error on row {x}, {name}'.format(
                    time=datetime.now(), x=row_count, name=row['name']))
    print(connections.get_connection().cluster.health())


def setup_general_index(combi_uni_list_path):
    ''' set up the raw entity index for querying'''
    print("Setting up the 'general' Index")
    i = Index('general')
    i.delete()
    general_ingest(combi_uni_list_path)


def setup_general_norm_index(combi_uni_list_norm_path):
    ''' set up the normalized entity index for querying'''
    print("Setting up the 'general_norm' Index")
    i = Index('general_norm')
    i.delete()
    general_norm_ingest(combi_uni_list_norm_path)


if __name__ == "__main__":
    cc_url = 'http://data.charitycommission.gov.uk/'
    cc_filepath = get_cc_data(cc_url, os.path.abspath(
                              os.path.join('..', 'data', 'data_cc')))
    ch_url = 'http://download.companieshouse.gov.uk/en_output.html'
    ch_filepath = get_ch_data(ch_url, os.path.abspath(
                              os.path.join('..', 'data', 'data_ch')))
    nhs_url = 'https://files.digital.nhs.uk/assets/ods/current/'
    nhs_filepath = grab_all_nhsdigital(nhs_url, os.path.abspath(
                                       os.path.join('..', 'data',
                                                    'data_nhsdigital')))
    raw_path, norm_path = make_master_list(os.path.abspath(
                                           os.path.join('..', 'data')),
                                           cc_filepath, ch_filepath,
                                           nhs_filepath)
    setup_general_index(raw_path)
    setup_general_norm_index(norm_path)
