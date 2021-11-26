import best_workforce_simple as best_workforces
import best_fleets
import price_team
import math
from general_tools import pload,pdump,list_to_extension
import os
import sys
from config import *
import time

optimal_team_prices={}
optimal_fleets={}
optimal_workforces={}
optimal_teams={}
initialised=False

def get_extension(base_fleet,base_workforce):
    out=''
    if base_fleet!=[]:
        out+='_ships'
        out+=list_to_extension(base_fleet)
    if base_workforce!=[]:
        out+='_workers'
        out+=list_to_extension(base_workforce)
    return out

def prices_fname(base_fleet,base_workforce):
    return PRICES_FNAME[:-4]+get_extension(base_fleet,base_workforce)+'.pkl'

def fleets_fname(base_fleet,base_workforce):
    return FLEETS_FNAME[:-4]+get_extension(base_fleet,base_workforce)+'.pkl'

def workforce_fname(base_fleet,base_workforce):
    return WORKFORCES_FNAME[:-4]+get_extension(base_fleet,base_workforce)+'.pkl'

def teams_fname(base_fleet,base_workforce):
    return OPTIMAL_TEAMS_FNAME[:-4]+get_extension(base_fleet,base_workforce)+'.pkl'

def init(update=False,base_fleet=[],base_workforce=[]):
    global initialised,optimal_team_prices,optimal_fleets,optimal_workforces,optimal_teams
    initialised=True
    best_workforces.init(update)
    best_fleets.init(update,False,base_fleet)#don't want to download the data twice
    price_team.init()#no need to send through update, since the data will have already been refreshed if needed
    if update or (prices_fname(base_fleet,base_workforce) not in os.listdir(DATA_DIR)):
        print('updating optimal teams')
        update_optimal_teams_specific(base_fleet,base_workforce)
    optimal_team_prices=pload(DATA_DIR+'/'+prices_fname(base_fleet,base_workforce))
    optimal_fleets=pload(DATA_DIR+'/'+fleets_fname(base_fleet,base_workforce))
    optimal_workforces=pload(DATA_DIR+'/'+workforce_fname(base_fleet,base_workforce))
    if update or (teams_fname(base_fleet,base_workforce) not in os.listdir(DATA_DIR)):
        update_optimal_teams(base_fleet,base_workforce)
    optimal_teams=pload(DATA_DIR+'/'+teams_fname(base_fleet,base_workforce))

def float_to_string(x):
    if x==math.inf:
        return 'inf'
    else:
        return '%.03f' %x

def calc_optimal_team(mine_power,base_workforce=[]):
    base_mp=sum(base_workforce)
    base_capacity=len(base_workforce)
    base_price,base_workforce_full=price_team.cheapest_workforce(base_workforce)
    best_price=math.inf
    best_fleet=[]
    best_workforce=[]
    for capacity in range(base_capacity,MAX_CAPACITY+1):
        fleet_price,fleet=best_fleets.get_best_fleet(capacity)
        workforce_price,workforce=best_workforces.get_optimum_workforce(capacity-base_capacity,mine_power-base_mp)
        total_price=fleet_price+workforce_price
        if total_price<best_price:
            best_price=total_price
            best_fleet=fleet
            best_workforce=workforce
    return best_price+base_price,best_fleet,best_workforce+base_workforce_full

def update_optimal_teams_specific(base_fleet=[],base_workforce=[]):
    prices={}
    fleets={}
    workforces={}
    for mp in range(1, MAX_MP+1):
        price,fleet,workforce=calc_optimal_team(mp,base_workforce)
        prices[mp]=price
        fleets[mp]=fleet
        workforces[mp]=workforce
    pdump(prices,DATA_DIR+'/'+prices_fname(base_fleet,base_workforce))
    pdump(fleets,DATA_DIR+'/'+fleets_fname(base_fleet,base_workforce))
    pdump(workforces,DATA_DIR+'/'+workforce_fname(base_fleet,base_workforce))

def update_optimal_teams(base_fleet=[],base_workforce=[]):
    global optimal_teams
    optimal_teams={}
    for mp in range(100,MAX_MP+1,100):
        print('Finding cheapest team with mine power >= %d' %mp)
        price,fleet,workforce=get_optimal_team(mp)
        optimal_teams[mp]=[price,fleet,workforce]
    pdump(optimal_teams,DATA_DIR+'/'+teams_fname(base_fleet,base_workforce))

def get_optimal_team(min_mp):#treats the argument as a minimum
    if not initialised:
        init()
    try:
        return optimal_teams[min_mp]
    except KeyError:
        pass
    best_price=optimal_team_prices[min_mp]
    best_mp=min_mp#this will be best in almost all circumstances I would guess
    for mp in range(min_mp+1,MAX_MP+1):
        price=optimal_team_prices[mp]
        if price<best_price:
            best_price=price
            best_mp=mp
    return best_price,optimal_fleets[best_mp],optimal_workforces[best_mp]

def save_specific_csv():
    if not initialised:
        init()
    with open(CSV_DIR+'/'+SPECIFIC_PRICES_CSV_NAME,'w') as f:
        for mp in range(1,MAX_MP+1):
            f.write('%d,%s\n' %(mp,float_to_string(optimal_team_prices[mp])))

def save_optimal_csv():
    with open(CSV_DIR+'/'+OPTIMAL_PRICES_CSV_NAME,'w') as f:
        for mp in range(100,MAX_MP+1,100):
            f.write('%d,%s\n' %(mp,float_to_string(get_optimal_team(mp)[0])))


def save_team(fleet,workforce,fname):
    total_price=0
    total_mp=0
    for ship in fleet:
        total_price+=ship['price']
    for worker in workforce:
        total_price+=worker['price']
        total_mp+=worker['nftData']['minePower']
    with open(fname,'w') as f:
        f.write('Total Mine Power, %d\n' %total_mp)
        f.write('Total Price, %.03f\n' %total_price )
        f.write('\n\n')
        
        f.write('Spaceships\n')
        f.write('Capacity,Price,Market ID,Token ID\n')
        for ship in fleet:
            f.write('%d,%.03f,%s,%s\n' %(ship['nftData']['workers'],ship['price'],ship['marketId'],ship['tokenId']))
        f.write('\n\n')

        f.write('Workers')
        f.write('Mine Power,Price,Market ID,Token ID\n')
        for worker in workforce:
            f.write('%d,%.03f,%s,%s\n' %(worker['nftData']['minePower'],worker['price'],worker['marketId'],worker['tokenId']))


def save_optimal_teams():
    if not initialised:
        init()
    save_specific_csv()
    save_optimal_csv()
    for mp in range(100,MAX_MP+1,100):
        price,fleet,workforce=get_optimal_team(mp)
        fname='%s/%s_%d.csv' %(TEAMS_DIRNAME, TEAMS_PREFIX,mp)
        save_team(fleet,workforce,fname)

def get_optimal_teams(base_fleet=[],base_workforce=[]):
    global optimal_teams
    if not initialised:
        init(base_fleet=base_fleet,base_workforce=base_workforce)
    return optimal_teams


if __name__=='__main__':
    start=time.time()
    update=("update" in sys.argv)
    if update:
        print("updating all data")
    init(update)
    save_optimal_teams()
    if update:
        total_time=time.time()-start
        minutes=int(total_time/60)
        seconds=int(total_time%60)
        print(f'Calculated optimal teams in {minutes} minutes and {seconds} seconds.')
