from get_data import get_data
from collections import defaultdict
import math
import sys
from config import *

spaceship_dict={}
worker_dict={}

initialised=False

def init(update=False):
    global spaceship_dict,worker_dict,initialised
    spaceship_dict,worker_dict=get_data(update)
    worker_dict=clean_data_percent(worker_dict) #remove cheapest
    if update:
        save_price_csv()
    initialised=True

def save_price_csv():
    print('saving updated best prices to ' +BEST_PRICES_CSV_NAME)
    with open(CSV_DIR+'/'+ BEST_PRICES_CSV_NAME,'w') as f:
        f.write('ships\n')
        f.write('capacity,price\n')
        for cap in sorted(spaceship_dict.keys()):
            f.write('%d,%.2f\n' %(cap,spaceship_dict[cap][0]['price']))
        f.write('\nworkers\n')
        f.write('mine power,price\n')
        for mp in range(80,131):#change this if want more in the output
            if mp in worker_dict.keys():
                f.write('%d,%.2f\n' %(mp,worker_dict[mp][0]['price']))
            else:
                f.write('%d\n' %mp)
        

def clean_data_fixed(prices_dict):
    out={}
    for k in prices_dict.keys():
        if len(prices_dict[k])>DROP_NUMBER:
            out[k]=prices_dict[k][DROP_NUMBER:]
        else:
            out[k]=[prices_dict[k][-1]]
    return out

def clean_data_percent(prices_dict):
    out={}
    for k in prices_dict.keys():
        drop_number=math.ceil(len(prices_dict)*DROP_PERCENT/100)
        if len(prices_dict[k])>drop_number:
            out[k]=prices_dict[k][drop_number:]
        else:
            out[k]=[prices_dict[k][-1]]
    return out

def cheapest_fleet(capacities):
    if not initialised:
        init()
    total_cost=0
    fleet=[]
    indices=defaultdict(int)
    for c in capacities:
        ship=spaceship_dict[c][indices[c]]
        indices[c]+=1  #ensures that we only select one of each ship
        total_cost+=ship['price']
        fleet.append(ship)
    return total_cost,fleet

def cheapest_workforce(mine_powers,existing=[]):
    if not initialised:
        init()
    total_cost=0
    workforce=[]
    indices=defaultdict(int)
    for mp in existing:
        indices[mp]+=1
    for mp in mine_powers:
        try:
            worker=worker_dict[mp][indices[mp]]
        except IndexError: #there aren't enough workers for sale to satisfy the requirements, return infinity
            return math.inf,[]
        except KeyError: #there are no workers with this mine power, return infinity
            return math.inf,[]
        indices[mp]+=1  #ensures that we only select one of each ship
        total_cost+=worker['price']
        workforce.append(worker)
    return total_cost,workforce

def get_max_worker_mp():
    if not initialised:
        init()
    return max(worker_dict.keys())

if __name__ =='__main__':
    update='update' in sys.argv
    if update:
        print('updating the data')
    init(update)
    if not update:#prevents it updating the csv twice
        save_price_csv()