import sys

from util import files

def diff(args):
	fileid_compare = files.load_file(args.compare)
	fileid_reference = files.load_file(args.reference)

	missing_from_reference = files.missing_from_right(fileid_compare, fileid_reference)

	if (not args.listout):
		print('row count in compare:  ', files.count(fileid_compare))
		print('row count in reference:', files.count(fileid_reference))
		print(f'missing from reference: {len(missing_from_reference)}')
	else:
		print(f'files in {args.compare} but not in {args.reference}:', file=sys.stderr)
		for m in missing_from_reference:
			print(m)
