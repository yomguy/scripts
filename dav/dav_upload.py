#
# DAV testing hack
#

import os
import sys
import davlib
import string
import gdbm
import StringIO
import base64
from xml.utils import qp_xml

#HOST = 'parisson.com'
HOST = 'localhost'
PORT = '1983'
BASE = 'http://%s:%s' % (HOST, PORT)
USERNAME = 'admin'
DESTDIR = 'CRFPA/formations/formations-en-ligne/cours-audio/droit_penal_cours/'
#DESTDIR =  'parisson.com_2/Members/yomguy/dav'
#DESTDIR = 'dav'
SOURCEDIR = '/home/momo/music/mp3' 
FILE = 'lll-0001.mp3'
#FILE = '04_Idjut_Boys_-_Rebirth_Evil_Vibrations.mp3'
PASSWORD = sys.argv[1]



def getprop(dirname, fname, ns, propname):
  g = gdbm.open(dirname + '/.DAV/' + fname, 'r')
  return g[str(ns) + ':' + propname + '\0']

def setprop(dirname, fname, ns, propname, value):
  g = gdbm.open(dirname + '/.DAV/' + fname, 'c')
  g[str(ns) + ':' + propname + '\0'] = value + '\0'

def dump(dirname, fname):
  g = gdbm.open(dirname + '/.DAV/' + fname, 'r')
  for key in g.keys():
    print `key`, '=', `g[key]`

class mydav(davlib.DAV):
  def _request(self, method, url, *rest, **kw):
    print 'REQUEST:', method, url
    response = apply(davlib.DAV._request, (self, method, url) + rest, kw)
    print "STATUS:", response.status
    print "REASON:", response.reason
    for hdr in response.msg.headers:
      print string.strip    (hdr)
    print '-'*70
    if response.status == 207:
      #print response.doc.dump()
      #print response.doc.toxml()
      response.parse_multistatus()
      davlib.qp_xml.dump(sys.stdout, response.root)
    elif method == 'LOCK' and response.status == 200:
      response.parse_lock_response()
      davlib.qp_xml.dump(sys.stdout, response.root)
    else:
      print response.read()
    print '-'*70
    return response
  def get_lock(self, url, owner='', timeout=None, depth=None):
    return self.lock(url, owner, timeout, depth).locktoken


def _dav():
  return mydav(HOST, PORT)

def getvalue(url, ns, prop):
  response = _dav().getprops(url, prop, ns=ns)
  resp = response.msr.responses[0]
  if resp.status and resp.status[0] != 200:
    raise 'error retrieving property', response.status
  propstat = resp.propstat[0]
  if propstat.status and propstat.status[0] != 200:
    raise 'error retrieving property', propstat.status
  return propstat.prop[(ns, prop)]

  #s = StringIO.StringIO()
  #davlib.qp_xml.dump(s, propstat.prop[(ns, prop)])
  #return s.getvalue()


def del_test_data():
  _dav().delete('/dav/testdata')

def gettest():
  _dav()._request('GET', '/dav/test.html')

def if_test():
  _dav().put('/dav/foo.html', 'foo.html contents\n')
  etag = qp_xml.textof(getvalue('/dav/foo.html', 'DAV:', 'getetag'))
  print 'ETAG:', etag
  _dav()._request('DELETE', '/dav/foo.html', extra_hdrs={
    'If' : '(["abc"])',
    })
  _dav()._request('DELETE', '/dav/foo.html', extra_hdrs={
    'If' : '([' + etag + '])',
    })

def lock_test():
  _dav().delete('/dav/locktest')
  _dav().mkcol('/dav/locktest')
  _dav().mkcol('/dav/locktest/sub')

  # test a locknull resource
  r = _dav().lock('/dav/locktest/locknull')

def upload(base, dest_dir, source_dir, file, username, password, encodeduserpass):
  _dav().setauth(username, password)
  auth_dict = {"Authorization":"Basic %s" % encodeduserpass}
  auth = auth_dict['Authorization']
  print auth

  f = open(source_dir + os.sep + file,'r')
  #_dav().mkcol(BASE+'/'+DESTDIR,auth)
  _dav().put(base+'/'+dest_dir+'/'+file,f.read(),None,None,auth_dict)



if __name__ == '__main__':
  if HOST == 'FILL THIS IN':
    import sys
    sys.stdout = sys.stderr
    print 'ERROR: you must edit davtest.py to set the HOST/PORT values'
    print '       at the top of the script.'
    sys.exit(1)

  encodedUSERPASS = base64.encodestring(USERNAME+":"+PASSWORD)
  upload(BASE, DESTDIR, SOURCEDIR, FILE, USERNAME, PASSWORD, encodedUSERPASS)
