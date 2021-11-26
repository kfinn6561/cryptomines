import price_team
from general_tools import pload,pdump
import os
import math
from config import *

cache={}
max_worker_mp=255#this should be updated by init

initialised=False

def init(update=False):
    price_team.init(update)
    global max_worker_mp,initialised
    max_worker_mp=price_team.get_max_worker_mp()
    if update or (CACHE_FNAME not in os.listdir(DATA_DIR)):
        populate_cache()
    load_cache()
    initialised=True    

def load_cache():
    global cache
    cache=pload(DATA_DIR+'/'+CACHE_FNAME)

def save_cache():
    pdump(cache,DATA_DIR+'/'+CACHE_FNAME)

def calc_optimal_workforce(capacity,mine_power,existing=[]):
    if mine_power>capacity*max_worker_mp:#impossible to achieve, no point wasting time by doing any calculation
        return math.inf,[]

    global cache
    try:
        return cache[(capacity,mine_power)]#could change this to a lookup, but might make things slower
    except KeyError:
        pass

    if capacity==1: 
        price,squad= price_team.cheapest_workforce([mine_power],existing)
        MPs=[worker['nftData']['minePower'] for worker in squad]
        return price, MPs#do not add singles to cache. Want to get them new each time to account for existing
        
    else:
        best_price=math.inf
        best_MPs=[]
        for split in range(1,min([mine_power,max_worker_mp])+1):
            group_price,group_MPs=calc_optimal_workforce(capacity-1,mine_power-split,existing)
            single_price,single_MPs=calc_optimal_workforce(1,split,existing+group_MPs)#makes sure the single doesn't take anything already in the group
            total_price=group_price+single_price
            total_MPs=group_MPs+single_MPs
            if total_price<best_price:
                best_price=total_price
                best_MPs=total_MPs
        
        price=best_price
        MPs=best_MPs

    cache[(capacity,mine_power)]=[price,MPs]

    return price,MPs
    
def populate_cache():
    print('populating the cache of optimum workforces')
    for capacity in range(1,MAX_CAPACITY+1):
        for MP in range(1,MAX_MP+1):
            if MP%1000==0:
                print(f'finding optimal team for capacity {capacity} and mine power {MP}')
            calc_optimal_workforce(capacity,MP)
    save_cache()
    
def get_optimum_workforce(capacity,mine_power):
    price,workforce=calc_optimal_workforce(capacity,mine_power)
    if price==math.inf:#an inf should always return inf
        return price,[]
    else:
        return price_team.cheapest_workforce(workforce)

if __name__ =='__main__':
    init(True)