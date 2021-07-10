import hashlib
import sys

# TODO: I really just want to import the whole module, and call it like `module.read_header`, etc
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_header
from util.hashdeep_csv import parse_csv
from util.database import load_dataframe
from util.database import read_count
from util.database import read_not_in_table2

def file_id(filename):
    hash_sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

dbname = 'main.db'

def load_file(hashdeep_filename):
	# TODO: don't make 3 filesystem calls here
	header = parse_header(read_header(hashdeep_filename))
	dataframe = parse_csv(header, hashdeep_filename)
	fileid = file_id(hashdeep_filename)
	_, _ = load_dataframe(dataframe, tablename=fileid, dbfilename=dbname)

	return fileid

def count(fileid):
	return read_count(fileid, dbname)

def missing_from_right(fileid_left, fileid_right):
	#TODO make this dynamic: tell the user what the available columns are, and let them pass them in
	rows = read_not_in_table2(fileid_left, fileid_right, dbname)
	filenames = [row['filename'] for row in rows]
	return filenames
