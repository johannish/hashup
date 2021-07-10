import sqlite3
import sys

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
	try:
		hashdeep_data.to_sql(tablename, conn)
	except ValueError as e:
		print('Table likely exists. Pandas error was:', e, file=sys.stderr) #TODO verbose logging

	conn.close()

	return (dbfilename, tablename)

def scrub(tablename):
	# thanks to https://stackoverflow.com/a/3247553/
	return ''.join( chr for chr in tablename if chr.isalnum() )

def read_count(tablename, dbfilename):
	conn = get_sqlite3_connection(dbfilename)

	c = conn.cursor()
	c.execute(f'select count(*) from "{scrub(tablename)}"') # BEWARE SQL INJECTION.
	result = c.fetchone()[0]
	conn.close()

	return result

def read_not_in_table2(tablename1, tablename2, dbfilename):
	conn = get_sqlite3_connection(dbfilename)
	conn.row_factory = sqlite3.Row # creates an efficient dict-like object

	c = conn.cursor()
	sql = '''
		select *
		from "{table1}" as t1
			left join "{table2}" as t2 on t1.md5 = t2.md5
		where t2.md5 is null
		'''.format(table1=scrub(tablename1), table2=scrub(tablename2))
	c.execute(sql)
	results = c.fetchall()
	conn.close()

	return results

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
