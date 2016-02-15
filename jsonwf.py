#!/usr/bin/env python

# check if json is well formed (ala xmlwf)

import json
import sys

with open(sys.argv[1], 'r') as fobj:
	json.load(fobj)
