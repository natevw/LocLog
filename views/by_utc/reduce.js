function (keys, values) {
    var x = 0, y = 0, z = 0, n = 0;
    values.forEach(function (coord) {
        x += coord.lon * (coord.n || 1);
        y += coord.lat * (coord.n || 1);
        z += coord.ele * (coord.n || 1);
        n += (coord.n || 1);
    });
    x /= n;
    y /= n;
    z /= n;
    return {lat:y, lon:x, ele:z, n:n};
}