#all calculations are done in ETL
import price_conversions as pc
from config import *

FLEET_LEVEL=11

level_bonuses={}
planets=[]

def init():
    pc.get_latest_prices()
    read_level_bonus_file()
    read_planet_data_file()

def get_fuel_cost(reward):
    return reward*0.05  #fuel is 5%

def get_gas_price():
    return pc.bnb_to_etl(0.002)

def get_fleet_cost(fleet,workforce):
    fleet_fees = pc.usd_to_etl(0.5*(len(fleet)+len(workforce)))
    gas_fees = pc.bnb_to_etl(0.002) * (len(fleet)+len(workforce)) * 2
    return fleet_fees + gas_fees

def get_worker_wages(workforce):
    return pc.usd_to_etl(len(workforce))

def calc_rank(fleet):
    levels=[ship['nftData']['level'] for ship in fleet]
    rank=0
    most=0
    for i in range(1,MAX_SHIP_LEVEL+1):
        x=levels.count(i)
        if x>most:
            rank=i
            most=x
    return rank

def read_level_bonus_file():
    with open(FLEET_EXPERIENCE_FNAME,'r') as f:
        r=f.readlines()
    global level_bonuses
    for line in r:
        data=line.split(',')
        level=int(data[0])
        bonus=float(data[4])
        level_bonuses[level]=bonus

def get_level_bonus(level):
    if level_bonuses=={}:
        read_level_bonus_file()
    return level_bonuses[level]

def read_planet_data_file():
    global planets
    with open(PLANET_DATA_FNAME,'r') as f:
        r=f.readlines()
    for line in r:
        data=line.split(',')
        planet={}
        planet['level']=int(data[0])
        planet['success_prob']={i:float(data[i]) for i in range(1,MAX_SHIP_LEVEL+1)}
        planet['reward']=pc.usd_to_etl(float(data[MAX_SHIP_LEVEL+1]))
        planet['min_mp']=int(data[MAX_SHIP_LEVEL+2])
        planet['VG_cap']=float(data[MAX_SHIP_LEVEL+3])
        planets.append(planet)

def get_success_prob(planet,fleet,workforce):
    total_mp=sum([worker['nftData']['minePower'] for worker in workforce])
    if total_mp<planet['min_mp']:
        return 0
    rank=calc_rank(fleet)
    success_prob=planet['success_prob'][rank]
    if total_mp>=1500:#veterans bonus
        bonus=int((total_mp-planet['min_mp'])/100)*0.02
        success_prob=min(success_prob+bonus,planet['VG_cap'])
    return success_prob

def calc_expected_return(planet,fleet,workforce):
    reward=planet['reward']*(1+get_level_bonus(FLEET_LEVEL))
    success_prob=get_success_prob(planet,fleet,workforce)
    expected_win=reward*success_prob

    fuel_cost=get_fuel_cost(planet['reward'])
    gas_price=get_gas_price()
    worker_wages=get_worker_wages(workforce)

    return expected_win-fuel_cost-gas_price-worker_wages

def get_asset_cost(fleet,workforce):
    ships_cost=sum([ship['price'] for ship in fleet])
    workforce_cost=sum([worker['price'] for worker in workforce])
    fleet_cost=get_fleet_cost(fleet,workforce)

    return ships_cost+workforce_cost+fleet_cost

def get_roi(planet,fleet,workforce):
    assets=get_asset_cost(fleet,workforce)
    expected_return=calc_expected_return(planet,fleet,workforce)

    return expected_return/assets


def find_best_roi(fleet,workforce):
    if planets==[]:
        read_planet_data_file()
    best_roi=0
    best_planet=planets[0]#want to have something sensible as the default
    for planet in planets:
        roi=get_roi(planet,fleet,workforce)
        if roi>best_roi:
            best_roi=roi
            best_planet=planet
    return best_roi,best_planet

init()