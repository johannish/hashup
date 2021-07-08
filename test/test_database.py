import os
import unittest

from util.hashdeep_csv import HashdeepCsvHeader
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_header
from util.hashdeep_csv import parse_csv
from util.database import load_dataframe
from util.database import read_count

class DatabaseTest(unittest.TestCase):
	def test_load_csv(self):
		fixture_dbfilename = 'test/data/unittest-out.db'
		try:
			os.remove(fixture_dbfilename)
		except FileNotFoundError:
			pass

		testfile = 'test/data/example.hashdeep'
		headers = parse_header(read_header(testfile))
		print(f'headers: {headers}')
		data = parse_csv(headers, testfile)

		dbfilename, tablename = load_dataframe(data, tablename='file1', dbfilename=fixture_dbfilename)

		rowcount = read_count(tablename, dbfilename)
		print(f'{rowcount} rows ingested from {testfile}')
		self.assertIsNotNone(rowcount)
		self.assertGreater(rowcount, 1)

		testfile2 = 'test/data/example2.hashdeep'
		headers2 = parse_header(read_header(testfile2))
		data2 = parse_csv(headers2, testfile2)

		dbfilename, tablename = load_dataframe(data2, tablename='file2', dbfilename=fixture_dbfilename)

		rowcount = read_count(tablename, dbfilename)
		print(f'{rowcount} rows ingested from {testfile2}')
		self.assertIsNotNone(rowcount)
		self.assertGreater(rowcount, 1)
