# -*- coding: utf-8 -*-

###
### $Release: $
### $Copyright$
### $License$
###

from __future__ import with_statement

import sys, os, re, logging, time

from google.appengine.ext import webapp
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

## add 'lib' into sys.path
libpath = os.getcwd() + '/lib'
if sys.path[0] != libpath:
    sys.path.insert(0, libpath)
import apptenjin
from apptenjin import AppTenjin
from tenjin.helpers import to_str, escape


def rfc1123_gmt(int_time):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(int_time))


_MIME_TYPE = {
    'html': 'text/html',
    'htm':  'text/html',
    'jpg':  'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif':  'image/gif',
    'png':  'image/png',
    'txt':  'text/plain',
    'text': 'text/plain',
    'css':  'text/css',
    'js':   'applicatin/x-javascript',
    'sh':   'text/plain',
    'csh':  'text/plain',
}

def guess_content_type(filepath):
    suffix = filepath.split('.')[-1]
    return _MIME_TYPE.get(suffix)


class StaticFileHandler(webapp.RequestHandler):
    """request handler class for static files"""

    ROOT = 'static'

    def handle(self):
        ## get request path
        path = self.request.path  # or path_info
        assert path[0] == '/'
        filepath = self.ROOT + path
        ## add 'index.html' if directory is requested
        if os.path.isdir(filepath):
            if not filepath.endswith('/'):
                permanent = True
                self.redirect(path + '/', permanent)
                return
            filepath += 'index.html'
        ## get content
        if os.path.exists(filepath):
            content = self._read_content(filepath)
        else:
            self.response.set_status(404, "Not Found")
            context = {'message': "%s: not found" % path }
            content = apptenjin.engine.render("404.html.pyt", context)
        ## write response body
        self.response.out.write(content)

    def _read_content(self, filepath):
        ## set Content-Type
        self.response.headers['Content-Type'] = guess_content_type(filepath)
        ## set Last-Modified
        mtime = os.path.getmtime(filepath)
        last_modified = rfc1123_gmt(mtime)
        self.response.headers['Last-Modified'] = last_modified
        ## return dummy content when HEAD method
        if self.request.method == 'HEAD':
            #self.response.headers['Content-Lenght'] = os.path.getsize(filepath)
            return " " * os.path.getsize(filepath)
        ## return empty content when not modified
        since = self.request.headers.get('If-Modified-Since')
        not_modified = since == last_modified
        if not_modified:
            self.response.set_status(304, "Not Modified")
            return ""
        ## return file content
        self.response.headers['Cache-Control'] = 'private'
        with open(filepath) as f:
            return f.read()

    get = post = put = delete = head = handle


## main application
routing = [
    ('/.*', StaticFileHandler),
]
application = WSGIApplication(routing, debug=True)


## main routine
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
