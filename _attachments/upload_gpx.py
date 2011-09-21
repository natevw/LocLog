import sys
import json
from uuid import uuid4
from xml.etree import ElementTree as ET


def _transport(method, path, data=None):
    import json
    from httplib import HTTPConnection
    
    conn = HTTPConnection("localhost", 5984)
    
    body = None
    if data is not None:
        body = json.dumps(data)
    conn.request(method, path, body)
    
    resp = conn.getresponse()
    return json.loads(resp.read())


file = sys.argv[1]

tree = ET.parse(file)
for seg in tree.findall(".//{http://www.topografix.com/GPX/1/1}trkseg"):
    seg_doc = {
        'com.stemstorage.loclog.track': True,
        'points': []
    }
    for pt in seg.findall("{http://www.topografix.com/GPX/1/1}trkpt"):
        point = {
             'lat': float(pt.attrib['lat']),
             'lon': float(pt.attrib['lon'])
        }
        ele = pt.find('{http://www.topografix.com/GPX/1/1}ele')
        if ele is not None:
            point['ele'] = float(ele.text)
        time = pt.find('{http://www.topografix.com/GPX/1/1}time')
        if time is not None:
            point['time'] = time.text
        seg_doc['points'].append(point)
    _transport('PUT', "/loctest/trk-%s" % uuid4().hex, seg_doc)
