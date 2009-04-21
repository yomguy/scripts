#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Guillaume Pellerin, 2009

# <yomguy@parisson.com>

# This software is a computer program whose purpose is to stream audio
# and video data through icecast2 servers.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <yomguy@parisson.com>

import sys
import urllib
import re
import simplejson
from threading import Thread

version = '0.1'

def prog_info():
    return """ search_mp3.py v%s

 Usage :
    $ search_mp3.py TEXT

    where TEXT is your google text query""" % version

class GoogleMediaSearch:

    def __init__(self, text):
        self.format = 'mp3'
        self.text = text
        self.n = range(0,25)
        self.media_q = 'intitle:"index.of" "parent directory" "size" "last modified" "description" [snd] (mp3|ogg|flac|avi|mp4) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics|mp3s|mp3|flac|ogg|index) -gallery -intitle:"last modified" -intitle:(intitle|%s)' % self.format
        self.q = '%s %s' % (self.text, self.media_q)
        self.results = self.google_search()
        self.get_media_links()

    def google_search(self):
        results = []
        for j in self.n:
            page = str(j*4)
            query = urllib.urlencode({'q' : self.q, 'start': page})
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
            json = simplejson.loads(urllib.urlopen(url).read())
            try:
                for r in json['responseData']['results']:
                    results.append(r)
            except:
                pass
        return results

    def get_media_links(self):
        links = []
        for result in self.results:
            m = MediaParser(self.format, self.text, result)
            m.start()

class MediaParser(Thread):

    def __init__(self, format, text, result):
        Thread.__init__(self)
        self.format = format
        self.text = text
        self.result = result

    def run(self):
        media_list = []
        url = self.result['unescapedUrl']
        if url:
            try:
                u = urllib.urlopen(url)
                data = u.read()
                lines = data.split("\012")
                for line in lines:
                    s = re.compile('HREF=".*\.'+ self.format + '">').search(line.strip(),1)
                    if s:
                        file_name = line[s.start():s.end()].split('"')[1]
                        if self.text.upper() in file_name or \
                                self.text.lower() in file_name or \
                                self.text.capitalize() in file_name:
                            media_list.append(url + file_name)
                if media_list:
                    print media_list
            except:
                pass


def main():
    if len(sys.argv) == 2:
        g = GoogleMediaSearch(sys.argv[1])
    else:
        text = prog_info()
        sys.exit(text)

if __name__ == '__main__':
    main()