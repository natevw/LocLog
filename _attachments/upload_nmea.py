import sys
from uuid import uuid4

from helpers import _transport

files = sys.argv[1:]



class Sentence(object):
    def __init__(self, line):
        if not line[0] == '$':
            raise AssertionError("Sentence must start with $")
        line = line.strip()[1:]
        
        if line[-3] == '*':
            checksum = int(line[-2:], 16)
            line = line[:-3]
            linesum = reduce(lambda a,b: a^ord(b), line, 0)
            if linesum != checksum:
                raise AssertionError("Line checksum was not matched")
        
        fields = line.split(',')
        self.talker = fields[0][:2]
        self.type = fields[0][2:]
        self.fields = fields[1:]

for file in files:
    
    line_number = 0
    for line in open(file):
        line_number += 1
        try:
            s = Sentence(line)
        except AssertionError as e:
            if line.strip():
                print "Skipping line %u. (%s)" % (line_number, e)
            continue
        print s.talker, s.type, s.fields
        