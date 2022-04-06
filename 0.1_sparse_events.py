import yaml

from functions.io_event_par import input_par
from functions.io_event_par import output_par_2
from functions.events_sparse import events_sparse


################# read in the event parameters from  events.par (ZLF) #############
if __name__ == '__main__':
    cfgs = yaml.load(open('config/para_for_get_events.yaml','r'), Loader = yaml.SafeLoader)
    
    events_tuple = input_par(cfgs['event_output']['origin'])
    
    print("1:: The event num is %4d "%(len(events_tuple)))

    new_events_tuple = events_sparse(events_tuple, 50.0)

    print("2:: The event num is %4d after sparse"%(len(new_events_tuple)))
    output_par_2(new_events_tuple, cfgs['event_output']['sparse'])