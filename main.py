import calculate_roi
import get_optimal_teams
import sys
from config import *

def get_csv_row(name,roi,planet,fleet,workforce):
    name=TEAMS_PREFIX+'_'+str(name)+'.csv'

    fleet=sorted(fleet,key=lambda ship: ship['nftData']['workers'])
    workforce=sorted(workforce,key=lambda worker: worker['nftData']['minePower'])

    

    total_mp=sum([worker['nftData']['minePower'] for worker in workforce])
    total_capacity=sum([ship['nftData']['workers'] for ship in fleet])
    roi=roi*100

    fleet_price=sum([ship['price'] for ship in fleet])
    workforce_price=sum([worker['price'] for worker in workforce])
    total_price=fleet_price+workforce_price

    planet_level=planet['level']

    line_1=f'{name},{planet_level},{roi:.1f},,{total_capacity},{total_mp},{total_price},'

    line_2=',,,,,,,price:'
    
    for ship in fleet:
        line_1+=f',{ship["nftData"]["workers"]}'
        line_2+=f',{ship["price"]}'
    
    for i in range(MAX_FLEET_SIZE-len(fleet)):
        line_1+=','
        line_2+=','

    line_1+=','
    line_2+=','

    for worker in workforce:
        line_1+=f',{worker["nftData"]["minePower"]}'
        line_2+=f',{worker["price"]}'
    
    return line_1+'\n'+line_2+'\n'


def get_list_from_args(name,args):
    out=[]
    if name in args:
        i=args.index(name)+1
        while i<len(args) and args[i].strip().isdigit():
            out.append(int(args[i]))
            i+=1
    return out


if __name__=='__main__':
    update='update' in sys.argv
    if update:
        print('updating the data')

    base_fleet=get_list_from_args('ships',sys.argv)
    base_workforce=get_list_from_args('workers',sys.argv)

    get_optimal_teams.init(update,base_fleet,base_workforce)
    if update:
        get_optimal_teams.save_optimal_teams()
    optimal_teams=get_optimal_teams.get_optimal_teams()

    best_rois=[]
    for team in optimal_teams.keys():
        _,fleet,workforce=optimal_teams[team]
        roi,planet=calculate_roi.find_best_roi(fleet,workforce)
        best_rois.append([team,roi,planet])

    best_rois=sorted(best_rois,key=lambda x:x[1])[::-1]#sort by roi highest to lowest

    with open(CSV_DIR+'/'+ BEST_INVESTMENTS_CSV_NAME,'w') as f:
        header='team name,planet,expected roi,,total_capacity, total MP, total price, ,ship capacities'
        for i in range(MAX_FLEET_SIZE):
            header+=','
        header+=',worker MPs\n'
        f.write(header)

        for investment in best_rois:
            team,roi,planet=investment
            _,fleet,workforce=optimal_teams[team]
            f.write(get_csv_row(team,roi,planet,fleet,workforce))
            f.write('\n')
        print(f'saved best investments to {BEST_INVESTMENTS_CSV_NAME}')

