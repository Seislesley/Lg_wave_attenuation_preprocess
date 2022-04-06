#This program is used to remove the response and add station files to sac.
#2021-11-12
#For mass_download

import os, yaml
from multiprocessing import Pool

from functions.io_event_par import input_par_2
from functions.remove_response import remove_response

if __name__ == '__main__':

	print('Start remove response:')
	   
	cfgs = yaml.load(open('config/para_for_remove_resp.yaml','r'), Loader = yaml.SafeLoader)

	#import the module that will be used 
	if os.path.exists(cfgs['vel_data_dir']):
		pass
	else:
		os.mkdir(cfgs['vel_data_dir'])

	events_tuple = input_par_2(cfgs['event_input'])

	pool = Pool(processes = cfgs['Process_num'])

	#set the breakpoint for error check
	ievent = 0  #event number
	while ievent <  len(events_tuple):  # the end of the event number
		pool.apply_async(remove_response, (events_tuple[ievent],ievent, cfgs))
		ievent += 1

	pool.close()
	pool.join()

	print('Main process done:')