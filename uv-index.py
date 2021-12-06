
# SI 206 Final Project- UV Index Component
# Name: 

import json
import unittest
import os
import requests
import matplotlib


#from weatherstack
#will return a list of 8 dates, one for each uv index 2-10
def get_uv_dates():
    r = requests.get('''http://api.weatherstack.com/current?access_key=c4e94a14f446360bc7d07ae8bb5eea49&query=Detroit''')
    r2 = requests.get('''http://api.weatherstack.com/historical?access_key=c4e94a14f446360bc7d07ae8bb5eea49&query=Detroit&historical_date=2018-10-10''')
    #r2 doesnt work because the free api doesnt give historical data
    data_text = r.text
    data = json.loads(data_text)
    return data
    #http://api.weatherstack.com/current?access_key=c4e94a14f446360bc7d07ae8bb5eea49&query=Detroit

#from strava
#will find 100 runs on each of the 8 dates passed in from the list (what get_uv_dates() returns), 
# and create a list of the speed/pace of the runs. will return list of 100 paces
def get_uv_speeds(uv_dates_list):
    pass

#creates a new table for the uv data. will have the 8 uv indices on x axis, 
# and the 100 speeds found (using get_uv_speeds) going down the columns for each uv index
def create_uv_db(uv_speeds_list):
    pass

#calculates the average speed of the 100 runs and adds a row to the db 
# that says the avg speed for each uv index
def calc_avg_speed_from_uvs():
    pass

#generates line graph using matplotlib for uv indices
def create_uv_table():
    pass


def main():
    print("This is main")
    pass

main()

if __name__ == '__main__':
    unittest.main(verbosity=2)

