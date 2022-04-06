import os, yaml
from multiprocessing import Pool
from functions.io_event_par import input_par_2
from functions.mass_download import mass_download_rect

if __name__ == '__main__':
    
    print('Start main process')

    cfgs = yaml.load(open('config/para_for_mass_down.yaml','r'), Loader = yaml.SafeLoader)

    if os.path.exists(cfgs['data_dir']):
        pass
    else:
        os.mkdir(cfgs['data_dir'])

    if os.path.exists(cfgs['resp_dir']):
        pass
    else:
        os.mkdir(cfgs['resp_dir'])

    events_tuple = input_par_2(cfgs['event_input'])

    pool = Pool(processes = cfgs['Process_num'])
    
    i = 0
    while i < len(events_tuple):
        pool.apply_async(mass_download_rect, (events_tuple[i], i, cfgs))
        i = i + 1

    pool.close()
    pool.join()

    print("Main process done")

