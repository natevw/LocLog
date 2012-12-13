/* Logs live flight status data from Gogo Inflight Internet */

var f = require('./fermata');

var INTERVAL = 5,
    DOC_PREFIX = 'fly_loc-';

var crumb = f.json("http://mq.southwestwifi.com/currentInfo"),
    db = f.json("http://localhost:5984/flights");
function fetchBreadcrumb() {
    // via http://airborne.gogoinflight.com/gbp/flightTracker.do
    // see also: https://github.com/aaronpk/GoGo-WiFi-to-Geoloqi
    crumb.get(function (e,d) {
        if (e) return console.error("Couldn't fetch crumb", e);
        d.fetched = new Date().toISOString();
        db(DOC_PREFIX + Date.now()).put(d, function (e) {
            if (e) return console.error("Couldn't store document", e);
            console.log(d.fetched, d.latitude, d.longitude, d.altitude);
        });
    });
}

fetchBreadcrumb();
setInterval(fetchBreadcrumb, INTERVAL * 1000);