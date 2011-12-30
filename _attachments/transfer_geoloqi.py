ACCESS_TOKEN = ""       # get from https://developers.geoloqi.com/getting-started when logged in
FILE = "/Users/natevw/Desktop/geoloqi_dump.json"

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

import json

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



try:
    fp = open(FILE, 'rb')
    points = json.load(fp)
    start_date = points[-1]['date']
except IOError:
    points = []
    start_date = "2010-01-01T00:00:00Z"

while 1:
    url = "https://api.geoloqi.com/1/location/history?after=%s&sort=asc&ignore_gaps=1&count=1000&oauth_token=%s" % (start_date.replace("+", "%2B"), ACCESS_TOKEN)
    data = _transport('GET', url)
    if not data['points']:
        break
    points.extend(data['points'])
    start_date = data['points'][-1]['date']
    logging.info("Loaded points up to %s", start_date)

fp = open(FILE, 'wb')
json.dump(points, fp, indent=4)
fp.close()
