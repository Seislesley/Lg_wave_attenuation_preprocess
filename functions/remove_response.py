import os, subprocess,glob
from obspy import read,read_inventory

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

def remove_response(event, i, cfgs):
	
	event_dir = event.name

	evlo = event.lon
	evla = event.lat
	evdp = event.depth
        
	print("\033[1;30;47m Process ID:%s-%s; Remove respnse for event %s; number %4d; \033[0m"%(os.getppid(), os.getpid(), event_dir, i))

	origin_time = event.time
	year = origin_time.year
	month = origin_time.month
	day = origin_time.day
	hour = origin_time.hour
	mini = origin_time.minute     
	sec = str(origin_time.second) + '.' + str(int(origin_time.microsecond/10000)).zfill(2)


	if os.path.exists(cfgs['vel_data_dir'] + event_dir):
		pass
	else:
		os.mkdir(cfgs['vel_data_dir'] + event_dir)

	if os.path.exists(cfgs['data_dir'] + event_dir + '/mseedfiles.txt'):
		pass
	else:
		now_dir = os.getcwd()
		os.chdir(cfgs['data_dir'] + event_dir)
		os.system('ls *.mseed > mseedfiles.txt')
		os.chdir(now_dir)
	
	mseedlf=open(cfgs['data_dir']+event_dir+'/mseedfiles.txt','r')
	mseedl=mseedlf.read().splitlines()
	mseedlf.close()

	isac = 0
	while isac < len(mseedl):
		mseed = mseedl[isac]

		#print(mseed)
		st = read(cfgs['data_dir'] + event_dir + '/' + mseed)
		
		head = st[0]
		
		print("Event number: "+str(i) + ' ; SAC number: ' + str(isac) + ' , Total SAC number: ' + str(len(mseedl)))
		print('Event: ' + event_dir + ' ; Station: ' + head.stats.network + '.' + head.stats.station)		

		resp = cfgs['resp_dir'] + event_dir + '/' + head.stats.network + '.' + head.stats.station + '.xml'

		try:
			inv = read_inventory(resp)
		except:
			print("\033[1;31m Process ID:%s-%s [ERROR1]: Can't find the response file %s \033[0m"%(os.getppid(), os.getpid(), resp))
			isac += 1
			continue
		else:
			stla = inv.networks[0].stations[0].latitude
			stlo = inv.networks[0].stations[0].longitude
			stdp = inv.networks[0].stations[0].elevation
			
			#print('Demean')
			st.detrend(type="demean")
			#print('Linear')
			st.detrend(type="linear")
			#print('Taper')
			st.taper(max_percentage = cfgs['max_percentage'])
			#print('Remove response')
			try:
				st.remove_response(inventory=inv,output=cfgs['output'],pre_filt=cfgs['pre_filt'])
			except:
				print("\033[1;31m [ERROR2]: The wrong response file %s \033[0m"%(os.getppid(), os.getpid(), resp))
				isac += 1
				continue
			else:
				newsacname = str(year) + '.' + str(origin_time.julday).zfill(3) + '.' + str(hour).zfill(2) + '.' + str(mini).zfill(2) + '.' + sec + '00.' + head.stats.network +'.' + head.stats.station + '..' + head.stats.channel + '.D.SAC'  
				st.write(cfgs['vel_data_dir'] + event_dir + '/' + newsacname,format='SAC')
				
				#the sac is in m/s, but what we need to change it 
				s = "wild echo off \n"
				s += "r {} \n".format(cfgs['vel_data_dir'] + event_dir + '/' + newsacname)
				s += "ch evlo {} evla {} evdp {}\n".format(evlo, evla, evdp)
				s += "ch stlo {} stla {} stdp {}\n".format(stlo, stla, stdp)
				s += "ch o gmt {} {} {} {} {} {}\n".format(year, origin_time.julday, hour, mini, sec.split('.')[0],  sec.split('.')[1])
				s += "wh \n"
				s += "q\n"
				subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())		#for event
				isac += 1
			
	print('Finishing remove response')
	print("\033[1;30;47m Process ID:%s-%s [DONE] for event %s; number %4d; \033[0m"%(os.getppid(), os.getpid(), event_dir, i))
