import unittest

from util.hashdeep_csv import HashdeepCsvHeader
from util.database import load_csv
from util.database import read_count

class DatabaseTest(unittest.TestCase):
	def test_load_csv(self):
		x = HashdeepCsvHeader('v1', ['size','md5','path'], '', '', 5)
		dbfilename, tablename = load_csv(x, 'test/data/example.hashdeep', tablename='file1')
		rowcount = read_count('file1', dbfilename)
		print(f'{rowcount} rows ingested from test file')
		self.assertIsNotNone(rowcount)
		self.assertGreater(rowcount, 1)
