from general_tools import pdump,pload,list_to_extension
import price_team
import os
import math
from config import *


best_fleets={}
initialised=False

def init(update=False,refresh_data=True,base_fleet=[]):#refresh_data flag allows to redo the optimisation without re-downloading the data
    if refresh_data:
        refresh_data=update#want same behaviour as before if only pass in one argument
    global best_fleets
    best_fleets=get_best_fleets(update,refresh_data,base_fleet)

def zeros_to_empty(mylist):
    out=[]
    for item in mylist:
        if item!=0:
            out.append(item)
    return out


def increment(cap_list):
    i=0
    while True:
        cap_list[i]+=1
        if cap_list[i]>MAX_SHIP_SIZE:
            i+=1
            if i>=len(cap_list):
                return [MAX_SHIP_SIZE+1]*len(cap_list)#this will signal that we're done
        else:
            break
    for j in range(i):
        cap_list[j]=cap_list[i]
    return cap_list

def pkl_name(base_fleet):
    return FLEETS_PKL_FNAME[:-4]+list_to_extension(base_fleet)+'.pkl'


def update_best_fleets(base_fleet=[]):#bese fleet is list of ships already bought that must be included
    best_fleets={}

    capacities=[0]*(MAX_FLEET_SIZE-len(base_fleet)) #use 0 to indicate an empty slot

    base_price,base_fleet_full=price_team.cheapest_fleet(base_fleet)

    while capacities[-1]<=MAX_SHIP_SIZE:
        all_capacities=base_fleet+capacities
        total_capacity=sum(all_capacities)
        price,fleet=price_team.cheapest_fleet(zeros_to_empty(capacities))
        if total_capacity not in best_fleets.keys() or price<best_fleets[total_capacity][0]:
            best_fleets[total_capacity]=[price+base_price,base_fleet_full+fleet]  
        capacities=increment(capacities)
    pdump(best_fleets,DATA_DIR+'/'+pkl_name(base_fleet))


def get_best_fleets(update=False,refresh_data=False,base_fleet=[]):
    global initialised
    initialised=True
    if update or (pkl_name(base_fleet) not in os.listdir(DATA_DIR)):
        price_team.init(refresh_data)
        update_best_fleets(base_fleet)
    return pload(DATA_DIR+'/'+pkl_name(base_fleet))

def get_best_fleet(capacity):
    if not initialised:
        init()
    try:
        return best_fleets[capacity]
    except KeyError:
        return math.inf,[]


def save_csv(update=False):
    best_fleets=get_best_fleets(update)
    with open(CSV_DIR+'/'+FLEETS_CSV_FNAME,'w') as f:
        for i in sorted(best_fleets.keys()):
            f.write('%d, %d\n' %(i,best_fleets[i]['price']))

if __name__=='__main__':
    save_csv(True)
