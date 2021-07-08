# TODO: I really just want to import the whole module, and call it like `module.read_header`, etc
from util.hashdeep_csv import read_header
from util.hashdeep_csv import parse_header
from util.hashdeep_csv import parse_csv

def info(args):
	print(f'info for {args.file}:')
	header = parse_header(read_header(args.file))
	dataframe = parse_csv(header, args.file)
	print(f'columns: {dataframe.columns.values}')
	print(f'rowcount: {len(dataframe.index)}')

