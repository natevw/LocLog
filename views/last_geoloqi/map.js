function (doc) {
    if (!doc['com.stemstorage.loclog.geoloqi']) return;
    
    var pts = doc.data, pt = pts[pts.length - 1];
    if (pt) emit(pt.date);
}