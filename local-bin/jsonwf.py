#!/usr/bin/env python

# check if json is well formed (ala xmlwf)

import json,sys

def file2str(fname):
	fobj = open(fname,'r')
	ret = fobj.read()
	fobj.close()
	return ret

print(json.loads(file2str(sys.argv[1])))
