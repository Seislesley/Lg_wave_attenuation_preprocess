import yaml

from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy import read_inventory, read_events
import math

from functions.get_Moho import get_Moho
from functions.get_Distance import get_Distance
from functions.get_station_num import get_station_num
from functions.get_events import get_events

from functions.io_event_par import output_par_2

#------------------------- define class of event
class event_tuple:
	def __init__(self,time,lat,lon,depth,mag,mag_type):
		self.time = time
		self.lat = lat
		self.lon = lon
		self.depth = depth
		self.mag = mag
		self.mag_type = mag_type
	def __repr__(self):
		return repr((self.time, self.lat, self.lon, self.depth, self.mag, self.mag_type))

#!!!!!!!!!!!!!!!!!!!! main process !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
	cfgs = yaml.load(open('config/para_for_get_events.yaml','r'), Loader = yaml.SafeLoader)
	
	cat = get_events(cfgs)

	events_tuple =[]
	
	for event in cat:
		#read in the parameters
		evla = event.origins[0].latitude
		evlo = event.origins[0].longitude
		origin_time = event.origins[0].time
		try:
			evdp = event.origins[0].depth / 1000 # in m
		except:
			evdp = 9999.99

		mag = event.magnitudes[0].mag
		mag_type = event.magnitudes[0].magnitude_type

		events_tuple.append(event_tuple(origin_time,evla,evlo,evdp, mag, mag_type))

	output_par_2(events_tuple, cfgs['event_output']['origin'])
