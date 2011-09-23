import sys
from uuid import uuid4

from helpers import _transport

files = sys.argv[1:]



class Sentence(object):
    def __init__(self, line):
        if not line[0] == '$':
            raise AssertionError("Sentence must start with $")
        line = line.strip()[1:]
        
        if line[-3] == '*':
            checksum = int(line[-2:], 16)
            line = line[:-3]
            linesum = reduce(lambda a,b: a^ord(b), line, 0)
            if linesum != checksum:
                raise AssertionError("Line checksum was not matched")
        
        fields = line.split(',')
        self.talker = fields[0][:2]
        self.type = fields[0][2:]
        self.data = self._name_fields(self.type, fields[1:])
    
    @staticmethod
    def _name_fields(type, raw_data):
        from collections import namedtuple
        HEADERS = {
            'AAM': namedtuple("ArrivalAlarm", ['entered', 'passed', 'radius', 'radius_units', 'waypoint_id']),
            'ALM': namedtuple("AlmanacData", ['messages_total', 'message_number', 'satellite_prn', 'gps_week', 'sv_health', 'eccentricity', 'reference_time', 'inclination', 'ascension_rate', 'semimajor_root', 'arg_perigree', 'lon_ascension_node', 'mean_anomaly', 'f0_clock_param', 'f1_clock_param']),
            # ...
            'RMC': namedtuple("RecommendedMinimumCoords", ['time', 'status', 'lat', 'lat_ns', 'lon', 'lon_ew', 'speed', 'track', 'date', 'magvar', 'magvar_ew', 'faa_mode']),
            'VTG': namedtuple("VelocityTrackMadeGood", ['track_true', 'is_true', 'track_magnetic', 'is_magnetic', 'speed_knots', 'is_knots', 'speed_kph', 'is_kph', 'faa_mode']),
            'GGA': namedtuple("GeoidAndAntenna", ['time', 'lat', 'lat_ns', 'lon', 'lon_ew', 'fix_quality', 'sats_in_view', 'hdop', 'geoid_alt', 'is_meters', 'geoidal_sep', 'in_meters', 'dgps_age', 'dgps_id']),
            'GSA': namedtuple("SatellitesAvailable", ['manual_auto', 'fix_mode', 'sat01', 'sat02', 'sat03', 'sat04', 'sat05', 'sat06', 'sat07', 'sat08', 'sat09', 'sat10', 'sat11', 'sat12', 'pdop', 'hdop', 'vdop']),
            'GSV': ("SatellitesInView", ['messages_total', 'message_number', 'sats_in_view', 'satNN', 'satNN_elevation', 'satNN_azimuth', 'satNN_snr'])
        }
        
        klass = HEADERS.get(type, None)
        if type == 'GSV':
            num_sats = (len(raw_data) - 3) / 4
            field_names = klass[1][:3]
            sat_template = klass[1][3:]
            for n in range(num_sats):
                field_names.extend(f.replace('NN', "%02u" % n) for f in sat_template)
            klass = namedtuple(klass[0], field_names)
        
        if klass and len(klass._fields) == len(raw_data) + 1:
            raw_data.append('')
        
        return klass(*raw_data) if klass else tuple(raw_data)


        

for file in files:
    
    line_number = 0
    for line in open(file):
        line_number += 1
        try:
            s = Sentence(line)
        except AssertionError as e:
            if line.strip():
                print "Skipping line %u. (%s)" % (line_number, e)
            continue
        
        if s.talker != 'GP':
            continue
        
        
        print s.talker, s.type, s.data
        