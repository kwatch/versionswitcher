from __future__ import with_statement

import sys, os, re, time
from glob import glob
urllib2 = None   # on-demand import



release = prop('release', '0.0.0')
DEBUG   = prop('debug', False)

def _debug(msg):
    if DEBUG:
        sys.stderr.write("\033[0;31m*** debug: %s\033[0m\n" % (msg, ))


@recipe
def task_update(c):
    """update 'website/static' according current branch name"""
    branch_name = current_branch_name()
    if branch_name.startswith('rel-'):
        task_update_sh(c)
    elif branch_name == 'master':
        task_update_files(c)
    #elif branch_name.startswith('dev-'):
    #    for x in ['versionswitcher.sh', 'install.sh', 'bootstrap.sh']:
    #        rm_f(c%"website/static/scripts/$(x)")
    #        system(c%"ln scripts/$(x) website/static/scripts/$(x)")
    else:
        assert False, "branch_name=%r" % branch_name


@recipe
@ingreds('create_dirs')
def task_update_files(c):
    """update 'website/static/{versions,installers}/*'"""
    for x in ('website/static/versions', 'website/static/installers'):
        os.path.isdir(x) or mkdir(x)
    fnames = []
    fnames.extend(glob("versions/*.txt"))
    fnames.extend(glob("installers/*.sh"))
    for fname in fnames:
        src_fname = fname
        dst_fname = "website/static/" + fname
        with open(src_fname) as f:
            src = f.read()
        if os.path.isfile(dst_fname):
            with open(dst_fname) as f:
                dst = f.read()
            dst = re.sub(r'\$Date:.*?\$', '$Date: $', dst, 1)
            flag_eq = src == dst
        else:
            flag_eq = False
        if flag_eq:
            print("(not updated) " + dst_fname)
        if not flag_eq:
            print("(UPDATED)     " + dst_fname)
            mtime = os.path.getmtime(src_fname)
            iso8601 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mtime))
            dst = re.sub(r'\$Date: \$', '$Date: %s $' % iso8601, src)
            with open(dst_fname, 'w')  as f:
                f.write(dst)
            os.utime(dst_fname, (mtime, mtime))


@recipe
@ingreds('create_dirs')
def task_update_sh(c):
    """update 'website/static/versionswitcher.sh'"""
    fnames = []
    fnames.extend(glob("scripts/*.sh"))
    fnames.extend(glob("hooks/*.sh"))
    for x in fnames:
        base = os.path.basename(x)
        cp_p(x, "website/static/"+x)


@recipe
def task_create_dirs(c):
    for x in ["scripts", "versions", "installers", "hooks"]:
        dirpath = "website/static/" + x
        if not os.path.isdir(dirpath):
            mkdir_p(dirpath)


def current_branch_name():
    f = os.popen("git branch")
    output = f.read()
    status = f.close()
    m = re.compile(r'^\* (.+)$', re.M).search(output)
    return m.group(1).strip()


@recipe
def task_edit(c):
    """update release number on files"""
    fnames = ['README.rst', 'scripts/*.sh']
    replacer = [
        (r'(:Release:\s+)\S+', lambda m: m.group(1) + release),
        (r'\$Release:.*?\$', '$Release: %s $' % release),
    ]
    edit(fnames, by=replacer)
    fnames = ['website/tmpl/_sidebar.html.pyt']
    replacer = [
        (r'\(version \d+\.\d+\.\d+\)', r'(version %s)' % (release,)),
    ]
    edit(fnames, by=replacer)


@recipe
@spices("-o: override 'versions/LANG.txt' when changed", "-D:", "[LANG...]")
def task_check(c, *args, **kwargs):
    """check versions of node.js, ruby, and python"""
    if not args: args = ['node', 'ruby', 'python', 'lua', 'luajit', 'pypy', 'rubinius']
    flag_overwrite = bool(kwargs.get('o'))
    gvars = globals()
    pairs = []
    for lang in args:
        classname = lang.capitalize() + 'Checker'
        classobj = gvars.get(classname)
        if not classobj:
            raise ValueError("%s: unsupported language name." % lang)
        pairs.append((lang, classobj))
    for lang, classobj in pairs:
        sys.stdout.write("- %s: " % lang)
        checker = classobj(flag_overwrite)
        #checker.run()
        fetched_versions, known_versions = checker.run()
        if kwargs.get('D'):
            text = checker.build_text(fetched_versions)
            sys.stdout.write("--------------------\n")
            sys.stdout.write(text)
            sys.stdout.write("--------------------\n")


class Checker(object):

    filename = None
    overwrite = False

    def __init__(self, overwrite=False):
        self.overwrite = overwrite

    def run(self):
        known_versions   = self.get_known_versions()
        fetched_versions = self.fetch_versions()
        self.compare(fetched_versions, known_versions)
        if self.overwrite:
            text = self.build_text(fetched_versions)
            assert text, "text should not be empty but it is: %r" % (text,)
            with open(self.filename, 'w') as f:
                f.write(text)
        return fetched_versions, known_versions

    def compare(self, fetched_versions, known_versions):
        if sorted(fetched_versions) == sorted(known_versions):
            print("not changed.")
        else:
            set1, set2 = set(fetched_versions), set(known_versions)
            print("new versions: %s" % ', '.join(set1 - set2))
            print("disappeared: %s" % ', '.join(set2 - set1))
            if self.overwrite:
                text = self.build_text(fetched_versions)
                with open(self.filename, 'w') as f:
                    f.write(text)

    def get_known_versions(self):
        with open(self.filename) as f:
            content = f.read()
        return content.split()

    version_rexp = re.compile(r'href=".*?-(\d+\.\d+(?:\.\d+)?).*?\.(?:tar\.gz|tar\.bz2|tgz)"')

    def fetch_versions(self):
        rexp = self.version_rexp
        html = self.fetch_page(self.url)
        versions = [ m.group(1) for m in rexp.finditer(html) ]
        return versions

    def fetch_page(self, url):
        global urllib2
        if not urllib2: import urllib2
        f = urllib2.urlopen(url)
        content = f.read()
        f.close()
        return content

    def page_exists(self, url):
        global urllib2
        if not urllib2: import urllib2
        f = None
        ex = None
        try:
            f = urllib2.urlopen(url)
        except urllib2.HTTPError:
            ex = sys.exc_info()[1]
        finally:
            if f: f.close()
        return not ex

    def normalize(self, ver):
        return ".".join("%03d" % int(d.group(0)) for d in re.finditer(r'\d+', ver))

    def build_text(self, versions):
        vers = sorted(versions, key=self.normalize, reverse=True)
        vers.append("")
        return "\n".join(vers)


class RubyChecker(Checker):

    filename = "versions/ruby.txt"
    url = "http://www.ring.gr.jp/archives/lang/ruby/"
    version_rexp = re.compile(r'href="ruby-(\d+\.\d+\.\d+(?:-p?\d.*?)?)\.tar.gz"')

    def fetch_versions(self):
        rexp = self.version_rexp
        versions = []
        for ver in ('1.8', '1.9'):
            html = self.fetch_page(self.url + ver + '/')
            versions.extend( m.group(1) for m in rexp.finditer(html) )
        return versions

    def build_text(self, versions):
        vals = {}
        for ver in sorted(versions, key=self.normalize, reverse=True):
            key = ver.split('-')[0]
            vals.setdefault(key, []).append(ver)
        pop = vals.pop
        rows = []
        rows.append(pop('1.9.2'))
        rows.append(pop('1.9.1') + [''] + pop('1.9.0'))
        rows.append(pop('1.8.7'))
        rows.append(pop('1.8.6'))
        rows.append(pop('1.8.5') + ['']
                    + pop('1.8.4') + pop('1.8.3') + pop('1.8.2')
                    + pop('1.8.1') + pop('1.8.0'))
        assert not vals, "vals is expected to be empty but it is: %r" % vals
        #length = max( len(row) for row in rows )
        #for row in rows:
        #    for i in range(length - len(row)):
        #        row.append('')
        #map(lambda *args: list(args), *rows)
        #transposed = map(lambda *args: [ x or "" for x in args ], *rows)
        buf = []
        for row in map(None, *rows):
            cols = ( '%-15s' % (s or '') for s in row )
            buf.append(''.join(cols).rstrip() + "\n")
        return "".join(buf)


class PythonChecker(Checker):

    filename = "versions/python.txt"
    url = "http://www.python.org/ftp/python/"
    version_rexp = re.compile(r'href="(\d\.\d(?:\.\d)?)/?"')

    def compare(self, fetched_versions, known_versions):
        set1, set2 = set(fetched_versions), set(known_versions)
        for ver in set1 - set2:
            if not self._is_released(ver):
                _debug("%s is removed because not released yet." % (ver,))
                fetched_versions.remove(ver)
        return Checker.compare(self, fetched_versions, known_versions)

    def fetch_versions(self):
        return [ ver.count('.') == 1 and ver + '.0' or ver
                   for ver in Checker.fetch_versions(self)
                   if self.normalize(ver) >= '002.002' ]

    def _is_released(self, version):
        ver = version.count('.') > 1 and re.sub(r'\.0$', '', version) or version
        #url = self.url + '%s/Python-%s.tar.bz2' % (ver, ver)
        #_debug("url=%r" % (url,))
        #return self.page_exists(url)
        url = 'http://www.python.org/download/releases/%s/' % (ver,)
        try:
            content = self.fetch_page(url)
        except urllib2.HTTPError:
            _debug('failed to open %s' % url)
            return False
        else:
            path = "/ftp/python/%s/Python-%s.tar.bz2" % (ver, ver)
            ret = ('href="%s"' % path) in content
            ret or _debug('href="Python-%s.tar.bz2" is not found in content' % ver)
            return ret

    def build_text(self, versions):
        vals = {}
        for ver in sorted(versions, key=self.normalize, reverse=True):
            key = ver[0:3]
            vals.setdefault(key, []).append(ver)
        pop = vals.pop
        rows = []
        rows.append(pop('3.2') + [''] + pop('3.1') + [''] + pop('3.0'))
        rows.append(pop('2.7') + [''] + pop('2.6'))
        rows.append(pop('2.5') + [''] + pop('2.4'))
        rows.append(pop('2.3') + [''] + pop('2.2'))
        assert not vals, "vals is expected to be empty but it is: %r" % vals
        buf = []
        for row in map(None, *rows):
            cols = ( '%-10s' % (s or '') for s in row )
            buf.append(''.join(cols).rstrip() + "\n")
        return "".join(buf)


class NodeChecker(Checker):

    filename = "versions/node.txt"
    url = "http://nodejs.org/dist/"
    version_rexp = re.compile(r'href="(?:node-)?v(\d+\.\d+(?:\.\d+)?)(?:/|\.tar.gz|\.tar.bz2)"')

    def fetch_versions(self):
        return [ ver for ver in Checker.fetch_versions(self)
                     if self.normalize(ver) > '000.004.003' ]


class LuaChecker(Checker):

    filename = "versions/lua.txt"
    url = "http://www.lua.org/ftp/"
    version_rexp = re.compile(r'(?:HREF|href)="lua-(\d+\.\d+(?:\.\d+)?)\.tar\.gz"')

    def fetch_versions(self):
        return [ ver for ver in Checker.fetch_versions(self)
                     if self.normalize(ver) >= '003.000' ]

    def compare(self, fetched_versions, known_versions):
        tweaked = [ re.sub(r'\.0$', '', v) for v in known_versions ]
        return Checker.compare(self, fetched_versions, tweaked)


class LuajitChecker(Checker):

    filename = "versions/luajit.txt"
    url = "http://luajit.org/download.html"
    version_rexp = re.compile(r'href="download/LuaJIT-(\d+\.\d+(?:\.\d+)?(?:-beta\d+)?)\.tar\.gz"')

    def fetch_versions(self):
        versions = []
        for version in Checker.fetch_versions(self):
            ver = self.normalize(version)
            if ver < '001.001.006':
                continue
            if '002' <= ver and ver <= '002.000.000.005':
                continue
            versions.append(version)
        return versions


class PypyChecker(Checker):

    filename = "versions/pypy.txt"
    url = "http://pypy.org/download/"
    version_rexp = re.compile(r'href="pypy-(\d+\.\d+(?:\.\d+)?)-src\.tar.bz2"')

    def fetch_versions(self):
        return [ ver for ver in Checker.fetch_versions(self)
                     if self.normalize(ver) >= '001.004' ]

    def compare(self, fetched_versions, known_versions):
        tweaked = [ re.sub(r'\.0$', '', v) for v in known_versions ]
        return Checker.compare(self, fetched_versions, tweaked)


class RubiniusChecker(Checker):

    filename = "versions/rubinius.txt"
    url = "http://rubini.us/releases/"
    version_rexp = re.compile(r'href="/releases/(\d+\.\d+(?:\.\d+)?)/"')

    def fetch_versions(self):
        return [ ver for ver in Checker.fetch_versions(self)
                     if self.normalize(ver) >= '001.002.003' ]
