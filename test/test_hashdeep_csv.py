import unittest
from unittest.mock import patch,mock_open

from util.hashdeep_csv import parse_header
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_csv

class HashdeepCsvTest(unittest.TestCase):
	def test_parse_header(self):
		headerlines = [
			'%%%% HASHDEEP-1234.abcde'
			,'%%%% size, hash1,hash2,filename'
			,'## Invoked from: /moo/cow/place/'
			,'## $ hashdeep -c hash1,hash2 -r .'
			,'##'
		]
		result = parse_header(headerlines)
		self.assertEqual(result.hashdeep_version, 'HASHDEEP-1234.abcde')
		self.assertEqual(result.csv_column_names, ['size','hash1','hash2','filename'])
		self.assertEqual(result.invoked_dir, '/moo/cow/place/')
		self.assertEqual(result.invoked_cmd, '$ hashdeep -c hash1,hash2 -r .')
		self.assertEqual(result.line_count, 5)

	def test_read_header(self):
		results = read_header('test/data/example.hashdeep')
		self.assertEqual(len(results), 5)

	def test_parse_csv_exception(self):
		testfile = 'some/path/nothashdeep.txt'
		with patch('builtins.open', mock_open(read_data='Not a hashdeep header')) as o:
			header = parse_header(read_header(testfile))
			o.assert_called_with(testfile, 'r')
			self.assertRaises(RuntimeError, parse_csv, header, testfile)

	def test_parse_csv_filepath(self):
		testfile = 'some/path/hashdeep-file'
		testfile_contents = \
'''%%%% HASHDEEP-0.0
%%%% size,md5,filename
10,an-md5-1,/a/file/path/sane.txt
12,an-md5-2,/a/file/path/with spaces, and, commas.txt
'''
		with patch('builtins.open', mock_open(read_data=testfile_contents)) as o:
			header = parse_header(read_header(testfile))
			o.assert_called_with(testfile, 'r')
			dataframe = parse_csv(header, testfile)
			for name in dataframe['leafname'].values:
				self.assertFalse("\n" in name, "leafname should not contain '\\n'")
			for name in dataframe['filename'].values:
				self.assertFalse("\n" in name, "filename should not contain '\\n'")

