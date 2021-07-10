import re
import pandas as pd
import ntpath

from dataclasses import dataclass

@dataclass
class HashdeepCsvHeader:
	hashdeep_version: str
	csv_column_names: list
	invoked_dir: str
	invoked_cmd: str
	line_count: int

def parse_header(hashdeepHeaderLines):
	# TODO: this is stupid. What's the Pythonic approach to a plain data object with optional fields?
	header = HashdeepCsvHeader('',[],'','',0)

	header.line_count = len(hashdeepHeaderLines)

	for line in hashdeepHeaderLines:
		match = re.search('%%%%.*(HASHDEEP-[^\s]+)', line)
		if match is not None:
			header.hashdeep_version = match.group(1)
			continue

		match = re.search('%%%% (size,.*)', line)
		if match is not None:
			header.csv_column_names = list(map(str.strip, match.group(1).split(',')))
			continue

		match = re.search('## Invoked from: (.*)', line)
		if match is not None:
			header.invoked_dir = match.group(1) or ''
			continue

		if line.startswith('## ') and line.find('Invoked') == -1:
			header.invoked_cmd = line.lstrip('## ')
			continue

	return header

def read_header(filename):
	with open(filename, 'r') as file:
		lines = []
		for line in file:
			if not line.startswith('%') and not line.startswith('#'):
				break
			lines.append(line)
	return lines

def parse_csv(header, filename):
	delimiter = ','
	# can't use pandas read_csv because of unquoted filenames with delimiter in hashdeep output
	#df = pd.read_csv(filename, names=header.csv_column_names, skiprows=header.line_count)
	rows = []
	with open(filename, 'r') as file:
		firstline = file.readline()
		if not firstline.find('HASHDEEP') > -1:
			raise RuntimeError(f'File "{filename}" is not in hashdeep csv format.'
				+ f'\nExpected firstline containing "HASHDEEP", but was "{firstline[:80]}..."')
		for line in file:
			if line.startswith('%') or line.startswith('#'):
				continue
			# assumes filename is last in output, and is the only field that contains the delimiter
			fields = line.split(delimiter, maxsplit=len(header.csv_column_names) - 1)
			data_filepath = fields.pop().replace('\n','')
			fields.append(data_filepath)

			## these extra fields double (or more) the size of the database and the execution time
			## and are of questionable value
			# relativepath = data_filepath.replace(header.invoked_dir, '')
			# fields.append(relativepath)
			# dirname = ntpath.dirname(data_filepath)
			# fields.append(dirname)

			# use ntpath as we might be processing windows filenames on linux
			# see: https://stackoverflow.com/a/8384788
			leafname = ntpath.basename(data_filepath)
			fields.append(leafname)

			rows.append(fields)

	# header.csv_column_names.append('relativepath')
	# header.csv_column_names.append('dirname')
	header.csv_column_names.append('leafname')
	
	return pd.DataFrame(data=rows, columns=header.csv_column_names)
