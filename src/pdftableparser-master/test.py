import logging
import os

from log_setup import logging_setup
from path_parser import process_path
from pdf_table_parser import data_path, PdfTableParser

logger = logging.getLogger('pdf_table_parser').getChild(__name__)


def test():
	logging_setup()

	pathnames = []
	pathnames += [os.path.join('nhs', 'BD-CCG-invoices-over-30k-April-2014-March-2015.pdf')]
	pathnames += [os.path.join('dcms', '1_Jan_to_31_Mar_2013_Ministerial_Meetings_Hospitality_Overseas_travel.pdf')]
	pathnames += [os.path.join('bis', 'bis-ministerial-expenses-january-march-2015.pdf')]
	pathnames += [os.path.join('bis', 'bis-ministerial-expenses-july-september-2014.pdf')]
	pathnames += [os.path.join('moj', '2015q1.pdf')]
	pathnames += [os.path.join('ago', '2015_0103.pdf')]

	for pathname in pathnames:
		logger.info('Starting to process pdf ' + pathname)

		parser = PdfTableParser(os.path.join(data_path, pathname))
		parser.get_page_layouts()
		parser.parse_layouts()
		parser.save_output()

	process_path(os.path.join(data_path, 'ccg', 'NHS_BARNET_CCG'))


if __name__ == '__main__':
	test()
