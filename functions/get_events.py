from obspy.clients.fdsn import Client

#---------------------------------------------------------
def get_events(cfgs):

	print("Start search the events")
	client = Client(cfgs['client']['event'])
	### search for stations  and  count the number of stations  #############################
	cat = client.get_events(starttime = cfgs['origin_time']['begin'], endtime = cfgs['origin_time']['end'],
							minlatitude = cfgs['latitude']['min'], maxlatitude = cfgs['latitude']['max'],
							minlongitude = cfgs['longitude']['min'], maxlongitude = cfgs['longitude']['max'],
							minmagnitude = cfgs['magnitude']['min'], maxmagnitude = cfgs['magnitude']['max'])

	print("Client %-6s find %d events"%(cfgs['client']['event'], len(cat)))
	return cat