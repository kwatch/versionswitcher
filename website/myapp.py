# -*- coding: utf-8 -*-

###
### $Release: $
### $Copyright$
### $License$
###

from __future__ import with_statement

from google.appengine.api import users
import apptenjin


##
## You can add your own functions available in templates
##
escape = apptenjin.GLOBAL['escape']

def js_link(label, js):
    return '<a href="javascript:undefined" onclick="%s">%s</a>' % (escape(js), label)
apptenjin.GLOBAL['js_link'] = js_link

def url_link(label, url):
    if url:  return '<a href="%s">%s</a>' % (escape(url), label)
    else:    return '<span>%s</span>' % label
apptenjin.GLOBAL['url_link'] = url_link


##
## You can add helper methods to handler class
##
class MyRequestHandler(apptenjin.DefaultRequestHandler):
    """you can customize this class"""

    #def new_context(self):
    #    context = apptenjin.DefaultRequestHandler.new_context(self)
    #    context.site_title = 'Your Site Title'
    #    return context

    def current_lang(self):
        lang = getattr(self, '_lang', None)
        if not lang:
            lang = self._current_lang()
            self._lang = lang
        return lang

    def _current_lang(self):
        lang = self.request.method == 'GET' and self.request.GET.get('_lang')
        if lang and lang.isalpha():
            self.response.headers['Set-Cookie'] = '_lang=%s; path=/' % lang
            return lang
        lang = self.request.cookies.get('_lang')
        if lang:
            return lang
        langs = self.request.accept_language.best_matches()
        if langs:
            return langs[0]
        return 'en'

    def current_user(self):
        return users.get_current_user()

    def current_user_name(self):
        user = users.get_current_user()
        return (user.nickname if user else None)
