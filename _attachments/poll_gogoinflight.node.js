/* Logs live flight status data from Gogo Inflight Internet */

var f = require('fermata'),
    vm = require('vm');

var DATABASE = "http://localhost:5984/loctest",     // TODO: reliably pull from settings.py someway/how?
    INTERVAL = 30,              // TODO: is this is too short/long? better way?
    DOCID = 'gogo-test';        // HACK/TODO: how should we do this "for realz"?

// make sure storage doc exists
var docURL = f.json(DATABASE + '/' + DOCID),
    doc = {crumbs:[]};
docURL.put(doc, function (e,d) {
    if (e) { // assume 409
        docURL.get(function (e,d) {
            doc = d;
            setInterval(fetchBreadcrumb, INTERVAL * 1000);
        });
    } else {
        console.log("here");
        doc._rev = d.rev;
        setInterval(fetchBreadcrumb, INTERVAL * 1000);
    }
});

function fetchBreadcrumb() {
    // via http://airborne.gogoinflight.com/gbp/flightTracker.do
    // see also: https://github.com/aaronpk/GoGo-WiFi-to-Geoloqi
    f.raw({base:"http://airborne.gogoinflight.com/abp/service/statusTray.do"}).get(function (e,d) {
        var crumb = vm.runInNewContext("val = " + d.data, {});
        console.log(crumb);
        
        // store to doc
        doc.crumbs.push(crumb);
        docURL.put(doc, function (e,d) {
            if (e) {
                console.error(e);
            } else {
                console.log(d);
                doc._rev = d.rev;
            }
        });
    });
}