## About LocLog

LocLog is a growing collection of location logging stuff for CouchDB.

It currently supports the following input sources:

* [JSON Location Tracker](http://www.precentral.net/homebrew-apps/json-location-tracker) if you set its POST field to http://host/database/_design/loclog/_update/jlt. (At one point JLT's continuous mode was not compatible, haven't tested lately.)
* GPX track segments, via Python script
* NMEA files from GPS loggers, via Python script
* fetch your [Geoloqi](https://geoloqi.com/) history via Python script

Mostly LocLog just generates CouchDB view indexes with this data. One view roughly match the structure of [HTML5 geolocation data](http://dev.w3.org/geo/api/spec-source.html#coordinates_interface) and the other is similar to [GeoJSON](http://geojson.org/geojson-spec.html) and designed for compact transfer into other apps like [ShutterStem](https://github.com/natevw/ShutterStem)'s geotagger.

There is also a sample HTML map viewer included which reads data via an interesting reduce function, providing a summary of all the breadcrumbs in the database.