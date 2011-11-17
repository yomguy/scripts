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
import Queue
from threading import Thread
from optparse import OptionParser

version = '0.3'

def prog_info():
    return """ deegger : easy media crawler through google search api

 Version:
    %s
    
 Depends on:
    python, python-simplejson

 Usage:
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


class DeeGGer(object):

    def __init__(self, options, args):
        self.format = options.format
        self.text = options.text
        self.m3u_dir = options.output
        if not os.path.exists(self.m3u_dir):
            os.makedirs(self.m3u_dir)
        self.m3u_file = self.m3u_dir + os.sep + 'deegger_' + self.text.replace('/', '_') + '.' + self.format + '.m3u'
        self.range = 4
        self.servers = []
        
        self.media_q = 'intitle:"index.of" "parent directory" "size" "last modified" "description" [snd] (%s) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics|index|%s|%ss) -gallery -intitle:"last modified"' % (self.format, self.format, self.format)
        #self.media_q = 'intitle:"index.of" [snd] (%s) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics|index|%s|%ss) -gallery' % (self.format, self.format, self.format)
        
        self.query = '%s %s' % (self.text, self.media_q)
        self.q = Queue.Queue(1)
        self.results = Queue.Queue(1)

    def run(self):
        g = GoogleSearch(self.range, self.query)
        self.results = g.search()
#        print self.results
        for result in self.results:
            url = result['url']
            s = UrlMediaParser(self.format, self.text, url, self.q)
            s.start()
        
        self.m3u = M3UPlaylist(self.q, self.m3u_file)
        self.m3u.start()
        
        self.q.join()
        self.m3u.close()
        
class Producer(Thread):
    """a Producer master thread"""

    def __init__(self, q):
        Thread.__init__(self)
        self.q = q

    def run(self):
        i=0
        q = self.q
        while True:
            q.put(i,1)
            i+=1
            
class GoogleSearch(object):

    def __init__(self, range, query):
        self.range = range
        self.query = query
        
    def search(self):
        results = []
        for j in range(0, self.range):
            page = str(j)
            query = urllib.urlencode({'q' : self.query, 'start': page})
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
            json = simplejson.loads(urllib.urlopen(url).read())
            if json['responseData']:
                for r in json['responseData']['results']:
                    results.append(r)
        return results


class UrlMediaParser(Thread):

    def __init__(self, format, text, url, q):
        Thread.__init__(self)
        self.format = format
        self.text = text
        self.url = url
        self.q = q

    def is_in_multiple_case(self, _string, text):
        return _string in text \
                or _string.upper() in text \
                or _string.lower() in text \
                or _string.capitalize() in text

    def get_multiple_case_string(self, _string):
        return _string.upper(), _string.lower() , _string.capitalize()


    def run(self):
        q = self.q
        media_list = []
        if self.url:
            print 'deegging : ' + self.url
            try:
                data = urllib.urlopen(self.url).read()
                for line in data.split("\012"):
                    s = re.compile('href=".*\.'+ format + '"').search(line,1)
                    if s:
                        file_name = line[s.start():s.end()].split('"')[1]
                        if self.is_in_multiple_case(self.text, file_name):
                            q.put(self.url + '/' + file_name)
            
            except:
                pass


class M3UPlaylist(Thread):

    def __init__(self, q, m3u_file):
        Thread.__init__(self)
        self.q = q
        self.m3u_file = m3u_file
        self.m3u = open(self.m3u_file, 'w')
        self.m3u.write('#EXTM3U\n')
        #self.m3u.flush()

    def run(self):
        url = self.q.get()
        print 'adding : ' + url
        info = '#EXTINF:'',%s' % (url +'\n')
        self.m3u.write(info)
        self.m3u.write(url + '\n')
        #self.m3u.flush()

    def close(self):
        self.m3u.close()


class Logger:
    """A logging object"""
    
    def __init__(self, file):
        import logging
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def write(self, message):
        self.logger.info(message)


def main():
    if len(sys.argv) <= 2:
        text = prog_info()
        sys.exit(text)
    
    else:
        parser = OptionParser()
        parser.add_option("-t", "--text", dest="text", help="set the TEXT google query", metavar="TEXT")
        parser.add_option("-f", "--format", dest="format", help="set the format to search for" , metavar="FORMAT")
        parser.add_option("-o", "--output", dest="output", help="set the output directory" , metavar="OUTPUT")
        (options, args) = parser.parse_args()
        
        d = DeeGGer(options, args)
        d.run()
        
if __name__ == '__main__':
    main()
