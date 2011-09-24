import sys
from uuid import uuid4
from xml.etree import ElementTree as ET
import logging

from helpers import _transport

files = sys.argv[1:]

for file in files:
    logging.info("Reading %s", file)
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
        _transport('PUT', "/loctest/loc_seg-%s" % uuid4().hex, seg_doc)
