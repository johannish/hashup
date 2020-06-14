import unittest

from util.hashdeep_csv import HashdeepCsvHeader
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_header
from util.database import load_csv
from util.database import read_count

class DatabaseTest(unittest.TestCase):
	def test_load_csv(self):
		testfile = 'test/data/output.20200525.hashdeep'
		#testfile = 'test/data/output.20200325.hashdeep'
		#testfile = 'test/data/example.hashdeep'
		#headers = HashdeepCsvHeader('v1', ['size','md5','filename'], '', '', 5)
		headers = parse_header(read_header(testfile))
		dbfilename, tablename = load_csv(headers, testfile, tablename='file2', dbfilename='twofiles.db')
		rowcount = read_count(tablename, dbfilename)
		print(f'{rowcount} rows ingested from test file')
		self.assertIsNotNone(rowcount)
		self.assertGreater(rowcount, 1)
