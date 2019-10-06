"""
	Run this module to download and ingest companies house data to an elastic cluster
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

# Download and file paths
# TODO Directory objects?
file_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.normpath(os.path.join(file_path))
data_path = os.path.join(project_path, 'data')

download_url = 'http://download.companieshouse.gov.uk/'

connections.create_connection(hosts=['localhost'])


class Address(InnerDoc):
	"""Class representing an Address field"""
	care_of = Text(fields={'raw': Keyword()})
	po_box = Text(fields={'raw': Keyword()})
	line1 = Text(fields={'raw': Keyword()})
	line2 = Text(fields={'raw': Keyword()})
	town = Text(fields={'raw': Keyword()})
	county = Text(fields={'raw': Keyword()})
	country = Text(fields={'raw': Keyword()})
	post_code = Text(fields={'raw': Keyword()})


class Accounts(InnerDoc):
	"""Class representing an accounts field"""
	ref_day = Byte()
	ref_month = Byte()
	next_due = Date(format='dd/MM/yyyy')
	last_made_up = Date(format='dd/MM/yyyy')
	category = Keyword()


class Returns(InnerDoc):
	"""Class representing a returns field"""
	next_due = Date(format='dd/MM/yyyy')
	last_made_up = Date(format='dd/MM/yyyy')


class Mortgages(InnerDoc):
	"""Class representing a mortgage field"""
	charges = Short()
	outstanding = Short()
	part_satisfied = Short()
	satisfied = Short()


class LimitedPartnerships(InnerDoc):
	"""Class representing a limited partnerships field"""
	general_partners = Short()
	limited_partners = Short()


class PreviousName(InnerDoc):
	"""Class representing a previous name field"""
	company_name = Text(analyzer='snowball', fields={'raw': Keyword()})
	date = Date(format='dd/MM/yyyy')


class Company(Document):
	"""Class representing the searchable companies metadata"""
	name = Text(analyzer='snowball', fields={'raw': Keyword()})
	number = Keyword()
	registered_address = Object(Address)
	category = Keyword()
	status = Keyword()
	country_of_origin = Keyword()
	dissolution = Date(format='dd/MM/yyyy')
	incorporation = Date(format='dd/MM/yyyy')

	accounts = Object(Accounts)
	returns = Object(Returns)
	mortgages = Object(Mortgages)
	SIC_code = [
		Text(analyzer='snowball', fields={'raw': Keyword()}),
		Text(analyzer='snowball', fields={'raw': Keyword()}),
		Text(analyzer='snowball', fields={'raw': Keyword()}),
		Text(analyzer='snowball', fields={'raw': Keyword()})
	]
	limited_partnerships = Object(LimitedPartnerships)
	URI = Keyword()
	previous_name = Nested(PreviousName)
	confirmation_statement = Object(Returns)

	def add_address(self, care_of, po_box, line1, line2, town, county, country, post_code):
		"""Change the registered address"""
		self.registered_address.update(
			Address(
				care_of=care_of,
				po_box=po_box,
				line1=line1,
				line2=line2,
				town=town,
				county=county,
				country=country,
				post_code=post_code))

	def age(self):
		"""Calculate the current age of the company"""
		if self.is_dissolved():
			return self.dissolution - self.incorporation
		return datetime.now() - self.incorporation

	def is_dissolved(self):
		"""Check if the company has been dissolved"""
		return self.dissolution >= self.incorporation

	class Index:
		"""The index that all instances of this metadata will be saved to"""
		name = 'companies'
		settings = {
			"number_of_shards"        : 1,
			"mapping.ignore_malformed": True,
		}

	def save(self, **kwargs):
		"""Saves the current item to the index"""
		# self.lines = len(self.body.split())
		return super(Company, self).save(**kwargs)


def download(zip_url, zip_filepath):
	"""Download the csv from companies house"""
	print('{time} Downloading companies house zip'.format(time=datetime.now()))
	with urllib.request.urlopen(zip_url) as response, open(zip_filepath, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)


def unzip(zip_filepath, output_path):
	"""Unzip the csv"""
	print('{time} Unzipping companies house zip'.format(time=datetime.now()))
	with zipfile.ZipFile(zip_filepath, 'r') as zipfilename:
		zipfilename.extractall(output_path)


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
				address = Address(
					care_of=row['RegAddress.CareOf'],
					po_box=row['RegAddress.POBox'],
					line1=row['RegAddress.AddressLine1'],
					line2=row['RegAddress.AddressLine2'],
					town=row['RegAddress.PostTown'],
					county=row['RegAddress.County'],
					country=row['RegAddress.Country'],
					post_code=row['RegAddress.PostCode'])

				accounts = Accounts(
					ref_day=row['Accounts.AccountRefDay'],
					ref_month=row['Accounts.AccountRefMonth'],
					next_due=row['Accounts.NextDueDate'],
					last_made_up=row['Accounts.LastMadeUpDate'],
					category=row['Accounts.AccountCategory'])

				returns = Returns(next_due=row['Returns.NextDueDate'], last_made_up=row['Returns.LastMadeUpDate'])

				confirmation_statement = Returns(
					next_due=row['ConfStmtNextDueDate'],
					last_made_up=row['ConfStmtLastMadeUpDate'])

				mortgages = Mortgages(
					charges=row['Mortgages.NumMortCharges'],
					outstanding=row['Mortgages.NumMortOutstanding'],
					part_satisfied=row['Mortgages.NumMortPartSatisfied'],
					satisfied=row['Mortgages.NumMortSatisfied'])

				limited_partnerships = LimitedPartnerships(
					general_partners=row['LimitedPartnerships.NumGenPartners'],
					limited_partners=row['LimitedPartnerships.NumLimPartners'])

				previous_name = [
					PreviousName(name=row['PreviousName_1.CompanyName'], date=row['PreviousName_1.CONDATE']),
					PreviousName(name=row['PreviousName_2.CompanyName'], date=row['PreviousName_2.CONDATE']),
					PreviousName(name=row['PreviousName_3.CompanyName'], date=row['PreviousName_3.CONDATE']),
					PreviousName(name=row['PreviousName_4.CompanyName'], date=row['PreviousName_4.CONDATE']),
					PreviousName(name=row['PreviousName_5.CompanyName'], date=row['PreviousName_5.CONDATE']),
					PreviousName(name=row['PreviousName_6.CompanyName'], date=row['PreviousName_6.CONDATE']),
					PreviousName(name=row['PreviousName_7.CompanyName'], date=row['PreviousName_7.CONDATE']),
					PreviousName(name=row['PreviousName_8.CompanyName'], date=row['PreviousName_8.CONDATE']),
					PreviousName(name=row['PreviousName_9.CompanyName'], date=row['PreviousName_9.CONDATE']),
					PreviousName(name=row['PreviousName_10.CompanyName'], date=row['PreviousName_10.CONDATE'])]

				company = Company(
					name=row['CompanyName'],
					number=row['CompanyNumber'],
					registered_address=address,
					category=row['CompanyCategory'],
					status=row['CompanyStatus'],
					country_of_origin=row['CountryOfOrigin'],
					dissolution=row['DissolutionDate'],
					incorporation=row['IncorporationDate'],
					accounts=accounts,
					returns=returns,
					mortgages=mortgages,
					SIC_code=[
						row['SICCode.SicText_1'],
						row['SICCode.SicText_2'],
						row['SICCode.SicText_3'],
						row['SICCode.SicText_4']],
					limited_partnerships=limited_partnerships,
					URI=row['URI'],
					previous_name=previous_name,
					confirmation_statement=confirmation_statement)
				company.save()
				row_count += 1
				if (row_count % 1000) == 0:
					print('{time} Ingested {x}'.format(x=row_count, time=datetime.now()))
			except UnicodeDecodeError:
				print('{time} unicode error on row {x}, {name}'.format(
					time=datetime.now(),
					x=row_count,
					name=row['CompanyName']))

	# Display cluster health
	print(connections.get_connection().cluster.health())


def setup_company_index(companies_file):
	"""Download companies house data and ingest it into the companies house index"""
	companies_zip_filename = companies_file + '.zip'
	companies_zip_url = download_url + companies_zip_filename
	companies_zip_filepath = os.path.join(data_path, companies_zip_filename)

	companies_csv_filename = companies_file + '.csv'
	companies_csv_filepath = os.path.join(data_path, companies_csv_filename)

	if not os.path.isfile(companies_zip_filepath):
		download(companies_zip_url, companies_zip_filepath)
	if not os.path.isfile(companies_csv_filepath):
		unzip(companies_zip_filepath, data_path)

	company_count(companies_csv_filepath)

	from elasticsearch_dsl import Index

	i = Index('companies')
	i.delete()

	ingest(companies_csv_filepath)


if __name__ == "__main__":
	setup_company_index('BasicCompanyDataAsOneFile-2019-04-01')
