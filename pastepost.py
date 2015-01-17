#!/usr/bin/env python

import web
import json

class Server:
    filename = None
    def config(self, filename):
        """ read the config from a file """
        self.filename = filename
        pass

    def sanitize(self, input_string):
        """ make it safe to present """
        pass

    def make_paste(self, input_string):
        """ write paste to disk """
        self.get_filename(input_string)
        pass

    def get_filename(self, input_string):
        """ take md5sum of message as the paste id """
        pass

