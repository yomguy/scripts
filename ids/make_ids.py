#!/usr/bin/python

import hashlib, time, base64

def get_an_id(st):
    m = hashlib.md5()
    m.update('this is a test of the emergency broadcasting system')
    m.update(str(time.time()))
    m.update(str(st))
    return base64.encodestring(m.digest())[:-3].replace('/', 'a').replace('+','b')

N= 1000
ids = []
for i in range(0, N):
    ids.append(get_an_id(str(i)))
    
print ids

