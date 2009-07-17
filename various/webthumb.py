"""Python interface to Webthumb API (see http://bluga.net/webthumb/)

By Ross Poulton - www.rossp.org

License: Use this how you like, just don't claim it as your own because
         that isn't cool. I'm not responsible for what this script does.

Usage: Define WEBTHUMB_APIKEY with your API key, as per the above URL.

Then, just call get_thumbnail(url, output_path). It will return true on
success, false on anything else.

An optional third parameter can be passed for the image size.
"""

import time
import os
import httplib

import xml.dom.minidom
from xml.dom.minidom import Node

WEBTHUMB_APIKEY='e1716f8b48a6b9f4b27fa9d06fbc8579'

WEBTHUMB_HOST='webthumb.bluga.net'
WEBTHUMB_URI='/api.php'

VALID_SIZES = (
    'small',
    'medium',
    'medium2',
    'large',
)

def get_thumbnail(url, output_path, size='medium2'):
    if size not in VALID_SIZES:
        return False

    request = """
<webthumb>
    <apikey>%s</apikey>
    <request>
        <url>%s</url>
        <output_type>png</output_type>
    </request>
</webthumb>
    """ % (WEBTHUMB_APIKEY, url)

    h = httplib.HTTPConnection(WEBTHUMB_HOST)
    h.request("GET", WEBTHUMB_URI, request)
    response = h.getresponse()

    type = response.getheader('Content-Type', 'text/plain')
    body = response.read()
    h.close()
    if type == 'text/xml':
        # This is defined as 'success' by the API. text/plain is failure.
        doc = xml.dom.minidom.parseString(body)
	wait = 1
        for node in doc.getElementsByTagName("job"):
            wait = node.getAttribute('estimate')
            key = ""
            for node2 in node.childNodes:
                if node2.nodeType == Node.TEXT_NODE:
                    key = node2.data

        # We're given an approx time by the webthumb server,
        # we shouldn't request the thumbnail again within this
        # time.
        time.sleep(int(wait))

        request = """
    <webthumb>
        <apikey>%s</apikey>
        <fetch>
            <job>%s</job>
            <size>%s</size>
        </fetch>
    </webthumb>
        """ % (WEBTHUMB_APIKEY, key, size)

        h = httplib.HTTPConnection(WEBTHUMB_HOST)
        h.request("GET", WEBTHUMB_URI, request)
        response = h.getresponse()
        try:
            os.unlink(output_path)
        except:
            pass
        img = file(output_path, "wb")
        img.write(response.read())
        img.close()
        h.close()
        return True
    else:
        return False
