
# SI 206 Final Project- Covid API
# Name: Sarah 

import json
import unittest
import os
import requests
import matplotlib

#functions
def get_countries_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    country_list = list(dict_list.keys()) 
    print(country_list)
    print(len(country_list))
    return country_list

def get_region_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    region_list = []
    for country in dict_list:
        




class TestCases(unittest.TestCase):
    def country_list_length(self):
        country_list = get_countries_from_api()
        self.assertEqual(len(country_list), 197)


def main():
    print("This is main")
    get_countries_from_api()

main()
if __name__ == '__main__':
    unittest.main(verbosity=2)

