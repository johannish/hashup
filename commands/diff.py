import sys

# TODO: I really just want to import the whole module, and call it like `module.read_header`, etc
from util.files import load_file
from util.files import count
from util.files import missing_from_right

def diff(args):
	fileid_compare = load_file(args.compare)
	fileid_reference = load_file(args.reference)

	missing_from_reference = missing_from_right(fileid_compare, fileid_reference)

	if (not args.listout):
		print('row count in compare:  ', count(fileid_compare))
		print('row count in reference:', count(fileid_reference))
		print(f'missing from reference: {len(missing_from_reference)}')
	else:
		print(f'files in {args.compare} but not in {args.reference}:', file=sys.stderr)
		for m in missing_from_reference:
			print(m)
