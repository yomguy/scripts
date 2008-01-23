#
# DAV testing hack
#

import sys
import davlib
import string
import gdbm
import StringIO
import base64
from xml.utils import qp_xml

HOST = 'localhost'
PORT = '1980'
BASE = 'http://%s:%s' % (HOST, PORT)
USERNAME = 'zope'
PASSWORD = 'washncellarz'
encodedUSERPASS = base64.encodestring(USERNAME+":"+PASSWORD)


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
      print string.strip(hdr)
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

def gen_test_data():
  # some property values
  pv1 = '<pv1>pv1</pv1>'
  pv2 = '<pv2/>'
  pv3 = '<foo:pv3 xmlns:foo="namespace">pv3</foo:pv3>'
  pv4 = '<foo:pv4 xmlns:foo="namespace"/>'
  pv5 = '<bar:pv5 xmlns:bar="namespace">pv5</bar:pv5>'
  pv6 = '<bar:pv6 xmlns:bar="namespace"/>'
  pv7 = '<pv7 xmlns="namespace">pv7</pv7>'
  pv8 = '<pv8 xmlns="namespace"/>'
  pv9 = '<foo:pv9 xmlns:foo="other">pv9</foo:pv9>'
  pv10 = '<foo:pv10 xmlns:foo="other"/>'
  pv11 = '<bar:pv11 xmlns:bar="other">pv11</bar:pv11>'
  pv12 = '<bar:pv12 xmlns:bar="other"/>'
  pv13 = '<pv13 xmlns="other">pv13</pv13>'
  pv14 = '<pv14 xmlns="other"/>'

  # prep the file structure
  _dav().mkcol('/dav/testdata')
  _dav().put('/dav/testdata/file1', 'file1 contents\n')
  _dav().put('/dav/testdata/file2', 'file2 contents\n')
  _dav().put('/dav/testdata/file3', 'file3 contents\n')
  _dav().mkcol('/dav/testdata/sub')
  _dav().put('/dav/testdata/sub/file1', 'sub/file1 contents\n')
  _dav().put('/dav/testdata/sub/file2', 'sub/file1 contents\n')
  _dav().put('/dav/testdata/sub/file3', 'sub/file1 contents\n')

  # attach a bunch of properties
  _dav().setprops('/dav/testdata',
                  pv1, pv2,
                  pv3, pv4, pv5, pv6, pv7, pv8,
                  pv9, pv10, pv11, pv12, pv13, pv14)
  _dav().setprops('/dav/testdata/file1',
                  pv1, pv2,
                  pv3, pv4, pv5, pv6, pv7, pv8,
                  pv9, pv10, pv11, pv12, pv13, pv14)
  _dav().setprops('/dav/testdata/file2',
                  pv9, pv10, pv11, pv12, pv13, pv14)
  _dav().setprops('/dav/testdata/file3',
                  pv1, pv2,
                  pv3, pv4, pv5, pv6, pv7, pv8)
  _dav().setprops('/dav/testdata/sub',
                  pv1, pv2)
  _dav().setprops('/dav/testdata/sub/file1',
                  pv1, pv2,
                  pv9, pv10, pv11, pv12, pv13, pv14)
  _dav().setprops('/dav/testdata/sub/file2',
                  pv3, pv4, pv5, pv6, pv7, pv8,
                  pv9, pv10, pv11, pv12, pv13, pv14)
  _dav().setprops('/dav/testdata/sub/file3',
                  pv1, pv2,
                  pv3, pv4, pv5, pv6, pv7, pv8)

  # do some moves and copies
  _dav().move('/dav/testdata/file1', BASE + '/dav/testdata/newfile1')
  _dav().move('/dav/testdata/sub', BASE + '/dav/testdata/newsub')
  _dav().move('/dav/testdata/newsub/file2', BASE + '/dav/testdata/newsubfile2')
  _dav().copy('/dav/testdata/newsub/file3', BASE + '/dav/testdata/newsub/file3copy')
  _dav().copy('/dav/testdata/newsub/file1', BASE + '/dav/testdata/subfile1copy')
  _dav().copy('/dav/testdata/newsub', BASE + '/dav/testdata/subcopy')

  # dump all the data
  _dav().allprops('/dav/testdata')


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

def test():
  f = open('hello.txt','r')
  text = '<br>'.join(f.readlines())
  print text
  
  _dav().setauth(USERNAME,PASSWORD)
  auth_dict = {"Authorization":"Basic %s" % encodedUSERPASS}
  auth = auth_dict['Authorization']
  print auth
  _dav().mkcol(BASE+'/test/',auth)
  _dav().put(BASE+'/test/foo.html',text,None,None,auth_dict)
  _dav().get(BASE+'/test/foo.html',auth_dict)
  _dav().getprops(BASE+'/test/foo.html', 'author', 'foober', 'title')
  #_dav().mkcol(BASE+'/dav/',{"Authorization":"Basic %s" % encodedUSERPASS})
  #_dav().put(BASE+'/foo.html','\n OKKKKKKKKKKK \n',{"Authorization":"Basic %s" % encodedUSERPASS})
  #_dav().options('/dav/foo.html')
  #_dav().delete('/dav/foo.html')
  #_dav().delete('/dav/newdir')
  #_dav().mkcol('/dav/newdir')
  #_dav().mkcol('/dav/newdir/another')
  #_dav().allprops('/dav', 1)
  #_dav().propnames('/dav', 1)
  #_dav().getprops('/dav', 'author', 'foober', 'title')
  #_dav().propfind('/dav',
                  #'<?xml version="1.0"?><propfind xmlns="DAV:"><prop>'
                  #'<author/><foobar/><title/>'
                  #'</prop></propfind>',
                  #'infinity')
  #_dav().delprops('/dav', 'author')
  #_dav().setprops('/dav', '''<author>
        #<complex oops="hi" two="three" > stuff goes in here
        #</complex>
          #<more foo="bar"/>
          #stuff
      #</author>''')
  #_dav().put('/dav/blah.cgi', 'body of blah.cgi\n')
  #_dav().put('/dav/file1', 'body of file1\n')
  #_dav().move('/dav/blah.cgi', BASE + '/dav/foo.cgi')
  #_dav().copy('/dav/subdir', BASE + '/dav/subdir3')
  #_dav().setprops('/dav/file1','<woo>bar</woo>')

  #_dav().propfind('/dav/foo.cgi', '''<?xml version="1.0"?>
  #<propfind xmlns="DAV:"><propname/>
  #<foo:bar xmlns:foo="xyz" xmlns:bar="abc">
  #<foo:bar bar:xxx="hello"/>
  #<bar:ddd what:aaa="hi" xmlns:what="ha"/>
  #<geez xmlns="empty"/>
  #<davtag/>
  #<rep:davtag2 xmlns:rep="DAV:"/>
  #</foo:bar>
  #</propfind>
  #''')

  #del_test_data()
  #gen_test_data()


if __name__ == '__main__':
  if HOST == 'FILL THIS IN':
    import sys
    sys.stdout = sys.stderr
    print 'ERROR: you must edit davtest.py to set the HOST/PORT values'
    print '       at the top of the script.'
    sys.exit(1)

  test()
