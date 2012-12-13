/* CouchDB (and friends) plugin for Fermata, with preliminary support for change events and default base URL.

Example use:
    <script src="fermata.js"></script>
    <script src="plugins/couchdb.js"></script>
    <script>
        var db = fermata.couchdb()('dev');      // db() === "http://localhost:5984/dev"
        fermata.plugins.couchdb.watchChanges(db, 50000, function (r) {
            console.log("Got change results:", r);
        });
    </script>
*/

var fermata;
(function () {
    var plugin = function (transport, url) {
        // TODO: better URL guessing (especially if window.location is available)
        this.base = url || "http://localhost:5984";
        return transport.using('statusCheck').using('autoConvert', "application/json");
    };
    
    plugin.watchChanges = function (db, lastSeq, callback) {
        // TODO: provide a way to "unwatch" (use built-in event models?), provide more info/options to callback, etc.
        var currentSeq = lastSeq,
            DEFAULT_DELAY = 100,
            backoff = DEFAULT_DELAY;
        function poll() {
            /* Deal with effects of IE caching — will poll rapidly once IE decides to screw up
               as described in e.g. http://www.dashbay.com/2011/05/internet-explorer-caches-ajax/ */
            // NOTE: see also https://issues.apache.org/jira/browse/COUCHDB-257 (shouldn't have been closed?!)
            db = db({nocache:Math.random()});
            db('_changes', {since:currentSeq, feed:'longpoll'}).get(function (e,d) {
                if (e) {
                    if (console && console.warn) console.warn("Error from CouchDB _changes feed, trying again in ", backoff, " milliseconds.", e, d);
                    setTimeout(poll, backoff);
                    backoff *= 2;
                } else {
                    backoff = DEFAULT_DELAY;
                    if (d.results.length) {
                        callback(d.results);
                    }
                    currentSeq = d.last_seq;
                    poll();
                }
            });
        }
        setTimeout(poll, 0);        // starting this after script completes helps avoid "progress" indicators
    };
    
    
    function onChange(seq, f) {
                    }

    // some boilerplate to deal with browser vs. CommonJS
    if (fermata) {
        fermata.registerPlugin("couchdb", plugin);
    } else {
        module.exports = plugin;
    }
})();