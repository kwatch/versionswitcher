from __future__ import with_statement

import sys, os, re, time
from glob import glob
urllib2 = None   # on-demand import



release = prop('release', '0.0.0')


@recipe
def task_update(c):
    """update 'website/static' according current branch name"""
    branch_name = current_branch_name()
    if branch_name.startswith('rel-'):
        task_update_sh(c)
    elif branch_name == 'master':
        task_update_files(c)
    else:
        assert False, "branch_name=%r" % branch_name


@recipe
@ingreds('create_dirs')
def task_update_files(c):
    """update 'website/static/{versions,script}/*'"""
    fnames = []
    fnames.extend(glob("versions/*.txt"))
    fnames.extend(glob("scripts/*.sh"))
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
    fname = 'versionswitcher.sh'
    cp_p(fname, 'website/static')


@recipe
def task_create_dirs(c):
    for x in ["website/static/versions", "website/static/scripts"]:
        if not os.path.isdir(x):
            mkdir_p(x)


def current_branch_name():
    f = os.popen("git branch")
    output = f.read()
    status = f.close()
    m = re.compile(r'^\* (.+)$', re.M).search(output)
    return m.group(1).strip()


@recipe
def task_edit(c):
    """update release number on files"""
    fname = 'README.rst'
    replacer = [
        (r'(:Release:\s+)\S+', lambda m: m.group(1) + release),
        (r'\$Release:.*?\$', '$Release: %s $' % release),
    ]
    edit('README.rst', 'versionswitcher.sh', by=replacer)


@recipe
@spices("-o: override 'versions/LANG.txt' when changed", "-D:", "[LANG...]")
def task_check(c, *args, **kwargs):
    """check versions of node.js, ruby, and python"""
    if not args: args = ['node', 'ruby', 'python']
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

    def fetch_versions(self):
        raise NotImplementedError("%s.fetch_versions(): not implemented yet." % self.__class__.__name__)

    def fetch_page(self, url):
        global urllib2
        if not urllib2: import urllib2
        f = urllib2.urlopen(url)
        content = f.read()
        f.close()
        return content

    def normalize(self, ver):
        return ".".join("%03d" % int(d.group(0)) for d in re.finditer(r'\d+', ver))


class NodeChecker(Checker):

    filename = "versions/node.txt"
    url = "http://nodejs.org/dist/"

    def fetch_versions(self):
        rexp = re.compile(r'href="node-v(\d+\.\d+(?:\.\d+)?)\.tar.(?:gz|bz2)"')
        html = self.fetch_page(self.url)
        versions = [ m.group(1) for m in rexp.finditer(html) ]
        versions = [ ver for ver in versions if self.normalize(ver) > '000.004.003' ]
        return versions

    def build_text(self, versions):
        vers = sorted(versions, key=self.normalize, reverse=True)
        vers.append("")
        return "\n".join(vers)


class RubyChecker(Checker):

    filename = "versions/ruby.txt"
    url = "http://www.ring.gr.jp/archives/lang/ruby/"

    def fetch_versions(self):
        rexp = re.compile(r'href="ruby-(\d+\.\d+\.\d+(?:-p?\d.*?)?)\.tar.gz"')
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

    def compare(self, fetched_versions, known_versions):
        set1, set2 = set(fetched_versions), set(known_versions)
        for ver in set1 - set2:
            if not self._is_released(ver):
                fetched_versions.remove(ver)
        return Checker.compare(self, fetched_versions, known_versions)

    def fetch_versions(self):
        rexp = re.compile(r'href="(\d\.\d(?:\.\d)?)/?"')
        html = self.fetch_page(self.url)
        versions = [ m.group(1) for m in rexp.finditer(html) ]
        return [ ver.count('.') == 1 and ver + '.0' or ver
                   for ver in versions if self.normalize(ver) >= '002.002']

    def _is_released(self, version):
        ver = version.count('.') > 1 and re.sub(r'\.0$', '', version) or version
        try:
            self.fetch_page(self.url + '%s/%s.tar.gz' % (ver, ver))
            return True
        except urllib2.HTTPError, ex:
        #except Exception, ex:
            return False

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
