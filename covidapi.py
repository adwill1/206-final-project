
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
    #print(country_list)
    #print(len(country_list))
    return country_list

def get_cases_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)
    
    cases_list = []
    for country_key in dict_list:
        cases = dict_list[country_key]["All"]["confirmed"]
        cases_list.append(cases)
    print(cases_list)
    print(len(cases_list))
    return cases_list

def get_deaths_from_api():




class TestCases(unittest.TestCase):
    def test_get_countries_from_api(self):
        country_list = get_countries_from_api()
        self.assertEqual(len(country_list), 197)
    
    def test_get_cases_from_api(self):
        cases_list = get_cases_from_api()
        self.assertEqual(len(cases_list), 197)

def main():
    print("This is main")
    get_countries_from_api()
    get_cases_from_api()

main()
if __name__ == '__main__':
    unittest.main(verbosity=2)

