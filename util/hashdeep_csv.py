import re

from dataclasses import dataclass

@dataclass
class HashdeepCsvHeader:
	hashdeep_version: str
	csv_column_names: list
	invoked_dir: str
	invoked_cmd: str

def parse_header(hashdeepHeaderLines):
	# TODO: this is stupid. What's the Pythonic approach to a plain data object with optional fields?
	header = HashdeepCsvHeader('','','','')

	for line in hashdeepHeaderLines:
		match = re.search('%%%%.*(HASHDEEP-[^\s]+)', line)
		if match is not None:
			header.hashdeep_version = match.group(1)
			continue

		match = re.search('%%%% (size,.*)', line)
		if match is not None:
			header.csv_column_names = match.group(1)
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
