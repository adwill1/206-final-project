
# SI 206 Final Project- Temperature Component
# Abby Williams, Lauren Fulcher, Sarah Whitman 

import json
import unittest
import os
import requests
import matplotlib

#from oikolab
#will return a list of 8 dates, one for each temperature (in increments of 10) between 10 and 90
def get_temp_dates():
    pass

#from strava
#will find 100 runs on each of the 8 dates passed in from the list (what get_temp_dates() returns), 
# and create a list of the speed/pace of the runs. will return list of 100 paces
def get_temp_speeds(temp_dates_list):
    pass

#creates a new table for the temp data. will have the 8 temps on x axis, 
# and the 100 speeds found (using get_temp_speeds) going down the columns for each temp
def create_temp_db(temp_speeds_list):
    pass

#calculates the average speed of the 100 runs and adds a row to the db 
# that says the avg speed for each temp
def calc_avg_speed_from_temps():
    pass

#generates line graph using matplotlib for temperatures
def create_temp_table():
    pass


def main():
    print("This is main")
    pass

main()

if __name__ == '__main__':
    unittest.main(verbosity=2)

