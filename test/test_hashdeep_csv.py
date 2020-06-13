import unittest

from util.hashdeep_csv import parse_header
from util.hashdeep_csv import read_header

class HashdeepCsvTest(unittest.TestCase):
	def test_parse_header(self):
		headerlines = [
			'%%%% HASHDEEP-1234.abcde'
			,'%%%% size,hash1,hash2,filename'
			,'## Invoked from: /moo/cow/place/'
			,'## $ hashdeep -c hash1,hash2 -r .'
			,'##'
		]
		result = parse_header(headerlines)
		self.assertEqual(result.hashdeep_version, 'HASHDEEP-1234.abcde')
		self.assertEqual(result.csv_column_names, 'size,hash1,hash2,filename')
		self.assertEqual(result.invoked_dir, '/moo/cow/place/')
		self.assertEqual(result.invoked_cmd, '$ hashdeep -c hash1,hash2 -r .')

	def test_read_header(self):
		results = read_header('test/data/example.hashdeep')
		self.assertEqual(len(results), 5)
