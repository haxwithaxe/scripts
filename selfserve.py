#!/usr/bin/env python3.3
import sys
import socketserver
import threading
import http.server
import logging

def init_logging(file_name='selfserve.log', level=logging.DEBUG):
	logging.basicConfig(filename=file_name, level=level, filemode='w')
	logging.info('new instance')
	return logging

def _is_cgi(path, dir_name, file_name):
	'''insert conditions here
		
		return boolean
	'''

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass

def _url_collapse_path(path):
    """
    Given a URL path, remove extra '/'s and '.' path elements and collapse
    any '..' references and returns a colllapsed path.

    Implements something akin to RFC-2396 5.2 step 6 to parse relative paths.
    The utility of this function is limited to is_cgi method and helps
    preventing some security attacks.

    Returns: A tuple of (head, tail) where tail is everything after the final /
    and head is everything before it.  Head will always start with a '/' and,
    if it contains anything else, never have a trailing '/'.

    Raises: IndexError if too many '..' occur within the path.

    """
    # Similar to os.path.split(os.path.normpath(path)) but specific to URL
    # path semantics rather than local operating system semantics.
    path_parts = path.split('/')
    head_parts = []
    for part in path_parts[:-1]:
        if part == '..':
            head_parts.pop() # IndexError if more '..' than prior parts
        elif part and part != '.':
            head_parts.append( part )
    if path_parts:
        tail_part = path_parts.pop()
        if tail_part:
            if tail_part == '..':
                head_parts.pop()
                tail_part = ''
            elif tail_part == '.':
                tail_part = ''
    else:
        tail_part = ''

    splitpath = ('/' + '/'.join(head_parts), tail_part)
    collapsed_path = "/".join(splitpath)

    return collapsed_path


class CustomCGIHandler(http.server.CGIHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		self.logger = logging.getLogger(__name__)
		super(CustomCGIHandler, self).__init__(request, client_address, server)

	def is_cgi(self):
		collapsed_path = _url_collapse_path(self.path)
		dir_sep = collapsed_path.find('/', 1)
		head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep+1:]
		if _is_cgi(self.path, head, tail):
			self.cgi_info = head, tail
			return True
		return False

	def log_request(self, code='-', size='-'):
		"""Log an accepted request.

		This is called by send_response().
		"""
		msg = '"%s" %s %s' % (self.requestline, str(code), str(size))
		self.logger.debug(msg)

	def log_error(self, format, *args):
		"""Log an error.

		This is called when a request cannot be fulfilled.  By
		default it passes the message on to log_message().

		Arguments are the same as for log_message().

		XXX This should go to the separate error log.

		"""
		msg = self.log_msg_fmt(format, *args)
		self.logger.error(msg)

	def log_msg_fmt(self, format, *args):
		msg = "%s - - [%s] %s\n" % (self.address_string(),
				self.log_date_time_string(),
				format%args)
		return msg

	def log_message(self, format, *args):
		"""Log an arbitrary message.

		This is used by all other logging functions.  Override
		it if you have specific logging wishes.

		The first argument, FORMAT, is a format string for the
		message to be logged.  If the format string contains
		any % escapes requiring parameters, they should be
		specified as subsequent arguments (it's just like
		printf!).

		The client ip and current date/time are prefixed to
		every message.
		"""
		msg = self.log_msg_fmt(format, *args)
		self.logger.info(msg)

def usage(script_name):
	usage = '''%s [--host <hostname/ip>] [--port <port number>]'''
	print(usage % script_name)

def main(args):
	init_logging()
	port=8080
	host=''
	'''if '-h' in args or '--help' in args or '/?' in args:
		usage(args[0])
		sys.exit(1)
	if '--port' in args:
		port_index = args.index('--port')
		if len(args) > port_index+1:
			port = int(args[port_index+1], 10)
	if '--host' in args:
		host_index = args.index('--host')
		if len(args) > host_index+1:
			port = args[host_index+1]'''
	msg = 'running server on: %s:%s' % (host, str(port))
	print(msg)
	logging.info(msg)
	server = ThreadingHTTPServer((host, port), CustomCGIHandler)
	server_thread = threading.Thread(target=server.serve_forever)
	try:
		logging.debug('running server')
		server_thread.start()
		logging.debug('server running')
	except KeyboardInterrupt:
		logging.debug('stopping server')
		server.shutdown()

if __name__ == '__main__':
	main(sys.argv)

