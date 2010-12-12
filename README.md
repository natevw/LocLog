## About

LocLog is the start of a collection of location logging stuff for CouchDB.

Currently, it only slurps up data from [JSON Location Tracker](http://www.precentral.net/homebrew-apps/json-location-tracker) if you set its POST field to http://host/database/_design/loclog/_update/jlt. Due to bugs in the JLT app, continuous mode will not work.

All LocLog does right now with posted data is to dump it into documents roughly matching the structure of [HTML5 geolocation data](http://dev.w3.org/geo/api/spec-source.html#coordinates_interface).