
from functions.io_event_par import input_par_2,output_par_CENC

#!!!!!!!!!!!!!!!!!!!! main process !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':

	events_tuple = input_par_2('../log/events_origin.par')

	output_par_CENC(events_tuple, 'events_CENC.txt')
