#!/usr/bin.python

import davlib

HOST = 'localhost'
PORT = 1980
BASE = 'http://%s:%s' % (HOST, PORT)

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

