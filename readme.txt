Steps to run the code:

1. Copy the source files to your local computer
2. Open terminal
3. cd into the directory with the code
4. Run the command: python3 main.py

#########################################################

Options:

update
    downloads the latest price data and re-runs the optimisation (takes about 5 minutes)

ships
    used to input ships already existing in the fleet. after the keyword "ships" enter the capacities of all existing ships e.g. ships 3 3

workers
    used to input workers already existing in the fleet. after the keyword "workers" enter the mine power of all existing workers e.g. workers 110 108

#########################################################

Example:

python3 main.py update ships 3 3 workers 110 86 98 103

#########################################################

Output:

data folder:
    machine readable data used by the code. no need to look in here

output folder:
    summary of the best options.contains the following
    
    best_investments.csv
        Best investment options ordered by ROI. Includes details of the required ships and workers
    optimal_teams_allow_greater.csv
        Cheapest price (col B) of a fleet with at least a given mine power (col A). Can copy into an existing spreadsheet
    optimal_team_prices_specific
        Cheapest price (col B) of a fleet with exactly a given mine power (col A). Can copy into an existing spreadsheet

optimal_teams folder:
    detailed breakdown of the best fleets with at least a given mine power. Seperate csv file for each one
