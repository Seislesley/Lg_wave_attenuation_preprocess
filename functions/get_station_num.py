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
def get_station_num(event, cfgs):
	evla = event.origins[0].latitude
	evlo = event.origins[0].longitude
	origin_time = event.origins[0].time

	begin_time = origin_time
	end_time = origin_time + 18 * 60

	client = Client(cfgs['client']['station'])
	### search for stations  and  count the number of stations  #############################
	stations = client.get_stations(starttime = begin_time, endtime = end_time, network = '*',
									minlatitude = cfgs['latitude']['min'], maxlatitude = cfgs['latitude']['max'],
									minlongitude = cfgs['longitude']['min'], maxlongitude = cfgs['longitude']['max'],
									channel = 'HHZ', includeavailability = True, includerestricted = True)
	stations_2 = client.get_stations(starttime = begin_time, endtime = end_time, network = '*',
									minlatitude = cfgs['latitude']['min'], maxlatitude = cfgs['latitude']['max'],
									minlongitude = cfgs['longitude']['min'], maxlongitude = cfgs['longitude']['max'],
									channel = 'BHZ', includeavailability = True, includerestricted = True)
	stations.extend(stations_2)

	station_num = 0
	for network in stations.networks:
		for stations in network.stations:
			stla = stations.latitude
			stlo = stations.longitude
			epicenter = get_Distance(stla, stlo, evla, evlo)
			if epicenter > cfgs['epicenter']['min'] and epicenter < cfgs['epicenter']['max']:
				station_num += 1
	return station_num