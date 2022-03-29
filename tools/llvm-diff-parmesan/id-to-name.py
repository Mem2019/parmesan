#!/usr/bin/python3
import sys

if len(sys.argv) != 4:
	print("Usage: python3 id-to-name.py ids.txt mapping.txt BBtargets.old.txt")
	exit(1)

with open(sys.argv[1], 'r') as fd:
	diff_bb_ids = fd.read().strip()

prefix = "Diff BB IDs: "
if diff_bb_ids.startswith(prefix):
	diff_bb_ids = diff_bb_ids[len(prefix):].strip()

diff_bb_ids = diff_bb_ids.split(' ')
diff_bb_ids = set(map(int, filter(lambda x : len(x) > 0, diff_bb_ids)))



with open(sys.argv[2], 'r') as fd:
	lines = fd.readlines()
with open(sys.argv[3], 'w') as fd:
	for line in lines:
		pair = line.split(',')
		if int(pair[1]) in diff_bb_ids:
			if '|' in pair[0]:
				print("Warning: Non-BB '%s' is selected" % pair[0])
			print(pair[0], file=fd)