import sqlite3
import pandas as pd

from datetime import datetime

conn = None

def load_csv(header, filename, tablename=None, dbfilename=None):
	delimiter = ','
	# can't use pandas read_csv because of unquoted filenames with delimiter
	#df = pd.read_csv(filename, names=header.csv_column_names, skiprows=header.line_count)
	rows = []
	with open(filename, 'r') as file:
		firstline = file.readline()
		if not firstline.find('HASHDEEP') > -1:
			raise Exception(f'File "{filename}" is not in hashdeep csv format. Start of first line is "{firstline[:80]}"')
		for line in file:
			if line.startswith('%') or line.startswith('#'):
				continue
			# assumes filename is last in output, and is the only field that contains the delimiter
			fields = line.split(delimiter, maxsplit=len(header.csv_column_names) - 1)
			rows.append(fields)
	
	df = pd.DataFrame(data=rows, columns=header.csv_column_names)

	if dbfilename is None:
		dbfilename = datetime.now().isoformat().replace('-','').replace(':','').replace('.','') + '.db'
	conn = get_sqlite3_connection(dbfilename)

	if tablename is None:
		tablename = datetime.now().isoformat().replace('-','').replace(':','').replace('.','')
	df.to_sql(tablename, conn)

	conn.close()

	return (dbfilename, tablename)

def scrub(tablename):
	return ''.join( chr for chr in tablename if chr.isalnum() )

def read_count(tablename, dbfilename):
	conn = get_sqlite3_connection(dbfilename)

	c = conn.cursor()
	c.execute(f'select count(*) from {scrub(tablename)}') # BEWARE SQL INJECTION.
	result = c.fetchone()[0]
	conn.close()

	return result

def get_sqlite3_connection(dbfilename):
	# TODO: figure out how to manage `conn.close()` lifecycle while allowing a toggle
	# between in-memory (where close() is irrelevant) and on-disk db.
	# if dbfilename is None:
		# if conn is None:
			# print('using in memory db')
			# conn = sqlite3.connect('file::memory:?cache=shared', uri=True)
		# return conn
	# else:
	return sqlite3.connect(dbfilename)
