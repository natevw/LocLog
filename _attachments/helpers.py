import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


import os.path
from urllib import quote
from uuid import uuid4

SEG_TYPE = 'com.stemstorage.loclog.track'

def _genid(path, seg_number):
    id = "loc_seg-%s_%03u-%s" % (os.path.basename(path), seg_number, uuid4().hex[:7])
    return quote(id)

def _transport(method, path, data=None):
    import json
    from httplib import HTTPConnection
    logging.debug("%s to %s", method, path)
    
    conn = HTTPConnection("localhost", 5984)
    body = None
    if data is not None:
        body = json.dumps(data)
    conn.request(method, path, body)
    resp = conn.getresponse()
    return json.loads(resp.read())

def upload_points(file, seg_number, points):
    _transport('PUT', "/loctest/%s" % _genid(file, seg_number), {SEG_TYPE:True, 'points':points})
