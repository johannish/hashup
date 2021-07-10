from util import hashdeep_csv

def info(args):
	print(f'info for {args.file}:')
	header = hashdeep_csv.parse_header(hashdeep_csv.read_header(args.file))
	dataframe = hashdeep_csv.parse_csv(header, args.file)
	print(f'columns: {dataframe.columns.values}')
	print(f'rowcount: {len(dataframe.index)}')

