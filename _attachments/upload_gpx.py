import sys
from xml.etree import ElementTree as ET
import logging

from helpers import upload_points

files = sys.argv[1:]

for file in files:
    logging.info("Reading %s", file)
    tree = ET.parse(file)
    seg_number = 0
    for seg in tree.findall(".//{http://www.topografix.com/GPX/1/1}trkseg"):
        points = []
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
            points.append(point)
        upload_points(file, seg_number, points)
        seg_number += 1
