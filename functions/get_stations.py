from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from functions.get_Distance import get_Distance
#------------------------- define class of event
class event_tuple:
	def __init__(self,time,lat,lon,depth,mag,mag_type,station_num):
		self.time = time
		self.lat = lat
		self.lon = lon
		self.depth = depth
		self.mag = mag
		self.mag_type = mag_type
		self.station_num = station_num
	def __repr__(self):
		return repr((self.time, self.lat, self.lon, self.depth, self.mag, self.mag_type, self.station_num))

#---------------------------------------------------------
def get_stations(cfgs):
	begin_time = cfgs['origin_time']['begin']
	end_time = cfgs['origin_time']['end']

	client = Client(cfgs['client']['station'])
	### search for stations  and  count the number of stations  #############################
	stations = client.get_stations(starttime = begin_time, endtime = end_time, network = '*',
									minlatitude = cfgs['latitude']['min'], maxlatitude = cfgs['latitude']['max'],
									minlongitude = cfgs['longitude']['min'], maxlongitude = cfgs['longitude']['max'],
									channel = 'HHZ',  includerestricted = True)
	stations_2 = client.get_stations(starttime = begin_time, endtime = end_time, network = '*',
									minlatitude = cfgs['latitude']['min'], maxlatitude = cfgs['latitude']['max'],
									minlongitude = cfgs['longitude']['min'], maxlongitude = cfgs['longitude']['max'],
									channel = 'BHZ',  includerestricted = True)
	stations.extend(stations_2)

	return stations