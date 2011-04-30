# -*- coding: utf-8 -*-

###
### $Release: $
### $Copyright$
### $License$
###

from __future__ import with_statement

from google.appengine.ext import webapp

import sys, os, re, logging
from UserDict import UserDict


class AppTenjin(object):
    try:
        import config
    except LoadError:
        ## dummy class to simulate config object
        class config(object):
            encoding        = 'utf-8'
            layout_template = '_layout.html.pyt'
            analytics_id    = None
            template_path   = ['htdocs', 'tmpl']

    root    = os.getcwd()
    version = '$Release: 0.0.0 $'.split(' ')[1]
    is_dev  = (os.getenv("SERVER_SOFTWARE") or "").startswith("Development")
    if is_dev:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging

del logging


## load tenjin
import tenjin
from tenjin.helpers import *
from tenjin.helpers.html import *
from my_template import MyTemplate
#if AppTenjin.config.encoding != 'utf-8':
#    to_str = tenjin.helpers.generate_tostrfunc(encode=AppTenjin.config.encoding)
tenjin.logger = AppTenjin.logger
shared_cache = tenjin.GaeMemcacheCacheStorage()
engine = tenjin.Engine(path=AppTenjin.config.template_path, cache=shared_cache,
                       layout=AppTenjin.config.layout_template, templateclass=MyTemplate)


##
class Script(tenjin.Template):
    """execute script using Tenjin mechanism"""

    def convert(self, input, filename=None):
        self._reset(input, filename)
        self.script = input
        return input


## change tenjin.Engine class to generate Script object for script (*.cgi)
def _create_template(self, filepath, _context, _globals):
    if filepath and self.preprocess:
        s = self._preprocess(filepath, _context, _globals)
        template = self.templateclass(None, **self.kwargs)
        template.convert(s, filepath)
    else:
        #template = self.templateclass(filepath, **self.kwargs)
        klass = filepath.endswith('.cgi') and Script or self.templateclass
        template = klass(filepath, **self.kwargs)
    return template
tenjin.Engine._create_template = _create_template


##
class ExitException(Exception):
    """dummy exception class to stop request handler gracefully"""
    pass


##
class DefaultRequestHandler(webapp.RequestHandler):
    """request handler class for AppTenjin"""

    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.engine  = engine
        self.context = UserDict()
        self.context['self'] = self

    def before(self):
        pass

    def after(self):
        pass

    def handle(self):
        self.before()
        path = self.request.path  # or path_info
        assert path[0] == '/'
        htdocs_path = AppTenjin.root + '/htdocs'
        filepath = htdocs_path + path
        if os.path.isdir(filepath):
            if not filepath.endswith('/'):
                permanent = True
                self.redirect(path + '/', permanent)
                self.after()
                return
            filepath += 'index.html'
        html = None
        if os.path.exists(filepath) and not path.endswith(('.pyt', '.cgi')):
            with open(filepath) as f:
                html = f.read()
        elif os.path.exists(filepath + '.pyt'):
            template_filename = filepath[len(htdocs_path)+1:] + '.pyt'
            flag_layout = filepath.endswith('.html')  # False when '.xml' or '.json'
            html = engine.render(template_filename, self.context, layout=flag_layout)
        else:
            if path.endswith('.cgi') and os.path.exists(filepath):
                script_path = filepath
            else:
                script_path = self.find_script('htdocs', path)
            if script_path:
                self.context['_engine'] = engine
                tmpl = Script(script_path)
                tmpl.render(self.context)
                html = ""    # script should send html by self.response.out.write()
            else:
                self.response.set_status(404)
                self.context['message'] = "%s: not found" % self.request.path
                html = engine.render("404.html.pyt", self.context)
        ## response body
        self.response.out.write(html)
        self.after()

    def find_script(self, base, path):
        _isfile = os.path.isfile
        for item in path.split('/')[1:]:
            base = '%s/%s' % (base, item)
            script = base + '.cgi'
            if _isfile(script):
                return script
        return None

    def exit(self):
        raise ExitException()

    def handle_exception(self, exception, debug_mode):
        if isinstance(exception, ExitException):
            pass
        else:
            webapp.RequestHandler.handle_exception(self, exception, debug_mode)
        self.after()

    def use_layout_template(self, layout_filename):
        self.context['_layout'] = layout_filename

    #get    = handle
    #post   = handle
    #put    = handle
    #delete = handle
    #head   = handle
    def get(self):     self.handle()
    def post(self):    self.handle()
    def put(self):     self.handle()
    def delete(self):  self.handle()
    def head(self):    self.handle()


## global variables
GLOBAL = globals()
