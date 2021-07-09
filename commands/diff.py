import sys

# TODO: I really just want to import the whole module, and call it like `module.read_header`, etc
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_header
from util.hashdeep_csv import parse_csv
from util.database import load_dataframe
from util.database import read_count
from util.database import read_not_in_table2

def diff(args):
	print(f'files in {args.compare} but not in {args.reference}:', file=sys.stderr)
	header = parse_header(read_header(args.compare))
	dataframe = parse_csv(header, args.compare)
	dbfname, tablename_compare = load_dataframe(dataframe)

	header = parse_header(read_header(args.reference))
	dataframe = parse_csv(header, args.reference)
	_, tablename_reference = load_dataframe(dataframe, dbfilename=dbfname)

	print('row count in compare:  ', read_count(tablename_compare, dbfname))
	print('row count in reference:', read_count(tablename_reference, dbfname))

	missing_from_reference = read_not_in_table2(tablename_compare, tablename_reference, dbfname)
	print(f'not in reference: {missing_from_reference}')
