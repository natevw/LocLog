function (head, req) {
    provides("json", function () {
        var row, point, buff = [];
        send("[");
        while (row = getRow()) {
            point = row.value;
            point[3] = row.key;
            buff.push(point);
            if (buff.length > 1000) {
                send(buff.map(JSON.stringify).join(','));
                buff.length = 0;
                buff.push(void 0)
            }
        }
        send(buff.map(JSON.stringify).join(','));
        send("]");
    });
}
