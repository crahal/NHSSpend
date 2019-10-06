import asyncio
import csv
import logging
import os

from log_setup import logging_setup
from pdf_table_parser import data_path, PdfTableParser

logger = logging.getLogger('pdf_table_parser').getChild(__name__)


async def process_path(path):
	results = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			name, file_type = os.path.splitext(filename)

			if file_type == '.pdf':
				try:
					result = await asyncio.wait_for(parse_file(dirpath, filename), timeout=60)
					result['path'] = os.path.relpath(dirpath, start=path)
				except asyncio.TimeoutError:
					logger.error('Timeout in pdf ' + filename)
					result = {'filename': filename, 'path': os.path.relpath(dirpath, start=path), 'state': 'TIMEOUT'}
				results.append(result)

	with open(os.path.join(path, 'results.csv'), 'w', encoding='utf8', newline='') as csvfile:
		# TODO more stats, processing time etc, output file path, log file path
		w = csv.DictWriter(csvfile, fieldnames=['filename', 'path', 'state', 'pages', 'columns', 'rows', 'headers'])
		w.writeheader()
		w.writerows(results)


async def parse_file(path, filename):
	# TODO much of this should be handled by the parser object, including exception catches and generating results dict
	logger.info('Starting to process pdf ' + filename)
	result = {'filename': filename, 'path': path, 'state': 'INIT'}
	try:
		# TODO dont need to join dirpath to filename
		parser = PdfTableParser(os.path.join(path, filename))
		parser.get_page_layouts()
		parser.parse_layouts()
		parser.save_output()
		result['pages'] = len(parser.layouts)
		result['columns'] = len(parser.headers[0]) if len(parser.headers) > 0 else 0
		result['rows'] = len(parser.rows)
		#result['fonts']
		result['headers'] = len(parser.headers)
		#result['unique headers']
		result['state'] = 'OK'
	except Exception as e:
		result['state'] = 'ERROR'
		logger.error('Error in pdf ' + filename)

	return result


async def main():
	logging_setup()
	await asyncio.wait_for(process_path(os.path.join(data_path, 'ccg')), timeout=None)


if __name__ == '__main__':
	# TODO atexit()
	asyncio.run(main())
