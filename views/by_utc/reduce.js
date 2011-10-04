function (keys, values, rereduce) {
    if (rereduce) {
        values = [].concat.apply([], values);
    }
    var maxAllowed = ~~Math.log(values.length) + 1,
        select = [], avg = {lat:0, lon:0, n:0};
    
    if (values.length < maxAllowed) {
        return values;
    } else while (avg.n < maxAllowed) {
        var target = (avg.n) ? {lat:avg.lat/avg.n, lon:avg.lon/avg.n} : avg,
            maxDistSqd = -1, maxIdx;
        values.forEach(function (coord, idx) {
            if (select[idx]) return;
            var dx = coord.lon - target.lon,
                dy = coord.lat - target.lat,
                distSqd = dx*dx + dy*dy;
            if (distSqd > maxDistSqd) {
                maxDistSqd = distSqd;
                maxIdx = idx;
            }
        });
        select[maxIdx] = true;
        avg.lat += values[maxIdx].lat;
        avg.lon += values[maxIdx].lon;
        avg.n += 1;
    }
    return values.filter(function (d, idx) { return select[idx]; });
}