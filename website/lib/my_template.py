##
## parse template with recognizing '#endfor', '#endif', and so on.
##
## ex:
##   import tenjin
##   from tenjin.helpers import *
##   from my_template import MyTemplate
##   engine = tenjin.Engine(templateclass=MyTemplate)
##   print("------------- script")
##   print(engine.get_template("file.pyhtml").script)
##   print("------------- output")
##   print(engine.render("file.pyhtml")
##

import re
import tenjin


class TemplateSyntaxError(Exception):
    pass


def _args2dict(*args):
    return dict([ (w, w) for w in args ])

START_WORDS = _args2dict('for', 'if', 'while', 'def', 'try:', 'with', 'class')
END_WORDS   = _args2dict('#endfor', '#endif', '#endwhile', '#enddef', '#endtry', '#endwith', '#endclass')
CONT_WORDS  = _args2dict('elif', 'else:', 'except', 'except:', 'finally:')


class MyTemplate(tenjin.Template):

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
            #if lspace:
            #    buf.append(lspace)
            #if mspace != " ":
            #    #buf.append(mspace)
            #    buf.append(mspace == "\t" and "\t" or "\n")  # don't append "\r\n"!
            if code:
                code = self.statement_hook(code)
                self.add_stmt(buf, code)
            #self._set_spaces(code, lspace, mspace)
            #if rspace:
            #    #buf.append(rspace)
            #    buf.append("\n")    # don't append "\r\n"!
        rest = input[index:]
        if rest:
            self.parse_exprs(buf, rest)

    def parse_exprs(self, buf, input, is_bol=False):
        buf2 = []
        tenjin.Template.parse_exprs(self, buf2, input, is_bol)
        if buf2:
            buf.append(''.join(buf2))

    def add_stmt(self, buf, code):
        if not code: return
        lines = code.splitlines(True)   # keep "\n"
        if lines[-1][-1] != "\n":
            lines[-1] = lines[-1] + "\n"
        buf.extend(lines)

    def after_convert(self, buf):
        tenjin.Template.after_convert(self, buf)
        block = self.parse_lines(buf)
        buf[:] = []
        self._join_block(block, buf, 0)

    depth = -1

    ##
    ## ex.
    ##   input = r"""
    ##   if items:
    ##   _buf.extend(('<ul>\n', ))
    ##   i = 0
    ##   for item in items:
    ##   i += 1
    ##   _buf.extend(('<li>', to_str(item), '</li>\n', ))
    ##   #endfor
    ##   _buf.extend(('</ul>\n', ))
    ##   #endif
    ##   """[1:]
    ##   lines = input.splitlines()
    ##   block = self.parse_lines(lines)
    ##      #=>  [ "if items:\n",
    ##             [ "_buf.extend(('<ul>\n', ))\n",
    ##               "i = 0\n",
    ##               "for item in items:\n",
    ##               [ "i += 1\n",
    ##                 "_buf.extend(('<li>', to_str(item), '</li>\n', ))\n",
    ##               ],
    ##               "#endfor\n",
    ##               "_buf.extend(('</ul>\n', ))\n",
    ##             ],
    ##             "#endif\n",
    ##           ]
    def parse_lines(self, lines):
        block = []
        try:
            self._parse_lines(lines.__iter__(), False, block)
        except StopIteration:
            if self.depth > 0:
                raise TemplateSyntaxError("unexpected EOF.")
        else:
            #raise TemplateSyntaxError("unexpected syntax.")
            pass
        return block

    def _parse_lines(self, iter, end_block, block=None):
        if block is None: block = []
        START_WORDS_ = START_WORDS
        END_WORDS_   = END_WORDS
        CONT_WORDS_  = CONT_WORDS
        while True:
            line = iter.next()
            m = re.search(r'\S+', line)
            if not m:
                block.append(line)
                continue
            word = m.group(0)
            if word in END_WORDS_:
                if word != end_block:
                    raise TemplateSyntaxError("'%s' exptexted buf got '%s'." % (end_block, word))
                return block, line, False
            elif line.endswith(':\n'):
                if word in CONT_WORDS_:
                    return block, line, True
                elif word in START_WORDS_:
                    block.append(line)
                    self.depth += 1
                    child_block, line, has_sibling = self._parse_lines(iter, '#end'+word)
                    block.extend((child_block, line, ))
                    while has_sibling:
                        child_block, line, has_sibling = self._parse_lines(iter, '#end'+word)
                        block.extend((child_block, line, ))
                    self.depth -= 1
                else:
                    block.append(line)
            else:
                block.append(line)
        assert "unreachable"

    #def join_block(self, block):
    #    buf = []
    #    depth = 0
    #    self._join_block(block, buf, depth)
    #    return ''.join(buf)

    def _join_block(self, block, buf, depth):
        indent = '    ' * depth
        for line in block:
            if isinstance(line, list):
                self._join_block(line, buf, depth+1)
            else:
                buf.append(indent + line.lstrip())


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        template = MyTemplate(filename)
        print(template.script)
    else:    # test
        input = r"""
<html>
  <body>
  <?py if items: ?>
    <table>
    <?py i = 0 ?>
    <?py for item in items: ?>
    <?py   i += 1 ?>
    <?py   klass = i % 2 and 'odd' or 'even' ?>
      <tr class="#{klass}">
        <td>#{i}</li>
        <td>${item}</li>
      </tr>
    <?py else: ?>
      <p>nothing.</p>
    <?py #endfor ?>
    </table>
  <?py else: ?>
    <p>Not found.</p>
  <?py #endif ?>
  </body>
</html>
"""[1:]
        expected = r"""
_buf.extend(('''<html>
  <body>\n''', ));
if items:
    _buf.extend(('''    <table>\n''', ));
    i = 0
    for item in items:
        i += 1
        klass = i % 2 and 'odd' or 'even'
        _buf.extend(('''      <tr class="''', to_str(klass), '''">
        <td>''', to_str(i), '''</li>
        <td>''', escape(to_str(item)), '''</li>
      </tr>\n''', ));
    else:
        _buf.extend(('''      <p>nothing.</p>\n''', ));
    #endfor
    _buf.extend(('''    </table>\n''', ));
else:
    _buf.extend(('''    <p>Not found.</p>\n''', ));
#endif
_buf.extend(('''  </body>
</html>\n''', ));
"""[1:]
        #
        template = MyTemplate()
        actual = template.convert(input)
        assert expected == actual
        #print(actual)
        #import pprint
        #pprint.pprint(result)

        ## if-statement
        input = r"""
<?py for x in nums: ?>
<?py if x > 0: ?>
<p>Positive.</p>
<?py elif x < 0: ?>
<p>Negative.</p>
<?py else: ?>
<p>Zero.</p>
<?py #endfor ?>
<?py #endfor ?>
"""[1:]
        expected = r"""
for x in nums:
    if x > 0:
        _buf.extend(('''<p>Positive.</p>\n''', ));
    elif x < 0:
        _buf.extend(('''<p>Negative.</p>\n''', ));
    else:
        _buf.extend(('''<p>Zero.</p>\n''', ));
    #endif
#endfor
"""[1:]
        actual = template.convert(input)
        assert expected == actual

