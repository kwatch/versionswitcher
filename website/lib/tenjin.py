##
## $Release: 0.9-beta $
## copyright(c) 2008-2010 kuwata-lab.com all rights reserved.
##
## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the
## "Software"), to deal in the Software without restriction, including
## without limitation the rights to use, copy, modify, merge, publish,
## distribute, sublicense, and/or sell copies of the Software, and to
## permit persons to whom the Software is furnished to do so, subject to
## the following conditions:
##
## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
## OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##

"""Very fast and light-weight template engine based embedded Python.
   See User's Guide, FAQ, and examples for details.
   http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html
   http://www.kuwata-lab.com/tenjin/pytenjin-faq.html
   http://www.kuwata-lab.com/tenjin/pytenjin-examples.html
"""

__release__  = "0.9-beta"
__license__  = "MIT License"
__all__      = ['Template', 'Engine', 'helpers', 'html', ]


import re, sys, os, time
random = marshal = pickle = memcache = unquote = None   # lazy import
python3 = sys.version_info[0] == 3
python2 = sys.version_info[0] == 2

logger = None


##
## utilities
##

def _write_binary_file(filename, content):
    global random
    f = None
    try:
        if random is None: from random import random
        tmpfile = filename + str(random())[1:]
        f = open(tmpfile, 'wb')
        f.write(content)
    finally:
        if f:
            f.close()
            os.rename(tmpfile, filename)

def _read_binary_file(filename):
    f = None
    try:
        f = open(filename, 'rb')
        return f.read()
    finally:
        if f: f.close()

if python2:

    def _read_template_file(filename, encoding=None):
        s = _read_binary_file(filename)          ## binary(=str)
        if encoding: s = s.decode(encoding)      ## binary(=str) to unicode
        return s

elif python3:

    def _read_template_file(filename, encoding=None):
        s = _read_binary_file(filename)          ## binary
        return s.decode(encoding or 'utf-8')     ## binary to unicode(=str)

def _create_module(module_name):
    """ex. mod = _create_module('tenjin.util')"""
    import types
    mod = types.ModuleType(module_name)  # or module_name.split('.')[-1] ?
    mod.__file__ = __file__
    sys.modules[module_name] = mod
    return mod



##
## helper method's module
##

if True:

    if python2:
        def generate_tostrfunc(encode=None, decode=None):
            """Generate 'to_str' function with encode or decode encoding.
               ex. generate to_str() function which encodes unicode into binary(=str).
                  to_str = tenjin.generate_tostrfunc(encode='utf-8')
                  repr(to_str(u'hoge'))  #=> 'hoge' (str)
               ex. generate to_str() function which decodes binary(=str) into unicode.
                  to_str = tenjin.generate_tostrfunc(decode='utf-8')
                  repr(to_str('hoge'))   #=> u'hoge' (unicode)
            """
            if encode:
                if decode:
                    raise ValueError("can't specify both encode and decode encoding.")
                else:
                    def to_str(val,   _str=str, _unicode=unicode, _isa=isinstance, _encode=encode):
                        """Convert val into string or return '' if None. Unicode will be encoded into binary(=str)."""
                        if _isa(val, _str):     return val
                        if val is None:                return ''
                        if _isa(val, _unicode): return val.encode(_encode)  # unicode to binary(=str)
                        return _str(val)
            else:
                if decode:
                    def to_str(val,   _str=str, _unicode=unicode, _isa=isinstance, _decode=decode):
                        """Convert val into string or return '' if None. Binary(=str) will be decoded into unicode."""
                        if _isa(val, _str):     return val.decode(_decode)  # binary(=str) to unicode
                        if val is None:         return ''
                        if _isa(val, _unicode): return val
                        return _unicode(val)
                else:
                    def to_str(val,   _str=str, _unicode=unicode, _isa=isinstance):
                        """Convert val into string or return '' if None. Both binary(=str) and unicode will be retruned as-is."""
                        if _isa(val, _str):     return val
                        if val is None:         return ''
                        if _isa(val, _unicode): return val
                        return _str(val)
            return to_str

    elif python3:
        def generate_tostrfunc(decode=None, encode=None):
            """Generate 'to_str' function with encode or decode encoding.
               ex. generate to_str() function which encodes unicode(=str) into bytes
                  to_str = tenjin.generate_tostrfunc(encode='utf-8')
                  repr(to_str('hoge'))  #=> b'hoge' (bytes)
               ex. generate to_str() function which decodes bytes into unicode(=str).
                  to_str = tenjin.generate_tostrfunc(decode='utf-8')
                  repr(to_str(b'hoge'))   #=> 'hoge' (str)
            """
            if encode:
                if decode:
                    raise ValueError("can't specify both encode and decode encoding.")
                else:
                    def to_str(val,   _str=str, _bytes=bytes, _isa=isinstance, _encode=encode):
                        """Convert val into string or return '' if None. Unicode(=str) will be encoded into bytes."""
                        if _isa(val, _str):   return val.encode(_encode)  # unicode(=str) to binary
                        if val is None:       return ''
                        if _isa(val, _bytes): return val
                        return _str(val).encode(_encode)
            else:
                if decode:
                    def to_str(val,   _str=str, _bytes=bytes, _isa=isinstance, _decode=decode):
                        """Convert val into string or return '' if None. Bytes will be decoded into unicode(=str)."""
                        if _isa(val, _str):    return val
                        if val is None:        return ''
                        if _isa(val, _bytes):  return val.decode(_decode)  # binary to unicode(=str)
                        return _str(val)
                else:
                    def to_str(val,   _str=str, _bytes=bytes, _isa=isinstance):
                        """Convert val into string or return '' if None. Both bytes and unicode(=str) will be retruned as-is."""
                        if _isa(val, _str):    return val
                        if val is None:        return ''
                        if _isa(val, _bytes):  return val
                        return _str(val)
            return to_str

    if python2:
        to_str = generate_tostrfunc(encode='utf-8')  # or encode=None?
    elif python3:
        to_str = generate_tostrfunc(decode='utf-8')

    def echo(string):
        """add string value into _buf. this is equivarent to '#{string}'."""
        frame = sys._getframe(1)
        context = frame.f_locals
        context['_buf'].append(string)

    def start_capture(varname=None):
        """start capturing with name."""
        frame = sys._getframe(1)
        context = frame.f_locals
        context['_buf_tmp'] = context['_buf']
        context['_capture_varname'] = varname
        context['_buf'] = []

    def stop_capture(store_to_context=True):
        """stop capturing and return the result of capturing.
           if store_to_context is True then the result is stored into _context[varname].
        """
        frame = sys._getframe(1)
        context = frame.f_locals
        result = ''.join(context['_buf'])
        context['_buf'] = context.pop('_buf_tmp')
        varname = context.pop('_capture_varname')
        if varname:
            context[varname] = result
            if store_to_context:
                context['_context'][varname] = result
        return result

    def captured_as(name):
        """helper method for layout template.
           if captured string is found then append it to _buf and return True,
           else return False.
        """
        frame = sys._getframe(1)
        context = frame.f_locals
        if name in context:
            _buf = context['_buf']
            _buf.append(context[name])
            return True
        return False

    def cache_as(cache_key, *options):
        def deco(func):
            def f():
                f_locals = sys._getframe().f_locals
                _buf     = f_locals.get('_buf')
                _context = f_locals.get('_context')
                _datacache = _context.get('_datacache')
                if not _datacache:
                    raise TypeError("data cache is required for cache_as()")
                fragment = _datacache.get(cache_key, *options)
                if fragment is None:
                    pos = len(_buf)
                    _context_block = _context.get('_context_block')
                    if _context_block:
                        values = _context_block(cache_key)
                        if isinstance(values, dict):
                            d.update(values)
                    fragment = ''.join(_buf[pos:])
                    _datacache.set(cache_key, fragment, *options)
                else:
                    _buf.append(fragment)
            return f
        return deco

    def cache_with(func, cache_key, *options):
        frame = sys._getframe(1)
        f_locals = frame.f_locals
        _buf     = f_locals.get('_buf')
        _context = f_locals.get('_context')
        _datacache = _context.get('_datacache')
        if not _datacache:
            raise TypeError("data cache is required for cache_with()")
        fragment = _datacache.get(cache_key, *options)
        if fragment is None:
            pos = len(_buf)
            vars = frame.f_globals.copy()
            vars.update(frame.f_locals)
            _context_block = _context.get('_context_block')
            if _context_block:
                values = _context_block(cache_key)
                if isinstance(values, dict):
                    vars.update(values)
                    #f_locals.update(values)
            sys.stderr.write("*** debug: f_globals.keys()=%s\n" % (repr(frame.f_globals.keys())))
            sys.stderr.write("*** debug: _context.keys()=%s\n" % (repr(_context.keys())))
            sys.stderr.write("*** debug: f_locals.keys()=%s\n" % (repr(f_locals.keys())))
            #exec(func.func_code, frame.f_globals, f_locals)
            exec(func.func_code, vars, vars)
            #func()
            fragment = ''.join(_buf[pos:])
            _datacache.set(cache_key, fragment, *options)
        else:
            _buf.append(fragment)

    def _p(arg):
        """ex. '/show/'+_p("item['id']") => "/show/#{item['id']}" """
        return '<`#%s#`>' % arg    # decoded into #{...} by preprocessor

    def _P(arg):
        """ex. '<b>%s</b>' % _P("item['id']") => "<b>${item['id']}</b>" """
        return '<`$%s$`>' % arg    # decoded into ${...} by preprocessor

    def _decode_params(s):
        """decode <`#...#`> and <`$...$`> into #{...} and ${...}"""
        global unquote
        if unquote is None:
            import urllib
            if   python2:  from urllib       import unquote
            elif python3:  from urllib.parse import unquote
        dct = { 'lt':'<', 'gt':'>', 'amp':'&', 'quot':'"', '#039':"'", }
        def unescape(s):
            #return s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#039;', "'").replace('&amp;',  '&')
            return re.sub(r'&(lt|gt|quot|amp|#039);',  lambda m: dct[m.group(1)],  s)
        s = to_str(s)
        s = re.sub(r'%3C%60%23(.*?)%23%60%3E', lambda m: '#{%s}' % unquote(m.group(1)), s)
        s = re.sub(r'%3C%60%24(.*?)%24%60%3E', lambda m: '${%s}' % unquote(m.group(1)), s)
        s = re.sub(r'&lt;`#(.*?)#`&gt;',   lambda m: '#{%s}' % unescape(m.group(1)), s)
        s = re.sub(r'&lt;`\$(.*?)\$`&gt;', lambda m: '${%s}' % unescape(m.group(1)), s)
        s = re.sub(r'<`#(.*?)#`>', r'#{\1}', s)
        s = re.sub(r'<`\$(.*?)\$`>', r'${\1}', s)
        return s

    mod = _create_module('tenjin.helpers')
    mod.to_str             = to_str
    mod.generate_tostrfunc = generate_tostrfunc
    mod.echo               = echo
    mod.start_capture      = start_capture
    mod.stop_capture       = stop_capture
    mod.captured_as        = captured_as
    mod.cache_with         = cache_with
    mod._p                 = _p
    mod._P                 = _P
    mod._decode_params     = _decode_params
    mod.__all__ = ['escape', 'to_str', 'echo', 'generate_tostrfunc',
                   'start_capture', 'stop_capture', 'captured_as', 'cache_with',
                   '_p', '_P', '_decode_params',
                   ]

helpers = mod
del echo, start_capture, stop_capture, captured_as, _p, _P, _decode_params
#del to_str, generate_tostrfunc
del mod


##
## module for html
##
if True:

    #_escape_table = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }
    #_escape_pattern = re.compile(r'[&<>"]')
    ##_escape_callable = lambda m: _escape_table[m.group(0)]
    ##_escape_callable = lambda m: _escape_table.__get__(m.group(0))
    #_escape_get     = _escape_table.__getitem__
    #_escape_callable = lambda m: _escape_get(m.group(0))
    #_escape_sub     = _escape_pattern.sub

    #def escape_xml(s):
    #    return s                                          # 3.02

    #def escape_xml(s):
    #    return _escape_pattern.sub(_escape_callable, s)   # 6.31

    #def escape_xml(s):
    #    return _escape_sub(_escape_callable, s)           # 6.01

    #def escape_xml(s, _p=_escape_pattern, _f=_escape_callable):
    #    return _p.sub(_f, s)                              # 6.27

    #def escape_xml(s, _sub=_escape_pattern.sub, _callable=_escape_callable):
    #    return _sub(_callable, s)                         # 6.04

    #def escape_xml(s):
    #    s = s.replace('&', '&amp;')
    #    s = s.replace('<', '&lt;')
    #    s = s.replace('>', '&gt;')
    #    s = s.replace('"', '&quot;')
    #    return s                                          # 5.83

    def escape_xml(s):
        """Escape '&', '<', '>', '"' into '&amp;', '&lt;', '&gt;', '&quot;'."""
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')   # 5.72


    def tagattr(name, expr, value=None, escape=True):
        """(experimental) Return ' name="value"' if expr is true value, else '' (empty string).
           If value is not specified, expr is used as value instead."""
        if not expr: return ''
        if value is None: value = expr
        if escape: value = escape_xml(to_str(value))
        return ' %s="%s"' % (name, value)

    def tagattrs(**kwargs):
        """(experimental) built html tag attribtes.
           ex.
           >>> tagattrs(klass='main', size=20)
           ' class="main" size="20"'
           >>> tagattrs(klass='', size=0)
           ''
        """
        if 'klass' in kwargs: kwargs['class'] = kwargs.pop('klass')
        if 'checked'  in kwargs: kwargs['checked']  = kwargs.pop('checked')  and 'checked'  or None
        if 'selected' in kwargs: kwargs['selected'] = kwargs.pop('selected') and 'selected' or None
        if 'disabled' in kwargs: kwargs['disabled'] = kwargs.pop('disabled') and 'disabled' or None
        return ''.join([' %s="%s"' % (k, escape_xml(to_str(v))) for k, v in kwargs.items() if v])

    def checked(expr):
        """return ' checked="checked"' if expr is true."""
        return expr and ' checked="checked"' or ''

    def selected(expr):
        """return ' selected="selected"' if expr is true."""
        return expr and ' selected="selected"' or ''

    def disabled(expr):
        """return ' disabled="disabled"' if expr is true."""
        return expr and ' disabled="disabled"' or ''

    def nl2br(text):
        """replace "\n" to "<br />\n" and return it."""
        if not text:
            return ''
        return text.replace('\n', '<br />\n')

    def text2html(text, _nl2br=nl2br):
        """(experimental) escape xml characters, replace "\n" to "<br />\n", and return it."""
        if not text:
            return ''
        return _nl2br(escape_xml(text).replace('  ', ' &nbsp;'))

    def nv(name, value, sep=None, _tagattrs=tagattrs, **kwargs):
        """(experimental) Build name and value attributes.
           ex.
           >>> nv('rank', 'A')
           'name="rank" value="A"'
           >>> nv('rank', 'A', '.')
           'name="rank" value="A" id="rank.A"'
           >>> nv('rank', 'A', '.', checked=True)
           'name="rank" value="A" id="rank.A" checked="checked"'
           >>> nv('rank', 'A', '.', klass='error', style='color:red')
           'name="rank" value="A" id="rank.A" class="error" style="color:red"'
        """
        s = sep and 'name="%s" value="%s" id="%s"' % (name, value, name+sep+value) \
                or  'name="%s" value="%s"'         % (name, escape_xml(value))
        return kwargs and s + _tagattrs(**kwargs) or s

    def new_cycle(*values):
        """Generate cycle object.
           ex.
             cycle = new_cycle('odd', 'even')
             print(cycle())   #=> 'odd'
             print(cycle())   #=> 'even'
             print(cycle())   #=> 'odd'
             print(cycle())   #=> 'even'
        """
        def gen(values):
            n = len(values)
            i = 0
            while True:
                yield values[i]
                i = (i + 1) % n
        if   python2:  return gen(values).next
        elif python3:  return gen(values).__next__

    mod = _create_module('tenjin.helpers.html')
    #mod._escape_table = _escape_table
    mod.escape_xml = escape_xml
    mod.escape     = escape_xml
    mod.tagattr    = tagattr
    mod.tagattrs   = tagattrs
    mod.checked    = checked
    mod.selected   = selected
    mod.disabled   = disabled
    mod.nl2br      = nl2br
    mod.text2html  = text2html
    mod.nv         = nv
    mod.new_cycle  = new_cycle

helpers.html = mod
#del escape_xml
del tagattr, tagattrs, checked, selected, disabled, nl2br, text2html, nv, new_cycle
del mod
helpers.escape = helpers.html.escape_xml



##
## Template class
##

class Template(object):
    """Convert and evaluate embedded python string.
       See User's Guide, FAQ, and examples for details.
       http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html
       http://www.kuwata-lab.com/tenjin/pytenjin-faq.html
       http://www.kuwata-lab.com/tenjin/pytenjin-examples.html
    """

    ## default value of attributes
    filename   = None
    encoding   = None
    escapefunc = 'escape'
    tostrfunc  = 'to_str'
    indent     = 4
    preamble   = None
    postamble  = None    # "_buf = []"
    smarttrim  = None    # "print ''.join(_buf)"
    args       = None
    timestamp  = None

    def __init__(self, filename=None, encoding=None, escapefunc=None, tostrfunc=None, indent=None, preamble=None, postamble=None, smarttrim=None):
        """Initailizer of Template class.

           filename:str (=None)
             Filename to convert (optional). If None, no convert.
           encoding:str (=None)
             Encoding name. If specified, template string is converted into
             unicode object internally.
             Template.render() returns str object if encoding is None,
             else returns unicode object if encoding name is specified.
           escapefunc:str (='escape')
             Escape function name.
           tostrfunc:str (='to_str')
             'to_str' function name.
           indent:int (=4)
             Indent width.
           preamble:str or bool (=None)
             Preamble string which is inserted into python code.
             If true, '_buf = []' is used insated.
           postamble:str or bool (=None)
             Postamble string which is appended to python code.
             If true, 'print "".join(_buf)' is used instead.
           smarttrim:bool (=None)
             If True then "<div>\\n#{_context}\\n</div>" is parsed as
             "<div>\\n#{_context}</div>".
        """
        if encoding   is not None:  self.encoding   = encoding
        if escapefunc is not None:  self.escapefunc = escapefunc
        if tostrfunc  is not None:  self.tostrfunc  = tostrfunc
        if indent     is not None:  self.indent     = indent
        if preamble   is not None:  self.preamble   = preamble
        if postamble  is not None:  self.postamble  = postamble
        if smarttrim  is not None:  self.smarttrim  = smarttrim
        #
        if preamble  is True:  self.preamble = "_buf = []"
        if postamble is True:  self.postamble = "print ''.join(_buf)"
        if filename:
            self.convert_file(filename)
        else:
            self._reset()

    def _reset(self, input=None, filename=None):
        self._spaces  = ''
        self.script   = None
        self.bytecode = None
        self.input    = input
        self.filename = filename
        if input != None:
            i = input.find("\n")
            if i < 0:
                self.newline = "\n"   # or None
            elif len(input) >= 2 and input[i-1] == "\r":
                self.newline = "\r\n"
            else:
                self.newline = "\n"
        self._stmt_not_added_yet = True

    def before_convert(self, buf):
        #buf.append('_buf = []; ')
        if self.preamble:
            buf.append(self.preamble)
            buf.append(self.input.startswith('<?py') and "\n" or "; ")

    def after_convert(self, buf):
        if self.postamble:
            if not buf[-1].endswith("\n"):
                buf.append("\n")
            buf.append(self.postamble + "\n")

    def convert_file(self, filename):
        """Convert file into python script and return it.
           This is equivarent to convert(open(filename).read(), filename).
        """
        input = _read_template_file(filename)
        return self.convert(input, filename)

    def convert(self, input, filename=None):
        """Convert string in which python code is embedded into python script and return it.

           input:str
             Input string to convert into python code.
           filename:str (=None)
             Filename of input. this is optional but recommended to report errors.
        """
        if python2:
            if self.encoding and isinstance(input, str):
                input = input.decode(self.encoding)
        self._reset(input, filename)
        buf = []
        self.before_convert(buf)
        self.parse_stmts(buf, input)
        self.after_convert(buf)
        script = ''.join(buf)
        self.script = script
        return script

    def compile_stmt_pattern(pi):
        return re.compile(r'<\?%s( |\t|\r?\n)(.*?) ?\?>([ \t]*\r?\n)?' % pi, re.S)

    STMT_PATTERN = None

    compile_stmt_pattern = staticmethod(compile_stmt_pattern)

    def stmt_pattern(self):
        pat = Template.STMT_PATTERN
        if not pat:   # make re.compile() to be lazy (because it is heavy weight)
            pat = Template.STMT_PATTERN = Template.compile_stmt_pattern('py')
        return pat

    def parse_stmts(self, buf, input):
        if not input:
            return
        rexp = self.stmt_pattern()
        is_bol = True
        index = 0
        for m in rexp.finditer(input):
            mspace, code, rspace = m.groups()
            #mspace, close, rspace = m.groups()
            #code = input[m.start()+4+len(mspace):m.end()-len(close)-(rspace and len(rspace) or 0)]
            text = input[index:m.start()]
            index = m.end()
            ## detect spaces at beginning of line
            lspace = None
            if text == '':
                if is_bol:
                    lspace = ''
            elif text[-1] == '\n':
                lspace = ''
            else:
                rindex = text.rfind('\n')
                if rindex < 0:
                    if is_bol and text.isspace():
                        lspace = text
                        text = ''
                else:
                    s = text[rindex+1:]
                    if s.isspace():
                        lspace = s
                        text = text[:rindex+1]
            #is_bol = rspace is not None
            ## add text, spaces, and statement
            self.parse_exprs(buf, text, is_bol)
            is_bol = rspace is not None
            if lspace:
                buf.append(lspace)
            if mspace != " ":
                #buf.append(mspace)
                buf.append(mspace == "\t" and "\t" or "\n")  # don't append "\r\n"!
            if code:
                code = self.statement_hook(code)
                self.add_stmt(buf, code)
            self._set_spaces(code, lspace, mspace)
            if rspace:
                #buf.append(rspace)
                buf.append("\n")    # don't append "\r\n"!
        rest = input[index:]
        if rest:
            self.parse_exprs(buf, rest)

    def statement_hook(self, stmt):
        """expand macros and parse '#@ARGS' in a statement."""
        if self.args is None:
            args_pattern = r'^ *#@ARGS(?:[ \t]+(.*?))?$'
            m = re.match(args_pattern, stmt)
            if m:
                arr = (m.group(1) or '').split(',')
                args = [];  declares = []
                for s in arr:
                    arg = s.strip()
                    if not s: continue
                    if not re.match('^[a-zA-Z_]\w*$', arg):
                        raise ValueError("%s: invalid template argument." % arg)
                    args.append(arg)
                    declares.append("%s = _context.get('%s'); " % (arg, arg))
                self.args = args
                return ''.join(declares)
        ##
        return stmt

    EXPR_PATTERN = None

    def expr_pattern(self):
        pat = Template.EXPR_PATTERN
        if not pat:   # make re.compile() to be lazy (because it is heavy weight)
            pat = Template.EXPR_PATTERN = re.compile(r'([#$])\{(.*?)\}', re.S)
        return pat

    def get_expr_and_escapeflag(self, match):
        return match.group(2), match.group(1) == '$'

    def parse_exprs(self, buf, input, is_bol=False):
        if not input:
            return
        if self._spaces:
            buf.append(self._spaces)
        self.start_text_part(buf)
        rexp = self.expr_pattern()
        smarttrim = self.smarttrim
        nl = self.newline
        nl_len  = len(nl)
        pos = 0
        for m in rexp.finditer(input):
            start  = m.start()
            text   = input[pos:start]
            pos    = m.end()
            expr, flag_escape = self.get_expr_and_escapeflag(m)
            #
            if text:
                self.add_text(buf, text)
                #if text[-1] == "\n":
                #    buf.append("\n")
                #    if self._spaces:
                #        buf.append(self._spaces)
            self.add_expr(buf, expr, flag_escape)
            #
            if smarttrim:
                flag_bol = text.endswith(nl) or not text and (start > 0  or is_bol)
                if flag_bol and not flag_escape and input[pos:pos+nl_len] == nl:
                    pos += nl_len
                    buf.append("\n")
        if smarttrim:
            if buf and buf[-1] == "\n":
                buf.pop()
        rest = input[pos:]
        if rest:
            self.add_text(buf, rest, True)
        self.stop_text_part(buf)
        if input[-1] == '\n':
            buf.append("\n")

    def start_text_part(self, buf):
        buf.append("_buf.extend((")

    def stop_text_part(self, buf):
        buf.append("));")

    _quote_rexp = None

    def add_text(self, buf, text, encode_newline=False):
        if not text:
            return;
        if self.encoding and python2:
            buf.append("u'''")
        else:
            buf.append("'''")
        #text = re.sub(r"(['\\\\])", r"\\\1", text)
        rexp = Template._quote_rexp
        if not rexp:   # make re.compile() to be lazy (because it is heavy weight)
            rexp = Template._quote_rexp = re.compile(r"(['\\\\])")
        text = rexp.sub(r"\\\1", text)
        if not encode_newline or text[-1] != "\n":
            buf.append(text)
            buf.append("''', ")
        elif len(text) >= 2 and text[-2] == "\r":
            buf.append(text[0:-2])
            buf.append("\\r\\n''', ")
        else:
            buf.append(text[0:-1])
            buf.append("\\n''', ")

    _add_text = add_text

    def add_expr(self, buf, code, flag_escape=None):
        if not code or code.isspace():
            return
        if flag_escape is None:
            buf.append(code); buf.append(", ");
        elif flag_escape is False:
            buf.extend((self.tostrfunc, "(", code, "), "))
        else:
            buf.extend((self.escapefunc, "(", self.tostrfunc, "(", code, ")), "))

    def add_stmt(self, buf, code):
        if self._stmt_not_added_yet:
            # insert dummy if-stmt between buf[-2] and buf[-1]
            if buf and buf[-1] != "\n" and buf[-1].isspace():
                buf[-1:-1] = ("if True: ## dummy\n", )
            self._stmt_not_added_yet = False
        if self.newline == "\r\n":
            code = code.replace("\r\n", "\n")
        buf.append(code)
        #if code[-1] != '\n':
        #    buf.append(self.newline)

    def _set_spaces(self, code, lspace, mspace):
        if lspace:
            if mspace == " ":
                code = lspace + code
            elif mspace == "\t":
                code = lspace + "\t" + code
        #i = code.rstrip().rfind("\n")
        #if i < 0:   # i == -1
        #    i = 0
        #else:
        #    i += 1
        i = code.rstrip().rfind("\n") + 1
        indent = 0
        n = len(code)
        ch = None
        while i < n:
            ch = code[i]
            if   ch == " ":   indent += 1
            elif ch == "\t":  indent += 8
            else:  break
            i += 1
        if ch:
            if code.rstrip()[-1] == ':':
                indent += self.indent
            self._spaces = ' ' * indent

    def render(self, context=None, globals=None, _buf=None):
        """Evaluate python code with context dictionary.
           If _buf is None then return the result of evaluation as str,
           else return None.

           context:dict (=None)
             Context object to evaluate. If None then new dict is created.
           globals:dict (=None)
             Global object. If None then globals() is used.
           _buf:list (=None)
             If None then new list is created.
        """
        if context is None:
            locals = context = {}
        elif self.args is None:
            locals = context.copy()
        else:
            locals = {}
            if '_engine' in context:
                context.get('_engine').hook_context(locals)
        locals['_context'] = context
        if globals is None:
            globals = sys._getframe(1).f_globals
        bufarg = _buf
        if _buf is None:
            _buf = []
        locals['_buf'] = _buf
        if not self.bytecode:
            self.compile()
        exec(self.bytecode, globals, locals)
        if bufarg is not None:
            return bufarg
        elif not logger:
            return ''.join(_buf)
        else:
            try:
                return ''.join(_buf)
            except UnicodeDecodeError:
                ex = sys.exc_info()[1]
                logger.error("[tenjin.Template] " + str(ex))
                logger.error("[tenjin.Template] (_buf=%s)" % repr(_buf))
                raise

    def compile(self):
        """compile self.script into self.bytecode"""
        self.bytecode = compile(self.script, self.filename or '(tenjin)', 'exec')


##
## preprocessor class
##

class Preprocessor(Template):
    """Template class for preprocessing."""

    STMT_PATTERN = None

    def stmt_pattern(self):
        pat = Preprocessor.STMT_PATTERN
        if not pat:   # re.compile() is heavy weight, so make it lazy
            pat = Preprocessor.STMT_PATTERN = Template.compile_stmt_pattern('PY')
        return Preprocessor.STMT_PATTERN

    EXPR_PATTERN = None

    def expr_pattern(self):
        pat = Preprocessor.EXPR_PATTERN
        if not pat:   # re.compile() is heavy weight, so make it lazy
            pat = Preprocessor.EXPR_PATTERN = re.compile(r'([#$])\{\{(.*?)\}\}', re.S)
        return Preprocessor.EXPR_PATTERN

    #def get_expr_and_escapeflag(self, match):
    #    return match.group(2), match.group(1) == '$'

    def add_expr(self, buf, code, flag_escape=None):
        if not code or code.isspace():
            return
        code = "_decode_params(%s)" % code
        Template.add_expr(self, buf, code, flag_escape)


##
## cache storages
##

class CacheStorage(object):
    """[abstract] Template object cache class (in memory and/or file)"""

    def __init__(self, postfix='.cache'):
        self.postfix = postfix
        self.items = {}    # key: full path, value: template object

    def get(self, fullpath, create_template):
        """get template object. if not found, load attributes from cache file and restore  template object."""
        template = self.items.get(fullpath)
        if not template:
            dict = self._load(fullpath)
            if dict:
                template = create_template()
                for k, v in dict.items():
                    setattr(template, k, v)
                self.items[fullpath] = template
        return template

    def set(self, fullpath, template):
        """set template object and save template attributes into cache file."""
        self.items[fullpath] = template
        dict = self._save_data_of(template)
        return self._store(fullpath, dict)

    def _save_data_of(self, template):
        return { 'args'  : template.args,   'bytecode' : template.bytecode,
                 'script': template.script, 'timestamp': template.timestamp }

    def unset(self, fullpath):
        """remove template object from dict and cache file."""
        self.items.pop(fullpath, None)
        return self._delete(fullpath)

    def clear(self):
        """remove all template objects and attributes from dict and cache file."""
        for k, v in self.items.items():
            self._delete(k)
        self.items.clear()

    def _load(self, fullpath):
        """(abstract) load dict object which represents template object attributes from cache file."""
        raise NotImplementedError.new("%s#_load(): not implemented yet." % self.__class__.__name__)

    def _store(self, fullpath, template):
        """(abstract) load dict object which represents template object attributes from cache file."""
        raise NotImplementedError.new("%s#_store(): not implemented yet." % self.__class__.__name__)

    def _delete(self, fullpath):
        """(abstract) remove template object from cache file."""
        raise NotImplementedError.new("%s#_delete(): not implemented yet." % self.__class__.__name__)

    def _cachename(self, fullpath):
        """change fullpath into cache file path."""
        return fullpath + self.postfix


class MemoryCacheStorage(CacheStorage):

    def _load(self, fullpath):
        return None

    def _store(self, fullpath, template):
        pass

    def _delete(self, fullpath):
        pass


class FileCacheStorage(CacheStorage):

    def _delete(self, fullpath):
        cachepath = self._cachename(fullpath)
        if os.path.isfile(cachepath): os.unlink(cachepath)


class MarshalCacheStorage(FileCacheStorage):

    def __init__(self, postfix='.cache'):
        global marshal
        if marshal is None: import marshal
        FileCacheStorage.__init__(self, postfix)

    def _load(self, fullpath):
        cachepath = self._cachename(fullpath)
        if not os.path.isfile(cachepath): return None
        if logger: logger.info("[tenjin.MarshalCacheStorage] load cache (file=%s)" % repr(cachepath))
        dump = _read_binary_file(cachepath)
        return marshal.loads(dump)

    def _store(self, fullpath, dict):
        cachepath = self._cachename(fullpath)
        if logger: logger.info("[tenjin.MarshalCacheStorage] store cache (file=%s)" % repr(cachepath))
        _write_binary_file(cachepath, marshal.dumps(dict))


class PickleCacheStorage(FileCacheStorage):

    def __init__(self, postfix='.cache'):
        global pickle
        if pickle is None:
            try:    import cPickle as pickle
            except: import pickle
        FileCacheStorage.__init__(self, postfix)

    def _load(self, fullpath):
        cachepath = self._cachename(fullpath)
        if not os.path.isfile(cachepath): return None
        if logger: logger.info("[tenjin.PickleCacheStorage] load cache (file=%s)" % repr(cachepath))
        dump = _read_binary_file(cachepath)
        return pickle.loads(dump)

    def _store(self, fullpath, dict):
        if 'bytecode' in dict: dict.pop('bytecode')
        cachepath = self._cachename(fullpath)
        if logger: logger.info("[tenjin.PickleCacheStorage] store cache (file=%s)" % repr(cachepath))
        _write_binary_file(cachepath, pickle.dumps(dict))


class TextCacheStorage(FileCacheStorage):

    def _load(self, fullpath):
        cachepath = self._cachename(fullpath)
        if not os.path.isfile(cachepath): return None
        if logger: logger.info("[tenjin.TextCacheStorage] load cache (file=%s)" % repr(cachepath))
        s = _read_binary_file(cachepath)
        if python2:
            header, script = s.split("\n\n", 1)
        elif python3:
            header, script = s.split("\n\n".encode('ascii'), 1)
            header = header.decode('ascii')
        timestamp = encoding = args = None
        for line in header.split("\n"):
            key, val = line.split(": ", 1)
            if   key == 'timestamp':  timestamp = float(val)
            elif key == 'encoding':   encoding  = val
            elif key == 'args':       args      = val.split(', ')
        if python2:
            if encoding: script = script.decode(encoding)   ## binary(=str) to unicode
        elif python3:
            script = script.decode(encoding or 'utf-8')     ## binary to unicode(=str)
        return {'args': args, 'script': script, 'timestamp': timestamp}

    def _store(self, fullpath, dict):
        s = dict['script']
        if python2:
            if dict.get('encoding') and isinstance(s, unicode):
                s = s.encode(dict['encoding'])           ## unicode to binary(=str)
        sb = []
        sb.append("timestamp: %s\n" % dict['timestamp'])
        if dict.get('encoding'):
            sb.append("encoding: %s\n" % dict['encoding'])
        if dict.get('args') is not None:
            sb.append("args: %s\n" % ', '.join(dict['args']))
        sb.append("\n")
        sb.append(s)
        s = ''.join(sb)
        if python3:
            if isinstance(s, str):
                s = s.encode(dict.get('encoding') or 'utf-8')   ## unicode(=str) to binary
        cachepath = self._cachename(fullpath)
        if logger: logger.info("[tenjin.TextCacheStorage] store cache (file=%s)" % repr(cachepath))
        _write_binary_file(cachepath, s)

    def _save_data_of(self, template):
        dict = FileCacheStorage._save_data_of(self, template)
        dict['encoding'] = template.encoding
        return dict


class GaeMemcacheCacheStorage(CacheStorage):

    lifetime = 0     # 0 means unlimited

    def __init__(self, lifetime=None, postfix='.cache'):
        CacheStorage.__init__(self, postfix)
        if lifetime is not None:  self.lifetime = lifetime
        global memcache
        if memcache is None: from google.appengine.api import memcache

    def _load(self, fullpath):
        key = self._cachename(fullpath)
        if logger: logger.info("[tenjin.GaeMemcacheCacheStorage] load cache (key=%s)" % repr(key))
        return memcache.get(key)

    def _store(self, fullpath, dict):
        if 'bytecode' in dict: dict.pop('bytecode')
        key = self._cachename(fullpath)
        if logger: logger.info("[tenjin.GaeMemcacheCacheStorage] store cache (key=%s)" % repr(key))
        ret = memcache.set(key, dict, self.lifetime)
        if not ret:
            if logger: logger.info("[tenjin.GaeMemcacheCacheStorage: failed to store cache (key=%s)" % repr(key))

    def _delete(self, fullpath):
        memcache.delete(self._cachename(fullpath))



##
## abstract class for data cache
##
class DataCache(object):

    def get(self, cache_key, *options):
        raise NotImplementedError("%s.get(): not implemented yet." % self.__class__.__name__)

    def set(self, cache_key, data, *options):
        raise NotImplementedError("%s.set(): not implemented yet." % self.__class__.__name__)

    def delete(self, cache_key, *options):
        raise NotImplementedError("%s.del(): not implemented yet." % self.__class__.__name__)

    def has(self, cache_key, *options):
        raise NotImplementedError("%s.has(): not implemented yet." % self.__class__.__name__)


##
## file base data cache
##
class FileBaseDataCache(DataCache):

    def __init__(self, root_path):
        if not os.path.isdir(root_path):
            raise ArgumentError("%s: directory not found." % root_path)
        self.root_path = root_path

    _pat = re.compile(r'[^-\/\w]')

    def filepath(self, cache_key, _pat1=_pat):
        return os.path.join(self.root_path, _pat1.sub('_', cache_key))

    def get(self, cache_key, lifetime=0):
        fpath = self.filepath(cache_key)
        if not os.path.isfile(fpath):
            return
        if lifetime and os.path.getmtime(fpath) + lifetime <= time.time():
            return
        return _read_binary_file(fpath)

    def set(self, cache_key, data, lifetime=0):
        fpath = self.filepath(cache_key)
        dirname = os.path.dirname(fpath)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        _write_binary_file(fpath, data)

    def delete(self, cache_key, lifetime=0):
        fpath = self.filepath(cache_key)
        if os.path.isfile(fpath):
            os.unlink(fpath)
            return True
        return False

    def has(self, cache_key, lifetime=0):
        fpath = self.filepath(cache_key)
        if not os.path.isfile(fpath): return False
        if linetime: return os.path.getmtime(fpath) + lifetime <= time.time()
        return True



##
## template engine class
##

class Engine(object):
    """Template Engine class.
       See User's Guide, FAQ, and examples for details.
       http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html
       http://www.kuwata-lab.com/tenjin/pytenjin-faq.html
       http://www.kuwata-lab.com/tenjin/pytenjin-examples.html
    """

    ## default value of attributes
    prefix     = ''
    postfix    = ''
    layout     = None
    templateclass = Template
    path       = None
    cache      = None
    datacache  = None
    preprocess = False
    timestamp_interval = 5  # seconds
    _cache_storage_classes = {
        'marshal': MarshalCacheStorage,
        'pickle' : PickleCacheStorage,
        'text'   : TextCacheStorage,
    }

    def __init__(self, prefix=None, postfix=None, layout=None, path=None, cache=True, datacache=None, preprocess=None, templateclass=None, **kwargs):
        """Initializer of Engine class.

           prefix:str (='')
             Prefix string used to convert template short name to template filename.
           postfix:str (='')
             Postfix string used to convert template short name to template filename.
           layout:str (=None)
             Default layout template name.
           path:list of str(=None)
             List of directory names which contain template files.
           cache:bool or 'text' (=True)
             Cache converted python code into file.
             If True, marshal-base cache files are created.
             If 'text', text-base cache files are created.
             If False, no cache files are created.
           preprocess:bool(=False)
             Activate preprocessing or not.
           templateclass:class (=Template)
             Template class which engine creates automatically.
           kwargs:dict
             Options for Template class constructor.
             See document of Template.__init__() for details.
        """
        if prefix:  self.prefix = prefix
        if postfix: self.postfix = postfix
        if layout:  self.layout = layout
        if templateclass: self.templateclass = templateclass
        if path  is not None:  self.path = path
        if datacache: self.datacache = datacache
        if preprocess is not None: self.preprocess = preprocess
        self.kwargs = kwargs
        self.encoding = kwargs.get('encoding')
        self._filepaths = {}   # template_name => relative path and absolute path
        #self.cache = cache
        self._set_cache_storage(cache)

    def _set_cache_storage(self, cache):
        if   cache is True:  self.cache = MarshalCacheStorage()
        elif cache is None:  self.cache = MemoryCacheStorage()
        elif cache is False: self.cache = None
        elif isinstance(cache, CacheStorage):  self.cache = cache
        elif self._cache_storage_classes.get(cache):
            self.cache = self._cache_storage_classes[cache]()
        else:
            raise ValueError("%s: invalid cache object." % repr(cache))

    def to_filename(self, template_name):
        """Convert template short name to filename.
           ex.
             >>> engine = tenjin.Engine(prefix='user_', postfix='.pyhtml')
             >>> engine.to_filename('list')
             'list'
             >>> engine.to_filename(':list')
             'user_list.pyhtml'
        """
        if template_name[0] == ':' :
            return self.prefix + template_name[1:] + self.postfix
        return template_name

    def _relative_and_absolute_path(self, template_name):
        pair = self._filepaths.get(template_name)
        if pair: return pair
        filename = self.to_filename(template_name)
        filepath = self._find_file(filename)
        if not filepath:
            raise IOError('%s: filename not found (path=%s).' % (filename, repr(self.path)))
        fullpath = os.path.abspath(filepath)
        self._filepaths[template_name] = pair = (filepath, fullpath)
        return pair

    def _find_file(self, filename):
        if self.path:
            for dirname in self.path:
                filepath = os.path.join(dirname, filename)
                if os.path.isfile(filepath):
                    return filepath
        else:
            if os.path.isfile(filename):
                return filename
        return None

    def _create_template(self, filepath, _context, _globals):
        if filepath and self.preprocess:
            s = self._preprocess(filepath, _context, _globals)
            template = self.templateclass(None, **self.kwargs)
            template.convert(s, filepath)
        else:
            template = self.templateclass(filepath, **self.kwargs)
        return template

    def _preprocess(self, filepath, _context, _globals):
        #if _context is None: _context = {}
        #if _globals is None: _globals = sys._getframe(3).f_globals
        if '_engine' not in _context:
            self.hook_context(_context)
        preprocessor = Preprocessor(filepath)
        return preprocessor.render(_context, globals=_globals)

    def get_template(self, template_name, _context=None, _globals=None):
        """Return template object.
           If template object has not registered, template engine creates
           and registers template object automatically.
        """
        filename, fullpath = self._relative_and_absolute_path(template_name)
        assert filename and fullpath
        cache = self.cache
        template = cache and cache.get(fullpath, self.templateclass) or None
        mtime = None
        now = time.time()
        if template:
            assert template.timestamp is not None
            if now > getattr(template, '_last_checked_at', 0) + self.timestamp_interval:
                mtime = os.path.getmtime(filename)
                if template.timestamp != mtime:
                    #if cache: cache.delete(path)
                    template = None
                    if logger: logger.info("[tenjin.Engine] cache is old (filename=%s, template=%s)" % (repr(filename), repr(template)))
        if not template:
            if not mtime: mtime = os.path.getmtime(filename)
            if self.preprocess:   ## required for preprocess
                if _context is None: _context = {}
                if _globals is None: _globals = sys._getframe(1).f_globals
            template = self._create_template(filename, _context, _globals)
            template.timestamp = mtime
            template._last_checked_at = now
            if cache:
                if not template.bytecode: template.compile()
                cache.set(fullpath, template)
        #else:
        #    template.compile()
        return template

    def include(self, template_name, append_to_buf=True):
        """Evaluate template using current local variables as context.

           template_name:str
             Filename (ex. 'user_list.pyhtml') or short name (ex. ':list') of template.
           append_to_buf:boolean (=True)
             If True then append output into _buf and return None,
             else return stirng output.

           ex.
             <?py include('file.pyhtml') ?>
             #{include('file.pyhtml', False)}
             <?py val = include('file.pyhtml', False) ?>
        """
        frame = sys._getframe(1)
        locals  = frame.f_locals
        globals = frame.f_globals
        assert '_context' in locals
        context = locals['_context']
        # context and globals are passed to get_template() only for preprocessing.
        template = self.get_template(template_name, context, globals)
        if append_to_buf:  _buf = locals['_buf']
        else:              _buf = None
        return template.render(context, globals, _buf=_buf)

    def render(self, template_name, context=None, context_block=None, globals=None, layout=True):
        """Evaluate template with layout file and return result of evaluation.

           template_name:str
             Filename (ex. 'user_list.pyhtml') or short name (ex. ':list') of template.
           context:dict (=None)
             Context object to evaluate. If None then new dict is used.
           globals:dict (=None)
             Global context to evaluate. If None then globals() is used.
           layout:str or Bool(=True)
             If True, the default layout name specified in constructor is used.
             If False, no layout template is used.
             If str, it is regarded as layout template name.

           If temlate object related with the 'template_name' argument is not exist,
           engine generates a template object and register it automatically.
        """
        if context is None:
            context = {}
        if globals is None:
            globals = sys._getframe(1).f_globals
        self.hook_context(context)
        context['_context_block'] = context_block
        while True:
            # context and globals are passed to get_template() only for preprocessing
            template = self.get_template(template_name, context, globals)
            content  = template.render(context, globals)
            layout   = context.pop('_layout', layout)
            if layout is True or layout is None:
                layout = self.layout
            if not layout:
                break
            template_name = layout
            layout = False
            context['_content'] = content
        context.pop('_content', None)
        return content

    def hook_context(self, context):
        context['_engine'] = self
        #context['render'] = self.render
        context['include'] = self.include
        context['_datacache'] = self.datacache
