#!/usr/bin/env python3


import cgi
import os
import urllib
import http.server


PORT = 8080


class UploadApp( http.server.BaseHTTPRequestHandler):

	script_name = '/'
	upload_path = '/tmp'
	template = """\
		<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
		<html>
			<head>
				<title>File Upload</title>
			</head>
			<body>
				<h1>File Upload</h1>
				<form action="%(script_name)s" method="POST" enctype="multipart/form-data">
					<div>
						<label>File name: <input name="payload" type="file"></label>
					</div>
					<input name="submit" type="submit" value="Upload" />
				</form>
				%(message)s
			</body>
		</html>
		"""


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def do_GET(self):
		self._render()

	def do_POST(self):
		content = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
		message = ''
		filename = content['payload'].filename
		payload = content['payload'].file
		with open(os.path.join(self.upload_path, filename.strip('.')), 'wb') as save_file:
			chunk = payload.read(1024)
			while chunk:
				save_file.write(chunk)
				chunk = payload.read(1024)
		if filename:
			message = '<div>Uploaded</div><div>%s</div>' % filename
		self._render(message)

	def _render(self, message=None):
		self.send_response(200)
		self.send_header('Content-type', 'text/html;charset=utf-8')
		self.end_headers()
		body = self.template % {'script_name': self.script_name, 'message':	message or ''}
		self.wfile.write(body.encode('utf-8'))


if __name__ == '__main__':
	http.server.HTTPServer(('', PORT), UploadApp).serve_forever()
