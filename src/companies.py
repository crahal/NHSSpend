"""
	Run this module to ingest companies house data to an elastic cluster
	Import the companies class to search the cluster and examine company data
"""
import csv
import os
import shutil
import urllib.request
import zipfile
from datetime import datetime
from elasticsearch_dsl import Document, Date, Keyword, Text, InnerDoc, Object, Byte, Nested, Short
from elasticsearch_dsl.connections import connections

file_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.normpath(os.path.join(file_path))
data_path = os.path.join(project_path, 'data')
connections.create_connection(hosts=['localhost'])

class Company(Document):
    """Class representing the searchable companies metadata"""
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    number = Keyword()
    class Index:
        """The index that all instances of this metadata will be saved to"""
        name = 'companies'
        settings = {
            "number_of_shards"        : 2,
            "mapping.ignore_malformed": True,
        }
    def save(self, **kwargs):
        """Saves the current item to the index"""
        # self.lines = len(self.body.split())
        return super(Company, self).save(**kwargs)


def company_count(filepath):
    """Check how many rows to ingest"""
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        companies = csv.reader(csvin)
        for company in companies:
            row_count += 1
    print('{time} Rows to ingest {x}'.format(x=row_count, time=datetime.now()))


def ingest(filepath):
    """Ingest everything in the csv into the cluster"""
    # create the mappings in elasticsearch
    Company.init()
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        companies = csv.DictReader(csvin, skipinitialspace=True)
        for row in companies:
            try:
                for key in row:
                    if not row[key]:
                        row[key] = None
                company = Company(
                    name=row['CompanyName'],
#                    number=row['CompanyNumber']
                    )
                company.save()
                row_count += 1
                if (row_count % 1000) == 0:
                    print('{time} Ingested {x}'.format(x=row_count, time=datetime.now()))
            except UnicodeDecodeError:
                print('{time} unicode error on row {x}, {name}'.format(
                    time=datetime.now(),
                    x=row_count,
                    name=row['CompanyName']))
    print(connections.get_connection().cluster.health())


def setup_company_index(companies_csv_filepath):
    """Download companies house data and ingest it into the companies house index"""
#	companies_zip_filename = companies_file + '.zip'
#	companies_zip_url = download_url + companies_zip_filename
#	companies_zip_filepath = os.path.join(data_path, companies_zip_filename)
#
#	companies_csv_filename = companies_file + '.csv'
#	companies_csv_filepath = os.path.join(data_path, companies_csv_filename)
#
#	if not os.path.isfile(companies_zip_filepath):
#		download(companies_zip_url, companies_zip_filepath)
#	if not os.path.isfile(companies_csv_filepath):
#		unzip(companies_zip_filepath, data_path)
#
    company_count(companies_csv_filepath)
    from elasticsearch_dsl import Index
    i = Index('companies')
    i.delete()
    ingest(companies_csv_filepath)


if __name__ == "__main__":
	setup_company_index('/home/tsl/Dropbox/NHSSpend/data/data_ch/uniq_CH_names_1m_only.csv')
