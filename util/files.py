import hashlib
import sys

from util import hashdeep_csv
from util import database

def file_id(filename):
    hash_sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

dbname = 'main.db'

def load_file(hashdeep_filename):
	# TODO: don't make 3 filesystem calls here
	header = hashdeep_csv.parse_header(hashdeep_csv.read_header(hashdeep_filename))
	dataframe = hashdeep_csv.parse_csv(header, hashdeep_filename)
	fileid = file_id(hashdeep_filename)
	_, _ = database.load_dataframe(dataframe, tablename=fileid, dbfilename=dbname)

	return fileid

def count(fileid):
	return database.read_count(fileid, dbname)

def missing_from_right(fileid_left, fileid_right):
	#TODO make this dynamic: tell the user what the available columns are, and let them pass them in
	rows = database.read_not_in_table2(fileid_left, fileid_right, dbname)
	filenames = [row['filename'] for row in rows]
	return filenames
