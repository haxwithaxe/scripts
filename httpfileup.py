#!/usr/bin/env python3


import cgi
import os
import http.server
import logging

# pylint: disable=mixed-indentation
# Defaults
PORT = 8080
ADDRESS = ''
SAVE_PATH = '/tmp'
SCRIPT_PATH = '/'
CLIENT_ID_HEADER = 'CLIENT-ID'

# Character replacement map for cleaning filenames
CLEAN_MAP = {'#': '', '?': '', '\\': '', '$': '', '*': '', '/': '.', ' ': '_'}

MESSAGE_TEMPLATE = '''\
    <div>Uploaded</div><div><div><table>
    <tr><th>Client</th><th>Uploaded</th><th>To</th></tr>
    <tr><td>%(client_id)s</td><td>%(upload_filename)s</td><td>%(save_filename)s</td></tr>
    </table></div>
    '''

FORM_TEMPLATE = '''\
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
            <head>
                <title>File Upload</title>
            </head>
            <body>
                <h1>File Upload</h1>
                <form action="%(script_name)s" method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="webform" value="true" />
                    <div>
                        <label>File name: <input name="payload" type="file"></label>
                    </div>
                    <input name="submit" type="submit" value="Upload" />
                </form>
                %(message)s
                <div>
                    <h5>Examlpes</h5>
                    <div>
                        PUT multiple files
                        <p><pre>curl -l -T "{tmp,hello.txt}" http://127.0.0.1:8080</pre></p>
                    </div>
                </div>
            </body>
        </html>
        '''


def sanitize_pathname(pathname):
    """Try to prevent trivial directory traversal attacks and annoying filenames."""
    for d, c in CLEAN_MAP.items():
        pathname = pathname.replace(d, c)
    return pathname.strip('.')


class Transfer:
    """ Transfer an uploaded file to disk.

    Arguments:
        save_file (file, optional): The file handle to save to.
        upload_file (file): The file handle of the uploaded file.
        content_length (int): The "Content-Length" header from the request.

    """
    def __init__(self, save_file=None, upload_file=None, content_length=None):
        self.logger = logging.getLogger(name=self.__class__.__name__)
        self.save_file = save_file
        self.upload_file = upload_file
        self.content_length = content_length
        self.remaining_length = content_length
        self._chunk_size = 1024

    def __log_reading_bytes(self):
        self.logger.debug('reading %s bytes', self.chunk_size)

    def __log_read_bytes(self):
        self.logger.debug('read so far %s/%s', self.content_length-self.remaining_length, self.content_length)

    def read_chunk(self):
        self.__log_reading_bytes()
        chunk = self.upload_file.read(self.chunk_size)
        self.__log_read_bytes()
        self.remaining_length -= self.chunk_size
        return chunk

    def write_chunk(self, chunk):
        wrote_bytes = self.save_file.write(chunk)
        self.logger.debug('wrote %s bytes', wrote_bytes)

    def __call__(self, save_file=None):
        """Save the downloaded file to disk.

        Arguments:
            save_file (file, optional): The file handle to save to. This is required if it was not passed in the
                constructor.

        """
        if save_file:
            self.save_file = save_file
        chunk = self.read_chunk()
        while chunk:
            self.write_chunk(chunk)
            chunk = self.read_chunk()

    @property
    def chunk_size(self):
        """Return the chunk size in bytes that best fits the amount of data left to download."""
        if self.remaining_length == 0:
             self._chunk_size = 0
        elif (self.remaining_length % self._chunk_size == 0 or
                self.remaining_length % self._chunk_size != self.remaining_length):
            if self.remaining_length > 1024:
                self._chunk_size = 1024
            elif self.remaining_length > 64:
                self._chunk_size = 64
        elif self.remaining_length % self._chunk_size == self.remaining_length:
            self._chunk_size = self.remaining_length
        return self._chunk_size


class UploadApp(http.server.SimpleHTTPRequestHandler):
    """ HTTP request handler that provides file upload facilities.
    
    Arguments:
        response_values (dict): Default values to pass to the templates.
        message (str): The formatted message.
        script_name (str): The path part of the URL of the "script".
        client_id (str): Client ID. Hostname, IP, or "X-Client-Id" header value.
        upload_filename (str): The name of the file being uploaded.
        save_filename (str): The name of the file where the uploaded file is being saved.
        save_dirname (str): The directory where the uploaded file is being saved.

    """

    logger = None
    save_path = '/tmp'
    use_client_dirs = False
    response_values = {'message': '', 'script_name': None, 'client_id': None, 'upload_filename': None, 'save_filename': None, 'save_dirname': None}
    upload_file = None
    paths = {'path': '/', 'path': '/files'}
    template = FORM_TEMPLATE
    serve_index = False

    @classmethod
    def new(cls, script_name=None, save_path=None, template=None, logger_name='httpfileup', use_client_dirs=None, response_values=None, serve_index=False):
        """Get a configured subclass of UploadApp.

        Arguments:
            script_name (str): . Defaults to '/'.
            save_path (str): Base path to save the files to.
            template (str): A template using % dictionary syntax for completion.
            logger_name (str): The name of the logging.Logger instance. Defaults to 'httpfileup'.
            use_client_dirs (bool): Use separate directories for each client if True.
            response_values (dict): Default values to be passed to the templates.
            serve_index (bool): Serve an index of files that have been uploaded.

        """

        class _UploadApp(cls):
            pass
        _UploadApp.logger = logging.getLogger(name=logger_name)
        _UploadApp.save_path = save_path or cls.save_path
        _UploadApp.template = template or cls.template
        _UploadApp.response_values.update(response_values or {})
        _UploadApp.response_values['script_name'] = script_name or SCRIPT_PATH
        _UploadApp.serve_index = serve_index
        if use_client_dirs is not None:
            _UploadApp.use_client_dirs = use_client_dirs
        return _UploadApp

    def do_GET(self):
        if self.path == self.paths['form']:
            self._render()
        elif self.serve_index and self.path == self.paths['index']:
            super().do_GET()

    @property
    def save_dirname(self):
        if not self.client_id:
            raise AttributeError('missing client_id')
        save_dirname = self.save_path
        if self.use_client_dirs:
            save_dirname = os.path.join(self.save_path, sanitize_pathname(self.client_id))
        self.response_values['save_dirname'] = save_dirname
        return save_dirname

    @property
    def save_filename(self):
        if not self.upload_filename:
            raise AttributeError('missing upload_filename')
        save_filename = os.path.join(self.save_dirname, sanitize_pathname(self.upload_filename))
        self.response_values['save_filename'] = save_filename
        return save_filename

    def do_PUT(self):
        self.logger.debug('do_PUT')
        self.client_id = self.headers.get(CLIENT_ID_HEADER, self.client_address[0])
        self.upload_filename = os.path.basename(self.path)
        self.logger.debug('client_id = %s, upload_filename = %s', self.client_id, self.upload_filename)
        self.upload_file = self.rfile
        try:
            self._handle_file_upload(
                    self.upload_filename, self.rfile, self.save_dirname, self.save_filename
                    )
        except Exception as err:
            self.logger.error(err, exc_info=True)
            self.send_response_only(500, 'Server Error')
        self.logger.info('%s uploaded %s to %s', self.client_id, self.upload_filename, self.save_filename)
        self.send_response_only(204, 'No Content')
        self.end_headers()

    def do_POST(self):
        """Handle Post Request."""
        content = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        self.response_values['message'] = ''
        is_webform = bool(content.getvalue('webform', False))
        self.client_id, self.response_values['client_id'] = content.getvalue('client_id', self.client_address[0])
        self.logger.debug('client_id: %s', self.client_id)
        payload = content.getvalue('payload')
        self.logger.debug(repr(payload))
        self.upload_filename = payload.filename
        self.upload_file = payload.file
        self._handle_file_upload(
                    self.upload_filename,
                    self.upload_file,
                    self.save_dirname,
                    self.save_filename
                    )
        self.logger.info(
                    '%s uploaded %s to %s',
                    self.client_id,
                    self.upload_filename,
                    self.save_filename
                    )
        if is_webform:
            message = MESSAGE_TEMPLATE % self.response_values
            self._render(message)
        else:
            self.send_response_only(204, 'No Content')
            self.end_headers()

    def list_directory(self, path):
        print('path', path)
        return super().translate_path(os.path.join(self.save_path, path))

    def _handle_file_upload(self, upload_filename, upload_file, save_dirname, save_filename):
        content_length = int(self.headers.get('Content-Length', 64))
        self.logger.info('_handle_file_upload: filename = %s, content-length = %s', upload_filename, content_length)
        if not os.path.exists(save_dirname):
            os.makedirs(save_dirname, exist_ok=True)
        transfer = Transfer(upload_file=upload_file, content_length=content_length)
        with open(save_filename, 'wb') as save_file:
            transfer(save_file)

    def _render(self, message=None, status=200):
        self.response_values[message] = message or ''
        self.send_response(status)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers()
        body = self.template % self.response_values
        self.wfile.write(body.encode('utf-8'))

    def __getattr__(self, attr):
        if attr in self.response_values:
            return self.response_values[attr]
        raise AttributeError(attr) # Raise native AttributeError

    def __setattr__(self, attr, value):
        if attr in self.response_values:
            self.response_values[attr] = value
        else:
            super().__setattr__(attr, value) # Raise native AttributeError



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default=ADDRESS)
    parser.add_argument('-p', '--port', type=int, default=PORT)
    parser.add_argument('-b', '--by-client', default=False, action='store_true')
    parser.add_argument('-d', '--save-path', default=SAVE_PATH)
    parser.add_argument('-s', '--script-path', default=SCRIPT_PATH)
    parser.add_argument('-t', '--template', type=argparse.FileType('r'), default=None)
    parser.add_argument('--debug', default=False, action='store_true')
    parser.add_argument('--index', default=False, action='store_true', help='Serve an index of the uploaded files.')
    args = parser.parse_args()
    config = {'script_name': args.script_path, 'save_path': args.save_path, 'use_client_dirs': args.by_client, 'serve_index': args.index}
    if args.template:
        config['template'] = args.template.read()
    print('address =', args.address or '0.0.0.0', 'port =', args.port)
    logging.basicConfig(level={True: logging.DEBUG, False: logging.INFO}[args.debug])
    http.server.HTTPServer((args.address, args.port), UploadApp.new(**config)).serve_forever()
