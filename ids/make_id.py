#!/usr/bin/python

import sys
import hashlib, time, base64

def makeSessionId(st):
    m = hashlib.md5()
    m.update('this is a test of the emergency broadcasting system')
    m.update(str(time.time()))
    m.update(str(st))
    return base64.encodestring(m.digest())[:-3].replace('/', 'a').replace('+','b')

print makeSessionId(sys.argv[-1])

