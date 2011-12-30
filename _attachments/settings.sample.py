'''This is the config file for the Python scripts in this folder. Chceck values and rename to `settings.py` before use.'''

DATABASE = "http://localhost:5984/loctest"

# used by upload_gpx and upload_nmea scripts
SEG_TYPE = 'com.stemstorage.loclog.track'

# used by transfer_geoloqi script
GEOLOQI_TYPE = 'com.stemstorage.loclog.geoloqi'
GEOLOQI_ACCESS_TOKEN = ""   # get from https://developers.geoloqi.com/getting-started
