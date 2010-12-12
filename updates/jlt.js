/* This CouchDB document update function is designed for use with
the JSON Location Tracker webOS app: https://github.com/jettero/jlt */
function (doc, req) {
    if (doc) {
        throw "New documents only";
    }
    
    // http://wiki.apache.org/couchdb/ExternalProcesses (req, response)
    // https://github.com/jettero/jlt/blob/master/PROTOCOL (req.form)
    
    var fix = JSON.parse(req.form.fixes)[0];
    if (!fix.t) {
        throw "Bad data!";
    }
    //log(fix);
    
    if (fix.t instanceof Array) {
        fix.t = fix.t[0];
    }
    var confirmation = {
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({fix_tlist:[fix.t]})
    };
    
    var doc = {};
    // randomize ID a bit to keep JLT from clogging itself with duplicates
    doc._id = "location@" + (fix.t + Math.random()/100);
    doc.timestamp = (new Date(fix.t)).toISOString();
    
    // mimic http://dev.w3.org/geo/api/spec-source.html#coordinates_interface
    doc.latitude = fix.ll[0];
    doc.longitude = fix.ll[1];
    doc.accuracy = fix.ha;
    
    // we get zeroes instead of null even when unknown, so assume these are always valid
    doc.altitude = fix.al;
    doc.altitudeAccuracy = fix.va;
    
    doc.heading = fix.vv[1];
    doc.speed = fix.vv[0];
    
    return [doc, confirmation];
}
