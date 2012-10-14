#!/usr/bin/python
import re
import sys
import dicts

if sys.argv[1] == '-h':
    print 'usage:', sys.argv[0], 'regex files...'
    print 'The regular expression must contain a group, i.e. parentheses.'
    print "For example: python regexcount.py '\bwent (\w+)\b' *.txt"

r = re.compile(sys.argv[1]);
counts = dicts.DefaultDict(0)

if len(sys.argv) < 3:
    sys.argv += '-'

for filename in sys.argv[2:]:
    if filename == '-':
	file = sys.stdin
    else:
	file = open(filename,'r')
    for line in file.xreadlines():
	iterator = r.finditer(line)
        found = False
        for match in iterator:
            found = True
            if match.group(1):
                counts[match.group(1)] += 1
        if found:  print filename, '***', line,

print counts.sorted()[:50]
