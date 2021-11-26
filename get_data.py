import requests
from general_tools import check_in_sorted, pdump,pload
import os
from json import JSONDecodeError
import time
from config import *

def update_data():

    spaceships,workers=get_raw_data(False) #change this when we figure out how to get better api data


    spaceship_dict={}
    for spaceship in spaceships:
        if spaceship['isSold']:
            continue
        key=spaceship['nftData']['workers']
        spaceship['price']=float(spaceship['price'])/1e18
        if key not in spaceship_dict.keys():
            spaceship_dict[key]=[]
        spaceship_dict[key].append(spaceship)

    for k in spaceship_dict.keys():
        spaceship_dict[k]=sorted(spaceship_dict[k],key=lambda d:d['price'])

    print('saving spaceship data to %s' %SPACESHIPS_FNAME)
    pdump(spaceship_dict,DATA_DIR+'/'+SPACESHIPS_FNAME)

    

    worker_dict={}
    for worker in workers:
        if worker['isSold']:
            continue
        key=worker['nftData']['minePower']
        worker['price']=float(worker['price'])/1e18
        if key not in worker_dict.keys():
            worker_dict[key]=[]
        worker_dict[key].append(worker)

    for k in worker_dict.keys():
        worker_dict[k]=sorted(worker_dict[k],key=lambda d:d['price'])

    print('saving worker data to %s' %WORKERS_FNAME)
    pdump(worker_dict,DATA_DIR+'/'+WORKERS_FNAME)


def get_raw_data(fix_fluctuations=False):
    print('downloading latest spaceship data from %s' %SPACESHIPS_URL)
    spaceships=get_single_data(SPACESHIPS_URL)
    

    print('downloading latest worker data from %s' %WORKERS_URL)
    workers=get_single_data(WORKERS_URL)

    return spaceships,workers

    # ship_ids=[int(ship['marketId']) for ship in spaceships]
    # worker_ids=[int(worker['marketId']) for worker in workers]

    # start=time.time()
    # print('Sleeping for %d seconds to remove fluctuations' %DATA_WAIT_TIME)

    # ship_ids=sorted(ship_ids) #sorting might take a while so do it while sleeping
    # worker_ids=sorted(worker_ids)

    # sort_time=time.time()-start
    # if sort_time<DATA_WAIT_TIME:
    #     time.sleep(DATA_WAIT_TIME-sort_time)

    # print('downloading latest spaceship data from %s' %SPACESHIPS_URL)
    # spaceships=requests.get(SPACESHIPS_URL).json()

    # print('downloading latest worker data from %s' %WORKERS_URL)
    # workers=requests.get(WORKERS_URL).json()

    # out_ships=[]
    # out_workers=[]
    # for ship in spaceships:
    #     if check_in_sorted(int(ship['marketId']),ship_ids):
    #         out_ships.append(ship)

    # for worker in workers:
    #     if check_in_sorted(int(worker['marketId']),worker_ids):
    #         out_workers.append(worker)

    # return out_ships,out_workers

def get_single_data(base_url,max_level=5):
    out=[]
    for i in range(1,max_level+1):
        level_dat=[]
        j=1
        while True:
            url=base_url+f'?level={i}&page={j}'
            print('reading data from %s' %url)
            try:
                data=requests.get(url).json()
            except JSONDecodeError:
                break
            level_dat+=data['data']
            if len(level_dat)>=data['count']:
                break
            if j>=MAX_PAGE:
                break
            j+=1
        out+=level_dat
    return out




def get_data(update=False):
    files=os.listdir(DATA_DIR)
    if update or (WORKERS_FNAME not in files) or (SPACESHIPS_FNAME not in files):
        update_data()
    spaceship_dict=pload(DATA_DIR+'/'+SPACESHIPS_FNAME)
    workers_dict=pload(DATA_DIR+'/'+WORKERS_FNAME)
    return spaceship_dict,workers_dict




if __name__=='__main__':
    update_data()