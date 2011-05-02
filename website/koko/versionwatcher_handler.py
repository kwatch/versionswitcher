from __future__ import with_statement

import sys, os, re, time, datetime
traceback = None     # on-demand import

from google.appengine.ext import webapp
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from koko.versionwatcher import VersionWatcher

__all__ = ('CronResult', 'VersionWatcherHander')


class CronResult(db.Model):

    name      = db.StringProperty()
    status    = db.StringProperty()  # 'ok', 'NG', 'failed', 'error', ...
    output    = db.StringProperty(multiline=True)
    exception = db.TextProperty()
    start_at  = db.DateTimeProperty()
    stop_at   = db.DateTimeProperty()

    @classmethod
    def new(cls, name=None, status=None, output=None, exception=None, start_at=None, stop_at=None):
        if isinstance(exception, Exception):
            exception = CronResult._ex2str(exception)
        if isinstance(start_at, (float, int)):
            start_at = datetime.datetime.utcfromtimestamp(start_at)
        if isinstance(stop_at, (float, int)):
            stop_at = datetime.datetime.utcfromtimestamp(stop_at)
        return cls(name=name, status=status, output=output, exception=exception, start_at=start_at, stop_at=stop_at)

    @staticmethod
    def _ex2str(ex):
        if not ex: return None
        global traceback
        if not traceback: import traceback
        return traceback.format_exc(ex)


class VersionWatcherHandler(webapp.RequestHandler):
    """request handler class to kick VersionWatcher"""

    def get(self):
        ex = None
        status = 'ok'
        output = ""
        start_at = time.time()
        try:
            newer_versions = VersionWatcher().run()
            output = ", ".join(newer_versions)
        except Exception, ex:
            status = 'ERROR'
        finally:
            stop_at  = time.time()
        self._record(output, status, start_at, stop_at, ex)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(status == 'ERROR' and 'ERROR' or output)
        if output:
            self._report_by_mail(output)

    def _record(self, output, status, start_at, stop_at, ex):
        model = CronResult.new(name='VersionWatcher', status=status,
                               output=output, exception=ex,
                               start_at=start_at, stop_at=stop_at)
        model.put()

    def _report_by_mail(self, version):
        from google.appengine.api import mail
        email = mail.EmailMessage()
        email.sender  = "kwatch@gmail.com"
        email.subject = "Node.js new version released: %s" % (version, )
        email.to      = "Makoto Kuwata <kwatch@gmail.com>"
        email.body = (
            "Node.js new version released: %s\n"
        ) % (version, )
        email.send()


## main application
routing = [
    ('/.*', VersionWatcherHandler),
]
application = WSGIApplication(routing, debug=True)


## main routine
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
