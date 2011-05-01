from __future__ import with_statement

import sys, os, re
from glob import glob
import time


release = prop('release', '0.0.0')


@recipe
def task_update(c):
    """update 'website/static' according current branch name"""
    if current_branch_name() == 'release':
        task_update_sh(c)
    else:
        task_update_files(c)


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
