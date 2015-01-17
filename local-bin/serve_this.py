#!/usr/bin/env python

__authors__ = ['haxwithaxe <me@haxwithaxe.net>']

__license__ = 'CC0'

import SimpleHTTPServer
import SocketServer
import os
import sys

if len(sys.argv) > 1:
	path = ''.join(sys.argv[1:])
	os.chdir(path)
	print(path)

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
