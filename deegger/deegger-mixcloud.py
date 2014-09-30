#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (C) 2014 Guillaume Pellerin <yomguy@parisson.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import sys, urllib2
from pyquery import PyQuery as pq


class MixCloud(object):
    """a MixCloud HTML resource with a hack for downloading related audio file.
    Be carefull, the base_url and the hacky parsing method have been reverse engineered,
    so are not safe, not scalable, even unstable..."""

    base_url = 'https://stream21.mixcloud.com/c/m4a/64/'
    block_size = 8192

    def __init__(self, url):
        self.url = url
        self.pq = pq(url=self.url)
        shift = 0
        if self.url[-1] == '/':
            shift = 1
        self.slug = url.split('/')[-1-shift]
        self.user = url.split('/')[-2-shift]
        self.media_url = self.get_media_url()
        self.filename = self.user + '_-_' + self.slug + '.m4a'

    def get_media_url(self):
        div = self.pq('.cloudcast-waveform')
        url = div.attr('m-waveform').split('/')[2:]
        url[0] = self.base_url
        url[-1] = url[-1].replace('json', 'm4a')
        return '/'.join(url)

    def download(self):
        u = urllib2.urlopen(self.media_url)
        f = open(self.filename, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (self.filename, file_size)
        file_size_dl = 0
        while True:
            buffer = u.read(self.block_size)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        f.close()


def main():
    url = sys.argv[-1]
    mc = MixCloud(url)
    mc.download()

if __name__ == '__main__':
    main()

