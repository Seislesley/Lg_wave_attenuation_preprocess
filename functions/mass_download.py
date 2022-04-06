import os, time
from obspy.clients.fdsn.mass_downloader import RectangularDomain, Restrictions, MassDownloader

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


def mass_download_rect(event, i, cfgs):
    
    event_dir = event.name

    sleep_time = abs(os.getppid() + 10 - os.getpid()) * cfgs['sleep_gap']
    time.sleep(sleep_time)

    print("\033[1;30;47m Process ID:%s-%s; Downloading data for event %s; number %4d; \033[0m"%(os.getppid(), os.getpid(), event_dir, i))
    
    origin_time = event.time
    
    # Circular domain around the epicenter. This will download all data between
    # 70 and 90 degrees distance from the epicenter. This module also offers
    # rectangular and global domains. More complex domains can be defined by
    # inheriting from the Domain class.
    # domain = CircularDomain(latitude=37.52, longitude=143.04,
    #                         minradius=70.0, maxradius=90.0)

    #Rectangular domain 
    domain = RectangularDomain(minlatitude=cfgs['latitude']['min'], maxlatitude=cfgs['latitude']['max'],
                               minlongitude=cfgs['longitude']['min'], maxlongitude=cfgs['longitude']['max'])

    restrictions = Restrictions(
        # Get data from 5 minutes before the event to one hour after the
        # event. This defines the temporal bounds of the waveform data.
        starttime = origin_time - cfgs['waveform_time']['pre_event'] * 60,
        endtime = origin_time + cfgs['waveform_time']['after_event'] * 60,
        # You might not want to deal with gaps in the data. If this setting is
        # True, any trace with a gap/overlap will be discarded.
        reject_channels_with_gaps = cfgs['mass_download_paramters']['reject_channels_with_gaps'],
        # And you might only want waveforms that have data for at least 95 % of
        # the requested time span. Any trace that is shorter than 95 % of the
        # desired total duration will be discarded.
        minimum_length = cfgs['mass_download_paramters']['minimum_length'],
        # No two stations should be closer than 10 km to each other. This is
        # useful to for example filter out stations that are part of different
        # networks but at the same physical station. Settings this option to
        # zero or None will disable that filtering.
        minimum_interstation_distance_in_m = cfgs['mass_download_paramters']['minimum_interstation_distance_in_m'],
        # Only HH or BH channels. If a station has HH channels, those will be
        # downloaded, otherwise the BH. Nothing will be downloaded if it has
        # neither. You can add more/less patterns if you like.
        channel_priorities = cfgs['mass_download_paramters']['channel_priorities'],
        # Location codes are arbitrary and there is no rule as to which
        # location is best. Same logic as for the previous setting.
        location_priorities = cfgs['mass_download_paramters']['location_priorities'])

    # No specified providers will result in all known ones being queried.
    if cfgs['mass_download_paramters']['providers'] == 'all':
        mdl = MassDownloader()
    else:
        mdl = MassDownloader(providers = cfgs['mass_download_paramters']['providers'])

    # The data will be downloaded to the ``./waveforms/`` and ``./stations/``
    # folders with automatically chosen file names.
    mdl.download(domain, restrictions, mseed_storage=cfgs['data_dir'] + event_dir, stationxml_storage=cfgs['resp_dir'] + event_dir)

    print("\033[1;30;47m Process ID:%s-%s is done! \033[0m"%(os.getppid(), os.getpid()))
