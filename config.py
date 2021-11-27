import os

DATA_DIR='data'
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

CSV_DIR='output'
if not os.path.isdir(CSV_DIR):
    os.mkdir(CSV_DIR)

TEAMS_DIRNAME='optimal_teams'
if not os.path.isdir(TEAMS_DIRNAME):
    os.mkdir(TEAMS_DIRNAME)

MAX_FLEET_SIZE=10
MAX_SHIP_SIZE=5
MAX_SHIP_LEVEL=5
MAX_MP=5000 #the maximum MP we're interested in
MAX_CAPACITY=50#the maximum fleet capacity we care about

FLEETS_CSV_FNAME='best_fleets.csv'
FLEETS_PKL_FNAME='best_fleets.pkl'

CACHE_FNAME='workforce_cache.pkl'

PRICES_FNAME='optimal_team_prices.pkl'
FLEETS_FNAME='optimal_team_fleets.pkl'
WORKFORCES_FNAME='optimal_team_workforces.pkl'

SPECIFIC_PRICES_CSV_NAME='optimal_team_prices_specific.csv'
OPTIMAL_PRICES_CSV_NAME='optimal_team_prices_allow_greater.csv'
BEST_INVESTMENTS_CSV_NAME='best_investment_options.csv'


OPTIMAL_TEAMS_FNAME='optimal_teams.pkl'

TEAMS_PREFIX='optimal_team'

SPACESHIPS_URL = 'https://api.cryptomines.app/api/spaceships'
WORKERS_URL = 'https://api.cryptomines.app/api/workers'

SPACESHIPS_FNAME='spaceships.pkl'
WORKERS_FNAME='workers.pkl'

FLEET_EXPERIENCE_FNAME='fleet_experience_data.csv'
PLANET_DATA_FNAME='planet_data.csv'

DROP_NUMBER=5 #will ignore the cheapest DROP_NUMBER workers in each mine power
DROP_PERCENT=3

DATA_WAIT_TIME=20 #time (in seconds) to wait for fluctuations in the marketplace to die down

BEST_PRICES_CSV_NAME='best_prices.csv'

MAX_PAGE=8