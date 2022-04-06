import re,glob,os,obspy, yaml
from obspy import read

from functions.io_event_par import input_par_2,output_par_2,output_par_3

class station:
	def __init__(self,name,lat,lon,dep):
		self.name = name
		self.lat = lat
		self.lon = lon
		self.dep = dep
		#self.dist = dist
	def __repr__(self):
		return repr((self.name,self.lat,self.lon,self.dep))

#------------------------- define class of event
class event_tuple_2:
    def __init__(self, name, time, lat, lon, depth, mag, mag_type):
        self.name = name
        self.time = time
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.mag = mag
        self.mag_type = mag_type
    def __repr__(self):
        return repr((self.name, self.time, self.lat, self.lon, self.depth, self.mag, self.mag_type))

################# read in the event parameters from  events.par (ZLF) #############
if __name__ == '__main__':
	cfgs = yaml.load(open('config/para_for_delete.yaml','r'), Loader = yaml.SafeLoader)

	events_tuple = input_par_2(cfgs['event_input'])

	i = 0
	m = 0 #record the event number for the sac less than 3 
	all_sac = 0
	left_event = 0

	station_name = []
	station_tuples = []

	if os.path.exists(cfgs['station_output']):
		print('\033[1;31m The Program will:\n a. delete the event_dir for sac less than 3;\n b. renew the events.par \033[0m')
		station_flag = 0
	else:
		print('\033[1;31m The Program will:\n a. delete the event_dir for sac less than 3;\n b. renew the events.par;\n c. extract station info \033[0m')
		station_flag = 1

	new_events_tuple = []
	while i < len(events_tuple):
		
		event = events_tuple[i]

		event_dir = event.name

		origin_time = event.time
		year = origin_time.year
		month = origin_time.month
		day = origin_time.day
		hour = origin_time.hour
		mini = origin_time.minute
		ymd = str(year) + str(month).zfill(2) + str(day).zfill(2)

		evlo = event.lon
		evla = event.lat
		evdp = event.depth

		try:
			now_dir = os.getcwd()
			os.chdir(cfgs['vel_data_dir'] + event_dir + '/')
		except:
			print("The records of %d-%s have been deleted, skippiing"%(i,event_dir))
			i += 1
			m += 1
			continue
		else:	
			if len(glob.glob('*.SAC')) < 3:
				print("The records of %d-%s is less then 3, delete"%(i,event_dir))
				os.chdir('../')
				os.system('rm -r ' + event_dir )
				os.chdir(now_dir)
				m += 1
			else:
				new_events_tuple.append(events_tuple[i])

				n_sac = len(glob.glob('*.SAC'))

				if station_flag == 0:
					pass
				else:
					#extract station info from the sac files
					print("Extract the station info for event %d-%s:"%(i, event_dir))
					for fname in glob.glob('*.SAC'):
						a = read(fname)
						head = a[0]

						#read station info
						net = head.stats.network
						sta = head.stats.station
						sname = net + '.' + sta
						if sname not in station_name:
							station_name.append(sname)
							#other informations
							try:
								slat = head.stats.sac.stla
								slon = head.stats.sac.stlo
								sdep = head.stats.sac.stdp
								station_tuples.append(station(sname,slat,slon,sdep))
							except:
								print('[ERROR3] Head info wrong: %s'%(fname))

				#make sacfiles:
				if os.path.exists('sacfiles.txt'):
					#print("3: The sacfiles exist, skipping")
					os.chdir(now_dir)
				else:
					print("Make sacfiles.txt for %d-%s"%(i,event_dir))
					os.system('ls *.?HZ.?.SAC > sacfiles.txt') 
					os.chdir(now_dir)

				#record the all sac and event number 
				all_sac = all_sac + n_sac
				left_event += 1
			i += 1

	print("Delete " + str(m) + ' event for sac less than 3')
	print("Total event number: " + str(left_event) + "; sac numbers: " + str(all_sac))

	output_par_2(new_events_tuple, cfgs['event_output'][1])
	output_par_3(new_events_tuple, cfgs['event_output'][2])

	#sorted 
	sort_station_tuples = sorted(station_tuples,key=lambda station: station.name,reverse=True)
	if station_flag == 0:
		pass
	else:
		i=0
		out=open(cfgs['station_output'],'w')
		while i < len(station_tuples):
			out.write('%-10s %-8.4f %-8.4f %3.1f\n' %(sort_station_tuples[i].name,sort_station_tuples[i].lon,sort_station_tuples[i].lat,sort_station_tuples[i].dep) )
			i+=1
		out.close()







