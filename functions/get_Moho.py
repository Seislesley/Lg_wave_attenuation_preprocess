#-----------------------------------------------------------------------
def get_Moho(lat1, lon1, moho_file):
	Moho_file = open(moho_file,'r')
	points = Moho_file.read().splitlines()
	Moho_file.close()

	for point in points:
		lon = float(point.split()[0])
		lat = float(point.split()[1])
		depth = 0.0 - float(point.split()[2])
		#print(lon, lat, lon1, lat1)
		if abs(lon - lon1) < 0.5  and abs(lat - lat1) < 0.5:
			return depth