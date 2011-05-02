from __future__ import with_statement

import sys, os, re
import urllib

__all__ = ('VersionWatcher', )


class Release(object):

    def __init__(self, version, filename):
        self.version  = version
        self.filename = filename


class VersionWatcher(object):

    #version_file_url  = "http://versionswitcher.appspot.com/versions/node.txt"
    version_file_path = os.path.dirname(os.path.dirname(__file__)) + "/static/versions/node.txt"
    download_page_url = "http://nodejs.org/dist/"

    def __init__(self, version_file_path=None):
        if version_file_path is not None:
            self.version_file_path = version_file_path

    def _get_registered_versions(self):
        with open(self.version_file_path) as f: data = f.read()
        return [ x for x in re.split(r'\s+', data) if x ]

    def _fetch(self, url):
        f = urllib.urlopen(url)
        data = f.read()
        f.close()
        return data

    def _parse_download_page(self, html):
        pattern = r'href="(node-v?([.\d]+)\.tar\.\w*)"'
        for m in re.finditer(pattern, html):
            filename, version = m.groups()
            yield version, filename

    def _normalize(self, version):
        return str.join(".", [ "%03d" % int(x) for x in version.split('.') ])

    def run(self):
        registered_versions = self._get_registered_versions()
        latest_version = registered_versions[0]
        threshold = self._normalize(latest_version)
        #
        html = self._fetch(self.download_page_url)
        newers = {}
        for version, filename in self._parse_download_page(html):
            key = self._normalize(version)
            if key > threshold:
                newers[key] = Release(version, filename)
        #
        if newers:
            keys = sorted(newers.keys(), reverse=True)
            newer_versions = [ newers[key].version for key in keys ]
            #versions = (newer_versions + registered_versions)[0:10]
            #self._replace_with(versions)
            return newer_versions
        else:
            return []

    def _replace_with(self, versions):
        content = "\n".join(versions) + "\n"
        with open(self.version_file_path, 'wb') as f:
            f.write(content)
