import sqlite3

from datetime import datetime

conn = None

def filesafe_timestamp():
	return datetime.now().isoformat().replace('-','').replace(':','').replace('.','')

def load_dataframe(hashdeep_data, tablename=None, dbfilename=None):
	if dbfilename is None:
		dbfilename = filesafe_timestamp() + '.db'
	conn = get_sqlite3_connection(dbfilename)

	if tablename is None:
		tablename = filesafe_timestamp()
	hashdeep_data.to_sql(tablename, conn)

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
	#  see: https://stackoverflow.com/a/51456087
	#  see: https://stackoverflow.com/a/32681822
	#  see: https://www.sqlite.org/inmemorydb.html
	# if dbfilename is None:
		# if conn is None:
			# print('using in memory db')
			# conn = sqlite3.connect('file::memory:?cache=shared', uri=True)
		# return conn
	# else:
	return sqlite3.connect(dbfilename)
