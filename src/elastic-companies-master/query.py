"""
	Run this module to run a list of match queries against the companies index
"""
import csv
import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)

client = Elasticsearch()


def example_search():
	"""An example query"""
	s = Search(using=client, index='companies').query("match", name="ROYAL CHARTER")
		# .filter("term", category="search") \
		# .query("match", name="43")
		# .exclude("match", description="beta")

	#s.aggs.bucket('per_tag', 'terms', field='tags') \
	#	.metric('max_lines', 'max', field='lines')

	response = s.execute()

	print(response)

	for hit in response:
		print(hit.meta.score, hit.name)

	#for tag in response.aggregations.per_tag.buckets:
	#	print(tag.key, tag.max_lines.value)

	# article = Company.get(id=42)
	# print(article.is_published())


def get_matches(matchlist):
	"""Run a series of match queries from an input list. Results returned as a list of dictionaries"""
	responses = []

	for match in matchlist:
		s = Search(using=client, index='companies').query("match", name=match)
		response = s.execute()
		result_row = {'query_string': match}
		for n, hit in enumerate(response):
			result_row['match_{n}'.format(n=n)] = hit.name
			result_row['score_{n}'.format(n=n)] = hit.meta.score
		responses += [result_row]

	return responses


def load_matchlist(filepath='example_for_matching.tsv'):
	"""Get a list of strings to match from a tsv file"""
	matchlist = []
	with open(filepath, 'r', encoding='utf8') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		try:
			for row in tsvin:
				matchlist += [row[0]]
		except UnicodeDecodeError:
			print('{time} unicode error. q={q}'.format(time=datetime.datetime.now(), q=row[0]))

	return matchlist


def save_to_csv(rows, filepath='matches.csv'):
	"""Save a list of dictionaries as a csv file"""
	with open(filepath, 'w', encoding='utf8') as csvout:
		fieldnames = rows[0].keys()
		writer = csv.DictWriter(csvout, fieldnames=fieldnames)

		writer.writeheader()
		writer.writerows(rows)


if __name__ == "__main__":
	matches = get_matches(load_matchlist())
	save_to_csv(matches)
