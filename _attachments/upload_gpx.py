import sys
from xml.etree import ElementTree as ET


file = sys.argv[1]

tree = ET.parse(file)
for seg in tree.findall(".//{http://www.topografix.com/GPX/1/1}trkseg"):
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
        print point
