import numpy
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

#-------------------------------------------------------------------------------------
def events_sparse(events, min_intra_dis):
    
    new_events = []
    
    signal = numpy.zeros((len(events)), dtype = numpy.int )
    ke = 0

    while ke < len(events):
        if ke == 0:
            event = events[ke] 

            evla0 = event.lat
            evlo0 = event.lon
            mag0 = event.mag
            sta_num0 = event.station_num
            
            signal[ke] = 1
            ke += 1
        
        else:
            signal[ke] = 1           
            ie = 0 
            while ie <= ke:
                if signal[ie] == 1:
                    event_2 = events[ie]

                    evla1 = event_2.lat
                    evlo1 = event_2.lon
                    mag1 = event_2.mag
                    sta_num1 = event_2.station_num

                    distance = get_Distance(evla0, evlo0, evla1, evlo1)
                    if distance < min_intra_dis and sta_num0 > sta_num1:
                        signal[ie] = 0
                ie += 1
            
            if signal[ke] > 0 : 
                event = events[ke] 

                evla0 = event.lat
                evlo0 = event.lon
                mag0 = event.mag
                sta_num0 = event.station_num

                ke += 1
            else:
                ke += 1
        
    ke = 0
    while  ke < len(events):
        if signal[ke] == 1:
            new_events.append(events[ke])
        ke += 1

    return new_events