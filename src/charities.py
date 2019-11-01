"""
	Run this module to download and ingest companies house data to an elastic cluster
	Import the companies class to search the cluster and examine charity data
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


class Charity(Document):
    """Class representing the searchable companies metadata"""
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    number = Keyword()
    class Index:
        """The index that all instances of this metadata will be saved to"""
        name = 'charities'
        settings = {
            "number_of_shards"        : 1,
            "mapping.ignore_malformed": True,
        }
    def save(self, **kwargs):
        """Saves the current item to the index"""
        return super(Charity, self).save(**kwargs)


def charity_count(filepath):
    """Check how many rows to ingest"""
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        charities = csv.reader(csvin)
        for charity in charities:
            row_count += 1
    print('{time} Rows to ingest {x}'.format(x=row_count, time=datetime.now()))


def charity_ingest(filepath):
    """Ingest everything in the csv into the cluster"""
    # create the mappings in elasticsearch
    Charity.init()
    row_count = 0
    with open(filepath, 'r', encoding='utf8') as csvin:
        charities = csv.DictReader(csvin, skipinitialspace=True)
        for row in charities:
            try:
                for key in row:
                    if not row[key]:
                        row[key] = None
                charity = Charity(
                    name=row['name'],#this needs also nameno?
                    number=row['regno'])
                charity.save()
                row_count += 1
                if (row_count % 1000) == 0:
                    print('{time} Ingested {x}'.format(x=row_count, time=datetime.now()))
            except UnicodeDecodeError:
                print('{time} unicode error on row {x}, {name}'.format(
                time=datetime.now(),
                x=row_count,
                name=row['name']))
    print(connections.get_connection().cluster.health())


def setup_charity_index(charities_filepath):
    charity_count(charities_filepath)
    from elasticsearch_dsl import Index
    i = Index('charities')
#    i.delete()
    charity_ingest(charities_filepath)


if __name__ == "__main__":
	setup_charity_index('/home/tsl/Dropbox/NHSSpend/data/data_cc/extract_name.csv')
