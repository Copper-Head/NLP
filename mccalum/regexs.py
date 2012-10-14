#!/sw/bin/python
import re
import sys

#print 'regex', sys.argv[1]
#print 'files', sys.argv[2:]

r = re.compile(sys.argv[1]);

for filename in sys.argv[2:]:
    file = open(filename,'r')
    for line in file.xreadlines():
	if r.search(line):
	    print filename, '***', line,
