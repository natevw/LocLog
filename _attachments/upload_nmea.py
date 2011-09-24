import sys
from uuid import uuid4
from collections import namedtuple, OrderedDict
from datetime import datetime, timedelta
import logging

from helpers import _transport

files = sys.argv[1:]


FIELD_HEADERS = {
    'AAM': namedtuple("ArrivalAlarm", ['entered', 'passed', 'radius', 'radius_units', 'waypoint_id']),
    'ALM': namedtuple("AlmanacData", ['messages_total', 'message_number', 'satellite_prn', 'gps_week', 'sv_health', 'eccentricity', 'reference_time', 'inclination', 'ascension_rate', 'semimajor_root', 'arg_perigree', 'lon_ascension_node', 'mean_anomaly', 'f0_clock_param', 'f1_clock_param']),
    # ...
    'RMC': namedtuple("RecommendedMinimumCoords", ['time', 'status', 'lat', 'lat_ns', 'lon', 'lon_ew', 'speed', 'track', 'date', 'magvar', 'magvar_ew', 'faa_mode']),
    'VTG': namedtuple("VelocityTrackMadeGood", ['track_true', 'is_true', 'track_magnetic', 'is_magnetic', 'speed_knots', 'is_knots', 'speed_kph', 'is_kph', 'faa_mode']),
    'GGA': namedtuple("GeoidAltitude", ['time', 'lat', 'lat_ns', 'lon', 'lon_ew', 'fix_quality', 'sats_in_fix', 'hdop', 'geoid_alt', 'is_meters', 'geoidal_sep', 'in_meters', 'dgps_age', 'dgps_id']),
    'GSA': namedtuple("SatellitesAvailable", ['manual_auto', 'fix_mode', 'sat01', 'sat02', 'sat03', 'sat04', 'sat05', 'sat06', 'sat07', 'sat08', 'sat09', 'sat10', 'sat11', 'sat12', 'pdop', 'hdop', 'vdop']),
    'GSV': ("SatellitesInView", ['messages_total', 'message_number', 'sats_in_view', 'satNN', 'satNN_elevation', 'satNN_azimuth', 'satNN_snr']),
    'WPL': namedtuple("WaypointLocation", ['wp_lat', 'wp_lat_ns', 'wp_lon', 'wp_lon_ew', 'waypoint_name']),
}

class Sentence(object):
    def __init__(self, line):
        if not line[0:1] == '$':
            raise AssertionError("Sentence must start with $")
        line = line.strip()[1:]
        
        if line[-3:-2] == '*':
            checksum = int(line[-2:], 16)
            line = line[:-3]
            linesum = reduce(lambda a,b: a^ord(b), line, 0)
            if linesum != checksum:
                raise AssertionError("Line checksum was not matched")
        
        fields = line.split(',')
        self.talker = fields[0][:2]
        self.type = fields[0][2:]
        try:
            self.data = self._name_fields(self.type, fields[1:])
        except:
            raise AssertionError("Could not parse fields")
    
    @staticmethod
    def _name_fields(type, raw_data):
        if type in ('VTG', 'GSA', 'GSV'): return tuple()    # skip frequent types we don't actually use
        
        klass = FIELD_HEADERS.get(type, None)
        if type == 'GSV':
            num_sats = (len(raw_data) - 3) / 4
            field_names = klass[1][:3]
            sat_template = klass[1][3:]
            
            msg = raw_data[1]
            field_names[1] += msg
            for n in range(num_sats):
                field_names.extend(f.replace('NN', "%02um%s" % (n+1, msg)) for f in sat_template)
            klass = namedtuple("%s%u" % (klass[0], num_sats), field_names)
        
        if klass and len(klass._fields) == len(raw_data) + 1:   # fixup pre-2.3 sentences lacking faa_mode
            raw_data.append('')
        
        return klass(*raw_data) if klass else tuple(raw_data)

def augment(current, new):
    for key, val in new.items():
        if current.get(key, val) != val:
            raise AssertionError("New data for '%s' not compatible with current." % key)
    for key, val in new.items():
        current[key] = val

def extract(fix):
    loc = OrderedDict()
    if 'date' in fix and 'time' in fix:
        loc['time'] = datetime.strptime(fix['date']+fix['time'], "%d%m%y%H%M%S.%f")
    if 'lat' in fix and 'lat_ns' in fix:
        loc['lat'] = (int(fix['lat'][:2]) + float(fix['lat'][2:]) / 60) * (-1 if fix['lat_ns'] == 'S' else 1)
    if 'lon' in fix and 'lon_ew' in fix:
        loc['lon'] = (int(fix['lon'][:3]) + float(fix['lon'][3:]) / 60) * (-1 if fix['lon_ew'] == 'W' else 1)
    if 'geoid_alt' in fix:
        loc['ele'] = float(fix['geoid_alt'])
    return loc

for file in files:
    logging.info("Reading %s", file)
    fixes, line_number, state, fix = [], 0, {}, OrderedDict()
    for line in open(file):
        line_number += 1
        try:
            s = Sentence(line)
        except AssertionError as e:
            if line.strip():
                logging.warn("Skipping line %u. (%s)", line_number, e)
            continue
        if s.talker != 'GP':
            continue
        if not hasattr(s.data, '_asdict'):
            continue
        
        update = s.data._asdict()
        if 'date' in update: state['date'] = update['date']
        if 'time' in update: state['time'] = update['time']
        try:
            augment(fix, update)
        except AssertionError as e:
            if 'time' not in str(e):
                logging.warn("Unusual split at line %u. (%s)", line_number, e)
            
            if 'time' not in fix and 'time' in state:
                fix['time'] = state['time']
            if 'date' not in fix and 'date' in state:
                fix['date'] = state['date'] if fix['time'] > state['time'] else (datetime.strptime(state['date'], "%d%m%y") + timedelta(days=1)).strftime("%d%m%y")
            fixes.append(fix)
            fix = update
    if fix:
        fixes.append(fix)
    
    segment, prev_time = [], None
    for loc in (extract(fix) for fix in fixes):
        if 'time' not in loc: continue
        if prev_time and loc['time'] > prev_time + timedelta(seconds=15):
            _transport('PUT', "/loctest/loc_seg-%s" % uuid4().hex, {'com.stemstorage.loclog.track': True, 'points': segment})
            segment = []
        segment.append(loc)
        prev_time = loc['time']
        loc['time'] = loc['time'].isoformat() + 'Z'
