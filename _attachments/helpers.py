import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

from settings import DATABASE, SEG_TYPE

import os.path
from urllib import quote
from uuid import uuid4

def _genid(path, seg_number):
    id = "loc_seg-%s_%03u-%s" % (os.path.basename(path), seg_number, uuid4().hex[:7])
    return quote(id)

def _transport(method, url, data=None):
    import json
    from urlparse import urlsplit
    from httplib import HTTPConnection
    logging.debug("%s to %s", method, url)
    
    _url = urlsplit(url)
    conn = HTTPConnection(_url.hostname, _url.port)
    body = None
    if data is not None:
        body = json.dumps(data)
    path = "%s?%s" % (_url.path, _url.query)
    if path.endswith('?'): path = path[:-1]
    conn.request(method, path, body)
    resp = conn.getresponse()
    return json.loads(resp.read())


def upload_points(file, seg_number, points):
    _transport('PUT', DATABASE + '/' + _genid(file, seg_number), {SEG_TYPE:True, 'points':points})
