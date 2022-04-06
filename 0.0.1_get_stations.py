import yaml

from functions.get_stations import get_stations


#!!!!!!!!!!!!!!!!!!!! main process !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
	cfgs = yaml.load(open('config/para_for_get_stations.yaml','r'), Loader = yaml.SafeLoader)
	
	cat = get_stations(cfgs)

	station_tuple =[]
	
	station_file = open('../log/stations_IRIS_2.txt','w')

	for network in cat:
		net = network.code
		for station in network.stations:
			stla = station.latitude
			stlo = station.longitude
			sta =station.code
			sta_name = net +'.' + sta
			print(sta_name, stla,stlo)
			station_file.write('%-8.4f %-8.4f %-14s \n'%(stla, stlo, sta_name))

	station_file.close()
