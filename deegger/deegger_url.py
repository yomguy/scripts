#!/usr/bin/python

import sys
from deegger import *

format = sys.argv[1]
text = sys.argv[2]
url = sys.argv[3]
m3u_dir = sys.argv[4]
m3u = M3UPlaylist(m3u_dir + os.sep + 'deegger_' + url[7:].replace('/', '_') + '.m3u')

u = UrlMediaParser(format, text, {'unescapedUrl': url}, m3u)
u.start()
    