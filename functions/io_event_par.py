from obspy.clients.fdsn import Client
from obspy import UTCDateTime

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


#--------------------------------------------------------------------------------------
#output par include station_num 
#e.g.
#20130325.20.02 20130325 20 2  44.41  56.0553  -155.6047 24.10 8.4 25.6 4.7 mb   151
def output_par(events,output_file):

	print("Write the events parameters in %-30s" % (output_file))
	event_file = open(output_file,'w')
	
	for event in events:
		origin_time = event.time
		year = origin_time.year
		month = origin_time.month
		day = origin_time.day
		hour = origin_time.hour
		mini = origin_time.minute
		
		sec = str(origin_time.second) + '.' + str(int(origin_time.microsecond/10000)).zfill(2)
		event_name = str(year) + str(month).zfill(2) + str(day).zfill(2) + '.' + str(hour).zfill(2) + '.' + str(mini).zfill(2)
		ymd = str(year) + str(month).zfill(2) + str(day).zfill(2)

		evla = event.lat
		evlo = event.lon
		evdp = event.depth

		mag = event.mag
		mag_type = event.mag_type

		station_num = event.station_num

		event_file.write('%-14s %-8s %-2d %-2d %-6s %-8.4f %-8.4f %-4.2f 8.4 25.6 %2.1f %-3s %4d\n'%(event_name,ymd,hour,mini,sec, evla, evlo, evdp, mag, mag_type, station_num))

	event_file.close()

#------------------------------------------------------------------------------------------
def output_par_2(events,output_file):
#output par exclude station_num
#e.g.
#20130325.20.02 20130325 20 2  44.41  56.0553  -155.6047 24.10 8.4 25.6 4.7 mb 
    print("Write the events parameters in %-30s" % (output_file))

    event_file = open(output_file,'w')
    
    for event in events:
        origin_time = event.time
        year = origin_time.year
        month = origin_time.month
        day = origin_time.day
        hour = origin_time.hour
        mini = origin_time.minute
        
        sec = str(origin_time.second) + '.' + str(int(origin_time.microsecond/10000)).zfill(2)
        event_name = str(year) + str(month).zfill(2) + str(day).zfill(2) + '.' + str(hour).zfill(2) + '.' + str(mini).zfill(2)
        ymd = str(year) + str(month).zfill(2) + str(day).zfill(2)

        evla = event.lat
        evlo = event.lon
        evdp = event.depth

        mag = event.mag
        mag_type = event.mag_type

        event_file.write('%-14s %-8s %-2d %-2d %-6s %-8.4f %-8.4f %-4.2f 8.4 25.6 %2.1f %-3s\n'%(event_name,ymd,hour,mini,sec, evla, evlo, evdp, mag, mag_type))

    event_file.close()

#------------------------------------------------------------------------------------------
def output_par_3(events,output_file):
#output par in 
#

    print("Write the events parameters in %-30s" % (output_file))

    event_file = open(output_file,'w')
    
    for event in events:
        origin_time = event.time
        year = origin_time.year
        month = origin_time.month
        day = origin_time.day
        hour = origin_time.hour
        mini = origin_time.minute
        
        sec = str(origin_time.second) + '.' + str(int(origin_time.microsecond/10000)).zfill(2)
        event_name = str(year) + str(month).zfill(2) + str(day).zfill(2) + '.' + str(hour).zfill(2) + '.' + str(mini).zfill(2)
        ymd = str(year) + str(month).zfill(2) + str(day).zfill(2)

        evla = event.lat
        evlo = event.lon
        evdp = event.depth

        mag = event.mag
        mag_type = event.mag_type

        event_file.write("%-8s %-4d %-3d %-2d %-2d %-6s %-8.4f %-8.4f %-4.2f 8.4 25.6 %-2.1f %3s\n"%(ymd,year,origin_time.julday,hour,mini,sec,evla,evlo,evdp,mag, mag_type))

    event_file.close()


#------------------------------------------------------------------------------------------
def output_par_CENC(events,output_file):
#output par in 
    print("Write the events parameters for CENC in %-30s" % (output_file))

    event_file = open(output_file,'w')
    
    for event in events:
        origin_time = event.time
        year = origin_time.year
        month = origin_time.month
        day = origin_time.day
        hour = origin_time.hour
        mini = origin_time.minute
        
        time = str(hour).zfill(2) + ':' + str(mini).zfill(2) + ":" + str(origin_time.second).zfill(2) + '.' + str(int(origin_time.microsecond/10000)).zfill(2)
        event_name = str(year) + str(month).zfill(2) + str(day).zfill(2) + '.' + str(hour).zfill(2) + '.' + str(mini).zfill(2)
        ymd = str(year) +'/' + str(month).zfill(2) + "/" + str(day).zfill(2)

        evla = event.lat
        evlo = event.lon
        evdp = event.depth

        mag = event.mag
        mag_type = event.mag_type

        event_file.write("%10s %11s %8.4f %8.4f %4.2f %2.1f %3s\n"%(ymd,time,evla,evlo,evdp,mag, mag_type))

    event_file.close()


################## read in the event parameters from  events.par (ZLF) #############
##input par with station_num 
#e.g.
#20130325.20.02 20130325 20 2  44.41  56.0553  -155.6047 24.10 8.4 25.6 4.7 mb   151
def input_par(input_file):

    print("Write the events parameters in %-30s" % (input_file))

    elf=open(input_file,'r')
    el=elf.read().splitlines()
    elf.close()

    events_tuple = []
    i = 0
    while i < len(el):
        event=el[i].split()

        event_dir = event[0]
        ymd = event[1]
        hour = event[2]
        mini = event[3]
        msec = event[4]

        origin_time = UTCDateTime(ymd + ' ' + hour + ':' + mini + ':' + msec)

        lat = float(event[5])
        lon = float(event[6])
        depth = float(event[7])

        mag = float(event[10])
        mag_type = event[11]

        station_num = int(event[12])
        events_tuple.append(event_tuple(origin_time,lat,lon,depth, mag, mag_type, station_num))
        
        i = i + 1
    return events_tuple

################## read in the event parameters from  events.par (ZLF) #############
###input par without station_num 
#e.g.
#20130325.20.02 20130325 20 2  44.41  56.0553  -155.6047 24.10 8.4 25.6 4.7 mb 

def input_par_2(input_file):
    
    print("Write the events parameters in %-30s" % (input_file))

    elf=open(input_file,'r')
    el=elf.read().splitlines()
    elf.close()

    events_tuple = []
    i = 0
    while i < len(el):
        event=el[i].split()
        print(event)
        event_dir = event[0]
        ymd = event[1]
        hour = event[2]
        mini = event[3]
        msec = event[4]

        origin_time = UTCDateTime(ymd + ' ' + hour + ':' + mini + ':' + msec)

        lat = float(event[5])
        lon = float(event[6])
        depth = float(event[7])

        mag = float(event[10])
        
        try:
            mag_type = event[11]
        except:
            mag_type = 'nan'

        events_tuple.append(event_tuple_2(event_dir,origin_time,lat,lon,depth, mag, mag_type))
        
        i = i + 1
    return events_tuple

