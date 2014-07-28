# -*- coding: utf-8 -*-

###
### $Release: $
### $Copyright$
### $License$
###

from __future__ import with_statement

#from google.appengine.ext.webapp import WSGIApplication
#from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2

import sys, os


## add 'lib' into sys.path
sys.path.insert(0, os.getcwd() + '/lib')

## load apptenjin.py, config.py, and myapp.py
import config, apptenjin, myapp
if config.encoding != 'utf-8':
    import tenjin
    apptenjin.GLOBAL['to_str'] = tenjin.helpers.generate_tostrfunc(encode=config.encoding)
apptenjin.AppTenjin.config = config

## main application
routing = [
    ('/.*', myapp.MyRequestHandler),
]
app = webapp2.WSGIApplication(routing, debug=True)

### main routine
#def main():
#    run_wsgi_app(app)
#
#if __name__ == "__main__":
#    main()
