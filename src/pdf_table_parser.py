import logging
import os
import random

from PIL import Image, ImageDraw
import PIL
import PIL.ImageFont
import PIL.ImageColor

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LTRect, LTChar
from pdfminer.layout import LTAnon, LTComponent
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
#from log_setup import logging_setup

logger = logging.getLogger('pdf_table_parser').getChild(__name__)

file_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(file_path, '')

data_path = os.path.join(path, 'data')


class PdfTableParser:
	def __init__(self, filepath):
		self.filepath = os.path.normpath(filepath)
		self.layouts = []
		self.rows = []
		self.headers = []

	def get_page_layouts(self):
		with open(self.filepath, 'rb') as fp:
			logger.info('Opening PDF file: {file}'.format(file=self.filepath))
			parser = PDFParser(fp)
			doc = PDFDocument()
			parser.set_document(doc)
			doc.set_parser(parser)

			doc.initialize("")

			if not doc.is_extractable:
				raise PDFTextExtractionNotAllowed

			resource_manager = PDFResourceManager()
			device = PDFPageAggregator(resource_manager, laparams=LAParams(heuristic_word_margin=True, word_margin=0, char_margin=0.5))
			interpreter = PDFPageInterpreter(resource_manager, device)

			self.layouts = []
			for page in doc.get_pages():
				interpreter.process_page(page)
				self.layouts.append(device.get_result())
			logger.info('Opened PDF with {n} pages'.format(n=len(self.layouts)))

	def parse_layouts(self):
		for l in self.layouts:
			p = LayoutTableParser(l, self.filepath)
			p.to_tables()
			self.rows += p.rows
		self.identify_headers()
		self.unique_headers()

	def parse_first_layouts(self):
		p = LayoutTableParser(self.layouts[5])
		p.to_tables()

	def save_output(self):
		import csv
		with open(self.filepath + '.csv', 'w', newline='', encoding="utf-8") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			if self.headers:
				header = [c.get_text().strip() if c is not None else '' for c in self.headers[0]['cells']]
				writer.writerow(header)
			for row in self.rows:
				line = [c.get_text().strip() if c is not None else '' for c in row['cells']]
				writer.writerow(line)

	def identify_headers(self):
		# TODO should identify headers much earlier before attempting to merge any tables
		logger.info('Attempting to identify headers')
		fonts = []
		found = False
		for row in self.rows:
			for font in fonts:
				if (font['name'] == row['font']) and (font['size'] / row['font_size'] > 0.95) and (font['size'] / row['font_size'] < 1.05):
					font['count'] = font['count'] + 1
					found = True
			if not found:
				fonts.append({'name': row['font'], 'size': row['font_size'], 'count': 1})
				found = False
		logger.info('{n} fonts in pdf'.format(n=len(fonts)))

		header_fonts = []
		for font in fonts:
			if font['count'] / len(self.rows) < 0.10:
				header_fonts.append(font)
		logger.info('{n} header fonts in pdf'.format(n=len(header_fonts)))

		headers = list(filter(lambda x: is_font_in_list(x['font'], x['font_size'], header_fonts), self.rows))
		rows = list(filter(lambda x: not is_font_in_list(x['font'], x['font_size'], header_fonts), self.rows))
		logger.info('{n} header rows in pdf'.format(n=len(headers)))
		logger.info('{n} rows in pdf'.format(n=len(rows)))

		self.rows = rows
		self.headers = headers

	def unique_headers(self):
		uniques = []
		for header in self.headers:
			if not uniques:
				uniques.append(header)
			elif not any(map(lambda y: is_row_identical(header, y), uniques)):
				uniques.append(header)
		self.headers = uniques
		rows = list(filter(lambda x: not any(map(lambda y: is_row_identical(x, y), self.headers)), self.rows))
		self.rows = rows
		logger.info('{n} unique headers'.format(n=len(self.headers)))
		for row in self.headers:
			line = [c.get_text() if c is not None else '' for c in row['cells']]
			logger.info(line)


def is_row_identical(a, b):
	if len(a['cells']) == len(b['cells']):
		for n in range(len(a['cells'])):
			if (a['cells'][n].get_text() if a['cells'][n] is not None else '').lower().strip() != (b['cells'][n].get_text() if b['cells'][n] is not None else '').lower().strip():
				# all()?
				return False
		return True
	else:
		return False


class LayoutTableParser:
	def __init__(self, layout, filepath, debug=False):
		self.layout = layout
		self.rows = []
		self.columns = []
		self.colgroups = []
		self.finalcols = []
		self.finalcols2 = []
		self.lines = []
		self.texts = []
		self.multi_col_boxes = []
		self.drawDebug = debug
		self.filepath = filepath
		self.scale_factor = 10
		self.h = int(self.layout.height * self.scale_factor)

	def to_tables(self):
		self.to_tables1()
		self.to_tables2()
		self.to_tables3()
		self.to_tables4()
		if self.drawDebug:
			im = Image.new('RGBA', (int(self.layout.width * self.scale_factor), int(self.layout.height * self.scale_factor)), 'white')
			draw = ImageDraw.Draw(im)
			self.draw_text(draw)
			for c in self.finalcols:
				draw.rectangle([int(c['contain'].bbox[0] * self.scale_factor), self.h - int(c['contain'].bbox[3] * self.scale_factor), int(c['contain'].bbox[2] * self.scale_factor), self.h - int(c['contain'].bbox[1] * self.scale_factor)], fill=None, outline=c['color'], width=5 * self.scale_factor)
			im.save('{file}.page{pn}.stage{sn}.png'.format(file=self.filepath, pn=self.layout.pageid, sn=4), "PNG")
		self.to_tables5()
		if self.drawDebug:
			im = Image.new('RGBA', (int(self.layout.width * self.scale_factor), int(self.layout.height * self.scale_factor)), 'white')
			draw = ImageDraw.Draw(im)
			self.draw_text(draw)
			for c in self.finalcols2:
				draw.rectangle([int(c['contain'].bbox[0] * self.scale_factor), self.h - int(c['contain'].bbox[3] * self.scale_factor), int(c['contain'].bbox[2] * self.scale_factor), self.h - int(c['contain'].bbox[1] * self.scale_factor)], fill=None, outline=c['color'], width=5 * self.scale_factor)
			im.save('{file}.page{pn}.stage{sn}.png'.format(file=self.filepath, pn=self.layout.pageid, sn=5), "PNG")
		self.to_tables6()
		if self.drawDebug:
			im = Image.new('RGBA', (int(self.layout.width * self.scale_factor), int(self.layout.height * self.scale_factor)), 'white')
			draw = ImageDraw.Draw(im)
			self.draw_text(draw)
			for c in self.finalcols2:
				draw.rectangle([int(c['contain'].bbox[0] * self.scale_factor), self.h - int(c['contain'].bbox[3] * self.scale_factor), int(c['contain'].bbox[2] * self.scale_factor), self.h - int(c['contain'].bbox[1] * self.scale_factor)], fill=None, outline=c['color'], width=5 * self.scale_factor)
			im.save('{file}.page{pn}.stage{sn}.png'.format(file=self.filepath, pn=self.layout.pageid, sn=6), "PNG")
			for c in self.multi_col_boxes:
				draw.rectangle([int(c.bbox[0] * self.scale_factor), self.h - int(c.bbox[3] * self.scale_factor), int(c.bbox[2] * self.scale_factor), self.h - int(c.bbox[1] * self.scale_factor)], fill=None, outline='black', width=5 * self.scale_factor)
			im.save('{file}.page{pn}.stage{sn}.png'.format(file=self.filepath, pn=self.layout.pageid, sn=6.1), "PNG")
		self.to_tables7()
		self.to_tables8()

	def draw_text(self, draw):
		for e in self.texts:
			char = e._objs[0]._objs[0]
			fontname = char.fontname
			font = PIL.ImageFont.truetype(font="arial.ttf", size=int(char.size * self.scale_factor))
			for line in e:
				c = random.choice(list(PIL.ImageColor.colormap.keys()))
				draw.rectangle([int(line.bbox[0] * self.scale_factor), self.h - int(line.bbox[3] * self.scale_factor), int(line.bbox[2] * self.scale_factor), self.h - int(line.bbox[1] * self.scale_factor)], fill=None, outline=c, width=2 * self.scale_factor)
				c = random.choice(list(PIL.ImageColor.colormap.keys()))
				for char in line:
					if not isinstance(char, LTAnon):
						draw.text((int(char.bbox[0] * self.scale_factor), self.h - int(char.bbox[3] * self.scale_factor)), char.get_text(), fill='black', font=font)
						draw.rectangle([int(char.bbox[0] * self.scale_factor), self.h - int(char.bbox[3] * self.scale_factor), int(char.bbox[2] * self.scale_factor), self.h - int(char.bbox[1] * self.scale_factor)], fill=None, outline=c, width=int(0.5 * self.scale_factor))

	def to_tables1(self):
		texts = []
		rectangles = []
		other = []
		logger.info("Starting page {id}".format(id=self.layout.pageid))

		#with open('page.png', 'r+') as imagefile:

		##im = Image.new('RGBA', (int(self.layout.width * scale_factor), int(self.layout.height * scale_factor)), 'white')

		##draw = ImageDraw.Draw(im)
		#draw.line((0, 0) + im.size, fill=128)
		#draw.line((0, im.size[1], im.size[0], 0), fill=128)
		for e in self.layout:
			if isinstance(e, LTTextBoxHorizontal):
				texts.append(e)
				char = e._objs[0]._objs[0]
				fontname = char.fontname
				#font = PIL.ImageFont.truetype(font="calibri.ttf", size=int(char.size * scale_factor))
				#draw.text((int(e.bbox[0] * 100), h - int(e.bbox[3] * 100)), e.get_text(), fill='black', font=font)
				c = random.choice(list(PIL.ImageColor.colormap.keys()))
				##draw.rectangle([int(e.bbox[0] * scale_factor), h - int(e.bbox[3] * scale_factor), int(e.bbox[2] * scale_factor), h - int(e.bbox[1] * scale_factor)], fill=None, outline=c, width=3 * scale_factor)
				logger.debug(e)
			elif isinstance(e, LTRect):
				rectangles.append(e)
				##draw.rectangle([int(e.pts[0][0] * scale_factor), h - int(e.pts[2][1] * scale_factor), int(e.pts[2][0] * scale_factor), h - int(e.pts[0][1] * scale_factor)], fill=None, outline='black', width=e.linewidth)
			else:
				other.append(e)
				logger.debug(e)

		self.texts = texts
		# write to stdout
		##im.save('page3.png', "PNG")

	def to_tables2(self):
		columns = []
		# texts.sort(key=lambda x: x.width)
		for e in self.layout:
			if isinstance(e, LTTextBoxHorizontal):
				logger.info('Finding a column for box {i}'.format(i=e.index))
				##im2 = im.copy()
				##d = ImageDraw.Draw(im2)
				col = None
				for c in columns:
					if (e.x1 < c['contain'].x1) and (e.x0 > c['contain'].x0):
						if (e.width / c['contain'].width) < 0.8:
							logger.info('Item too small, column may be several columns wide')
						else:
							logger.info('Item totally contained in column')
							logger.info('{ex1} < {cx1} and {ex0} > {cx0}'.format(ex1=e.x1, cx1=c['contain'].x1, ex0=e.x0, cx0=c['contain'].x0))
							col = c
							col['boxes'].append(e)
							col['contain'].set_bbox((c['contain'].x0, min(c['contain'].y0, e.y0), c['contain'].x1, max(c['contain'].y1, e.y1)))
							##d.rectangle([int(c['contain'].bbox[0] * scale_factor), h - int(c['contain'].bbox[3] * scale_factor), int(c['contain'].bbox[2] * scale_factor), h - int(c['contain'].bbox[1] * scale_factor)], fill=None, outline=c['color'], width=5 * scale_factor)
						break
					elif ((c['contain'].hoverlap(e) / c['contain'].width) > 0.9) and ((c['contain'].hoverlap(e) / c['contain'].width) < 1.1):
						logger.info('Item is within 10% of current col width')
						logger.info('Overlap of {hdist}, column width of {width}'.format(hdist=c['contain'].hoverlap(e), width=c['contain'].width))
						col = c
						col['boxes'].append(e)
						col['contain'].set_bbox((min(c['contain'].x0, e.x0), min(c['contain'].y0, e.y0), max(c['contain'].x1, e.x1), max(c['contain'].y1, e.y1)))
						##d.rectangle([int(c['contain'].bbox[0] * scale_factor), h - int(c['contain'].bbox[3] * scale_factor), int(c['contain'].bbox[2] * scale_factor), h - int(c['contain'].bbox[1] * scale_factor)], fill=None, outline=c['color'], width=5 * scale_factor)
						break
				if not col:
					logger.info('Creating new column')
					col = {'contain': LTComponent(e.bbox), 'boxes': list(e), 'color': random.choice(list(PIL.ImageColor.colormap.keys()))}
					columns.append(col)
					columns.sort(key=lambda x: x['contain'].width)
					##d.rectangle([int(col['contain'].bbox[0] * scale_factor), h - int(col['contain'].bbox[3] * scale_factor), int(col['contain'].bbox[2] * scale_factor), h - int(col['contain'].bbox[1] * scale_factor)], fill=None, outline=col['color'], width=5 * scale_factor)
				##im2.save('page0.{x}.png'.format(x=e.index), "PNG")
		self.columns = columns
		##im3 = im.copy()
		##draw2 = ImageDraw.Draw(im3)
		##for c in columns:
		##	draw.rectangle([int(c['contain'].bbox[0] * scale_factor), h - int(c['contain'].bbox[3] * scale_factor), int(c['contain'].bbox[2] * scale_factor), h - int(c['contain'].bbox[1] * scale_factor)], fill=None, outline=c['color'], width=5 * scale_factor)

		##im.save('page4.png', "PNG")

	def to_tables3(self):
		colgroups = []
		for c in self.columns:
			colg = None
			for d in colgroups:
				if c is not d:
					if all(c['contain'].is_hoverlap(e['contain']) for e in d['cols']):
						d['cols'].append(c)
						colg = d
						break
			if not colg:
				colgroups.append({'contain': LTComponent(c['contain'].bbox), 'cols': [c]})
		logger.info('{x} colgroups'.format(x=len(colgroups)))
		self.colgroups = colgroups

	def to_tables4(self):
		finalcols = []
		multi_col_boxes = []
		for g in self.colgroups:
			logger.info('colgroup with {x} columns'.format(x=len(g['cols'])))
			if len(g) == 0:
				continue
			elif len(g) == 1:
				finalcols.append(g['cols'][0])
			elif all(col1['contain'].is_hoverlap(col2['contain']) for col1 in g['cols'] for col2 in g['cols']):
				logger.info('All cols have horizontal overlap')
				# all voverlap is less than the average line height
				# if all()
				x0 = min([col['contain'].x0 for col in g['cols']])
				y0 = min([col['contain'].y0 for col in g['cols']])
				x1 = max([col['contain'].x1 for col in g['cols']])
				y1 = max([col['contain'].y1 for col in g['cols']])
				g['cols'][0]['contain'].set_bbox((x0, y0, x1, y1))
				for e in g['cols'][1:]:
					g['cols'][0]['boxes'] += e['boxes']
				if all(not g['cols'][0]['contain'].is_hoverlap(col['contain']) for col in finalcols):
					finalcols.append(g['cols'][0])
				else:
					boxes = list(filter(lambda x: all(not x.is_hoverlap(y['contain']) for y in finalcols), g['cols'][0]['boxes']))
					if not len(boxes):
						logger.info('Engulfed column')
						for col in finalcols:
							if any(col['contain'].is_hoverlap(x) for x in g['cols'][0]['boxes']):
								col['multicol'] = True
						finalcols.append(g['cols'][0])
					else:
						x0 = min([box.x0 for box in boxes])
						y0 = min([box.y0 for box in boxes])
						x1 = max([box.x1 for box in boxes])
						y1 = max([box.y1 for box in boxes])
						g['cols'][0]['contain'].set_bbox((x0, y0, x1, y1))
						g['cols'][0]['boxes'] = boxes
						finalcols.append(g['cols'][0])
						multi_col_boxes = list(filter(lambda x: any(x.is_hoverlap(y['contain']) for y in finalcols), g['cols'][0]['boxes']))
						logger.info('{n} multi col boxes'.format(n=len(multi_col_boxes)))
			else:
				# multi-col
				logger.info('Need to split multi-col')
				g['cols'].sort(key=lambda x: x['contain'].width, reverse=True)
				#if c is not d:
				#	if (d['contain'].x1 <= c['contain'].x1) and (d['contain'].x0 >= c['contain'].x0):
				#		if ((c['contain'].hoverlap(d['contain']) / c['contain'].width) < 0.9):
				#			# solely contained column d that is less than 90% of the width of c
				#			if c in columns:
				#				columns.remove(c)
				#				break
				#		elif ((c['contain'].hoverlap(d['contain']) / c['contain'].width) > 0.9) and ((c['contain'].hoverlap(d['contain']) / c['contain'].width) < 1.1):
				#			c['contain'].set_bbox((min(c['contain'].x0, d['contain'].x0), min(c['contain'].y0, d['contain'].y0), max(c['contain'].x1, d['contain'].x1), max(c['contain'].y1, d['contain'].y1)))
				#			if d in columns:
				#				columns.remove(d)
		self.finalcols = finalcols

	def to_tables5(self):
		finalcols2 = []
		for col in self.finalcols:
			if 'multicol' in col and col['multicol']:
				continue
			else:
				finalcols2.append(col)

		for col in self.finalcols:
			if 'multicol' in col and col['multicol']:
				boxes = list(filter(lambda x: all(not x.is_hoverlap(y['contain'] if x is not col else True) for y in finalcols2), col['boxes']))
				if not len(boxes):
					logger.info('Nested engulfed column, need to while with limit')
				else:
					x0 = min([box.x0 for box in boxes])
					y0 = min([box.y0 for box in boxes])
					x1 = max([box.x1 for box in boxes])
					y1 = max([box.y1 for box in boxes])
					col['contain'].set_bbox((x0, y0, x1, y1))
					col['boxes'] = boxes
					finalcols2.append(col)
					multi_col_boxes = list(filter(lambda x: any(x.is_hoverlap(y['contain']) for y in finalcols2), col['boxes']))
					logger.info('{n} multi col boxes'.format(n=len(multi_col_boxes)))
		self.finalcols2 = finalcols2

	def to_tables6(self):
		multi_col_boxes = []

		for c in self.finalcols2:
			c['boxes'] = []

		# reacquire all text boxes that only overlap with a single column
		for t in self.texts:
			hoverlaps = 0
			col = None
			for c in self.finalcols2:
				if t.hoverlap(c['contain']):
					hoverlaps += 1
					col = c
			if hoverlaps == 1:
				col['boxes'].append(t)
			elif hoverlaps > 1:
				if t not in multi_col_boxes:
					multi_col_boxes.append(t)

		for c in self.finalcols2:
			if len(c['boxes']):
				x0 = min([box.x0 for box in c['boxes']])
				y0 = min([box.y0 for box in c['boxes']])
				x1 = max([box.x1 for box in c['boxes']])
				y1 = max([box.y1 for box in c['boxes']])
				c['contain'].set_bbox((x0, y0, x1, y1))
			else:
				logger.info('Error empty column')

		self.finalcols2.sort(key=lambda x: x['contain'].x0)
		logger.info('{x} multi column boxes'.format(x=len(multi_col_boxes)))
		logger.info('{x} columns'.format(x=len(self.finalcols2)))
		self.multi_col_boxes = multi_col_boxes

	def to_tables7(self):
		lines = []
		for t in filter(lambda x: x not in self.multi_col_boxes, self.texts):
			for line in t:
				placed = False
				for l in lines:
					if (l['contain'].voverlap(line) / l['contain'].height > 0.9) and (l['contain'].voverlap(line) / l['contain'].height < 1.1):
						l['texts'].append(line)
						l['contain'].set_bbox((min(l['contain'].x0, line.x0), l['contain'].y0, max(l['contain'].x1, line.x1), l['contain'].y1))
						placed = True
				if not placed:
					lines.append({'contain': LTComponent(line.bbox), 'texts': [line]})
		lines.sort(key=lambda x: x['contain'].y0)

		for line in lines:
			line['cells'] = [None]*len(self.finalcols2)
			for columntext in line['texts']:
				for i, column in enumerate(self.finalcols2):
					if column['contain'].hoverlap(columntext):
						if line['cells'][i] is None:
							line['cells'][i] = columntext
							break
						else:
							# seems like the parser library sometimes duplicates text, possible bug
							pass
		self.lines = lines

	def to_tables8(self):
		rows = []
		while self.lines:
			l = self.lines.pop()
			if l['cells'][0] is None and self.lines:
				# font check should really check font is consistent for a row, then compare row fonts
				current_font = None
				current_font_size = 0
				for cell in l['cells']:
					if cell:
						for char in cell:
							if isinstance(char, LTChar):
								current_font = char.fontname
								current_font_size = char.size

				next_font = None
				next_font_size = 0
				for cell in self.lines[-1]['cells']:
					if cell:
						for char in cell:
							if isinstance(char, LTChar):
								next_font = char.fontname
								next_font_size = char.size

				if (current_font == next_font) and (current_font_size / next_font_size > 0.95) and (current_font_size / next_font_size < 1.05):
					# merge
					# how to know the valign?
					# should recurse, how many lines to merge?
					l2 = self.lines.pop()
					row = l
					for i, cell in enumerate(l['cells']):
						if cell is not None:
							if l2['cells'][i] is None:
								row['cells'][i] = cell
							else:
								for char in l2['cells'][i]:
									if isinstance(char, LTChar):
										cell.add(char)
								row['cells'][i] = cell
								l2['cells'][i] = None
						else:
							row['cells'][i] = l2['cells'][i]
					rows.append(row)
				else:
					rows.append(l)
			else:
				rows.append(l)

		# check row fonts, this might be useful earlier as its used in the merge rows check
		for row in rows:
			for cell in row['cells']:
				if cell:
					for char in cell:
						if isinstance(char, LTChar):
							row['font'] = char.fontname
							row['font_size'] = char.size
		self.rows = rows


# group textboxes by left x point for left-aligned columns, group textboxes by right x point for right -aligned, group by midpoint for center align
# midpoint might be more useful for establishing cols

def is_same_font(name, size, name2, size2):
	return name == name2 and (size / size2 > 0.95) and (size / size2 < 1.05)


def is_font_in_list(name, size, fontlist):
	for font in fontlist:
		if is_same_font(name, size, font['name'], font['size']):
			return True


def parse():
	logging_setup()
	pdf_pathname = os.path.join(data_path, 'nhs', 'BD-CCG-invoices-over-30k-April-2014-March-2015.pdf')

	parser = PdfTableParser(pdf_pathname)
	parser.get_page_layouts()
	parser.parse_layouts()
	parser.save_output()


if __name__ == '__main__':
	parse()
