

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