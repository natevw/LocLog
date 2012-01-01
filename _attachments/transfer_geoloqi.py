from settings import DATABASE, GEOLOQI_ACCESS_TOKEN as ACCESS_TOKEN, GEOLOQI_TYPE as LOQITYPE

from helpers import logging
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
    if str(resp.status)[0] != '2':
        logging.error("%s to %s returned %s", method, url, resp.status)
        raise AssertionError("Bad server response status")
    return json.loads(resp.read())


initial = _transport('GET', DATABASE + "/_design/loclog/_view/last_geoloqi?descending=true&limit=1&include_docs=true")
if initial['rows']:
    start_doc = initial['rows'][0]['doc']
    start_date = start_doc['data'][-1]['date']
else:
    start_doc = None
    start_date = '2010-04-01T00:00:00Z'

points = []
while 1:
    url = "https://api.geoloqi.com/1/location/history?after=%s&sort=asc&ignore_gaps=1&count=1000&oauth_token=%s" % (start_date.replace("+", "%2B"), ACCESS_TOKEN)
    data = _transport('GET', url)
    if not data['points']:
        logging.info("No more points available.")
        break
    points.extend(data['points'])
    start_date = data['points'][-1]['date']
    logging.info("Loaded points up to %s.", start_date)

from itertools import groupby
points.sort(key=lambda p: p['date'])
for k, g in groupby(points, lambda p: p['date'].split('T')[0]):
    if start_doc and start_date.split('T')[0] == k:
        start_doc['data'].extend(g)
        id, doc = start_doc['_id'], start_doc
        logging.info("Updating %s document.", k)
    else:
        id, doc = "geoloqi-%s" %k.replace('-',''), {LOQITYPE:True, 'data':list(g)}
        logging.info("Storing %s document.", k)
    _transport('PUT', DATABASE + "/%s" % id, doc)
    start_doc = None

logging.info("Stored %s new point(s) from Geoloqi.", len(points))
