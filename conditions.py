
# SI 206 Final Project- Weather Condition Component
# Name: 

import json
import unittest
import os
import requests
import matplotlib

#from Weatherstack
#will return a list of 8 dates, one for each weather condition 
def get_cond_dates():
    pass

#from strava
#will find 100 runs on each of the 8 dates passed in from the list (what get_cond_dates() returns), 
# and create a list of the speed/pace of the runs. will return list of 100 paces
def get_cond_speeds(cond_dates_list):
    pass

#creates a new table for the cond data. will have the 8 conditions on x axis, 
# and the 100 speeds found (using get_cond_speeds) going down the columns for each condiditon
def create_cond_db(cond_speeds_list):
    pass

#calculates the average speed of the 100 runs and adds a row to the db 
# that says the avg speed for each condition
def calc_avg_speed_from_conds():
    pass

#generates line graph using matplotlib for conditions
def create_cond_table():
    pass



def main():
    print("This is main")
    pass

main()

if __name__ == '__main__':
    unittest.main(verbosity=2)

