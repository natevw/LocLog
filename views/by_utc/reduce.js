function (keys, values) {
    var x = 0, y = 0;
    values.forEach(function (coord) {
        x += coord.lon;
        y += coord.lat;
    });
    x /= values.length;
    y /= values.length;
    
    var minIdx, minDistSqd;
    values.forEach(function (coord, idx) {
        var dX = coord.lon - x,
            dY = coord.lat - y,
            distSqd = dX*dX + dY*dY;
        if (!minIdx || distSqd < minDistSqd) {
            minIdx = idx;
            minDistSqd = distSqd;
        }
    });
    
    return values[minIdx];
}