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
@spices("-o: override 'versions/LANG.txt' when changed", "[LANG...]")
def task_check(c, *args, **kwargs):
    """check versions of node.js, ruby, and python"""
    if not args: args = ['node', 'ruby', 'python']
    gvars = globals()
    for lang in args:
        func = gvars['task_' + lang + '_vers']
        if not func:
            raise ValueError("%s: unsupported language name." % lang)
        sys.stdout.write('- ' + lang + ': ')
        func(c, *args, **kwargs)


@recipe
@spices("-o: override 'versions/node.txt' when changed")
def task_node_vers(c, *args, **kwargs):
    #"""check node's versions"""
    filename = "versions/node.txt"
    known_versions   = _get_known_versions(filename)
    fetched_versions = _fetch_node_versions()
    _compare_versions(fetched_versions, known_versions,
                      kwargs.get('o') and _generate_node_text or None)


@recipe
@spices("-o: override 'versions/ruby.txt' when changed")
def task_ruby_vers(c, *args, **kwargs):
    #"""check ruby's versions"""
    filename = "versions/ruby.txt"
    known_versions = _get_known_versions(filename)
    fetched_versions = _fetch_ruby_versions()
    _compare_versions(fetched_versions, known_versions,
                      kwargs.get('o') and _generate_ruby_text or None)


@recipe
@spices("-o: override 'versions/python.txt' when changed")
def task_python_vers(c, *args, **kwargs):
    #"""check python's versions"""
    filename = "versions/python.txt"
    known_versions = _get_known_versions(filename)
    fetched_versions = _fetch_python_versions()
    set1, set2 = set(fetched_versions), set(known_versions)
    for ver in set1 - set2:
        if not _is_python_released(ver):
            fetched_versions.remove(ver)
    _compare_versions(fetched_versions, known_versions,
                      kwargs.get('o') and _generate_python_text or None)


def _compare_versions(fetched_versions, known_versions, text_func):
    if sorted(fetched_versions) == sorted(known_versions):
        print("not changed.")
    else:
        set1, set2 = set(fetched_versions), set(known_versions)
        print("new versions: %s" % ', '.join(set1 - set2))
        print("disappeared: %s" % ', '.join(set2 - set1))
        if text_func:
            text = text_func(versions)
            with open(filename, 'w') as f:
                f.write(text)

def _get_known_versions(filename):
    with open(filename) as f:
        content = f.read()
    return content.split()

def _fetch_node_versions():
    url  = 'http://nodejs.org/dist/'
    rexp = re.compile(r'href="node-v(\d+\.\d+(?:\.\d+)?)\.tar.(?:gz|bz2)"')
    html = _fetch_page(url)
    versions = [ m.group(1) for m in rexp.finditer(html) ]
    versions = [ ver for ver in versions if _normalize(ver) > '000.004.003' ]
    return versions

def _fetch_ruby_versions():
    url  = 'http://www.ring.gr.jp/archives/lang/ruby/'
    rexp = re.compile(r'href="ruby-(\d+\.\d+\.\d+(?:-p?\d.*?)?)\.tar.gz"')
    versions = []
    for ver in ('1.8', '1.9'):
        html = _fetch_page(url + ver + '/')
        versions.extend( m.group(1) for m in rexp.finditer(html) )
    return versions

def _fetch_python_versions():
    url  = 'http://www.python.org/ftp/python/'
    rexp = re.compile(r'href="(\d\.\d(?:\.\d)?)/?"')
    html = _fetch_page(url)
    versions = [ m.group(1) for m in rexp.finditer(html) ]
    return [ ver.count('.') == 1 and ver + '.0' or ver
               for ver in versions if _normalize(ver) >= '002.002']

def _is_python_released(version):
    ver = version.count('.') > 1 and re.sub(r'\.0$', '', version) or version
    try:
        html = _fetch_page('http://www.python.org/ftp/python/%s/%s.tar.gz' % (ver, ver))
        return True
    except urllib2.HTTPError, ex:
    #except Exception, ex:
        return False


def _fetch_page(url):
    global urllib2
    if not urllib2: import urllib2
    f = urllib2.urlopen(url)
    content = f.read()
    f.close()
    return content

def _normalize(ver):
    return ".".join("%03d" % int(d.group(0)) for d in re.finditer(r'\d+', ver))

def _generate_node_text(versions):
    vers = sorted(versions, key=_normalize, reverse=True)
    return "\n".join(vers)

def _generate_ruby_text(versions):
    vals = {}
    for ver in sorted(versions, key=_normalize, reverse=True):
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

def _generate_python_text(versions):
    vals = {}
    for ver in sorted(versions, key=_normalize, reverse=True):
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
