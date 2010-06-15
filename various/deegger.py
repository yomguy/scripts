#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Guillaume Pellerin, 2009

# <yomguy@parisson.com>

# This software is a computer program whose purpose is to find cool music
# samples over internet with the help of google search ajax api.

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

import os
import re
import sys
import urllib
import simplejson
from threading import Thread

version = '0.1'

def prog_info():
    return """ deegger.py v%s : easy media crawler through google search

 Depends on:
    python, python-simplejson

 Usage :
    $ ./deegger.py FORMAT TEXT M3U_DIR

 Where:
    FORMAT is the media type you are looking for
    TEXT is your google text query
    M3U_DIR an output M3U playlist directory

 For example:
    ./deegger.py wav "sample" /var/www/m3u

 Author:
    Guillaume Pellerin <yomguy@parisson.com>

 License:
    CeCILL v2
 """ % version


class DeeGGer(Thread):

    def __init__(self, format, text, m3u_dir):
        Thread.__init__(self)
        self.format = format
        self.text = text
        self.m3u_dir = m3u_dir
        if not os.path.exists(self.m3u_dir):
            os.makedirs(self.m3u_dir)
        self.m3u_file = self.m3u_dir + os.sep + 'deegger_' + self.text.replace('/', '_') + '.' + self.format + '.m3u'
        self.m3u = M3UPlaylist(self.m3u_file)

        self.n = 4
        self.media_q = 'intitle:"index.of" "parent directory" "size" "last modified" "description" [snd] (%s) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics|index|%s|%ss) -gallery -intitle:"last modified"' % (self.format, self.format, self.format)
        #self.media_q = 'intitle:"index.of" [snd] (%s) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics|index|%s|%ss) -gallery' % (self.format, self.format, self.format)
        self.q = '%s %s' % (self.text, self.media_q)
        self.results = self.google_search()

    def google_search(self):
        results = []
        for j in range(0,self.n):
            page = str(j*4)
            query = urllib.urlencode({'q' : self.q, 'start': page})
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
            json = simplejson.loads(urllib.urlopen(url).read())
            #print json
            if json['responseData']:
                for r in json['responseData']['results']:
                    results.append(r)
            #except:
                #pass
                ##print "ERROR"
        return results

    def run(self):
        print self.results
        print len(self.results)
        i = 0
        parsers = []
        media_list = []
        for result in self.results:
            if result:
                parsers.append(UrlMediaParser(self.format, self.text, result))
                try:
                    list = parsers[i].start()
                    if list:
                        i += 1
                    self.m3u.put(list)
                except:
                    continue
        self.m3u.close()


class M3UPlaylist:

    def __init__(self, m3u_file):
        self.m3u_file = m3u_file
        self.m3u = open(self.m3u_file, 'w')
        self.init_m3u()

    def init_m3u(self):
        self.m3u.write('#EXTM3U\n')
        self.m3u.flush()

    def put(self, url_list):
        #print url_list
        for url in url_list:
            info = '#EXTINF:'',%s' % (url +'\n')
            self.m3u.write(info)
            self.m3u.write(url + '\n')
            self.m3u.flush

    def close(self):
        self.m3u.close()

class UrlMediaParser(Thread):

    def __init__(self, format, text, results):
        Thread.__init__(self)
        self.format = format
        self.text = text
        self.results = results
        self.url = self.results['unescapedUrl']

    def is_in_multiple_case(self, _string, text):
        return _string in text \
                or _string.upper() in text \
                or _string.lower() in text \
                or _string.capitalize() in text

    def get_multiple_case_string(self, _string):
        return _string.upper(), _string.lower() , _string.capitalize()


    def run(self):
        media_list = []
        if self.url:
            try:
                data = urllib.urlopen(self.url).read()
                for line in data.split("\012"):
                    for format in self.get_multiple_case_string(self.format):
                        s = re.compile('href=".*\.'+ format + '">').search(line,1)
                        if s:
                            file_name = line[s.start():s.end()].split('"')[1]
                            print file_name
                            if self.is_in_multiple_case(self.text, file_name) or \
                               self.is_in_multiple_case(self.text, self.url):
                                media_list.append(self.url + file_name)
            except:
                pass

            if media_list:
                return media_list

def main():
    if len(sys.argv) == 4:
        d = DeeGGer(sys.argv[1], sys.argv[2], sys.argv[3])
        d.start()
    else:
        text = prog_info()
        sys.exit(text)

if __name__ == '__main__':
    main()
