function (doc) {
    var exports = {};
    // !code lib/date.js
    var dt = exports;
    
    if (doc['com.stemstorage.loclog.track']) {
        doc.points.forEach(function (pt) {
            emit(dt.toUTCComponents(dt.newDate(pt.time)), [pt.lon, pt.lat, pt.ele]);
        });
    }
}