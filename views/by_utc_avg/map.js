function (doc) {
    var exports = {};
    // !code lib/date.js
    var dt = exports;
    
    if (doc['com.stemstorage.loclog.track']) {
        doc.points.forEach(function (pt) {
            emit(dt.toUTCComponents(dt.newDate(pt.time)), {time:pt.time, lat:pt.lat, lon:pt.lon, ele:pt.ele});
        });
    } else if (doc['com.stemstorage.loclog.geoloqi']) {
        doc.data.forEach(function (pt) {
            var p = pt.location.position;
            emit(dt.toUTCComponents(dt.newDate(pt.date)), {time:pt.date, lat:p.latitude, lon:p.longitude, ele:p.altitude});
        });
    }
}