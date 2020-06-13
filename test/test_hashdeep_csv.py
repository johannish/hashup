import unittest
from util.hashdeep_csv import parse_header

class HashdeepCsvTest(unittest.TestCase):
	def test_parse_header_happypath(self):
		self.assertEqual(parse_header('moo'), '')
