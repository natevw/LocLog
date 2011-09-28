function (doc) {
    var exports = {};
    // !code lib/date.js
    var dt = exports;
    
    if (doc['com.stemstorage.loclog.track']) {
        doc.points.forEach(function (pt) {
            emit(dt.toUTCComponents(dt.newDate(pt.time)), {lat:pt.lat, lon:pt.lon, ele:pt.ele});
        });
    }
}