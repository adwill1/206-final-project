
# SI 206 Final Project- Covid API
# Name: Sarah 

import json
import unittest
import os
import requests
import matplotlib
import sqlite3

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
    #print(cases_list)
    #print(len(cases_list))
    return cases_list

def get_deaths_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    deaths_list = []
    for country_key in dict_list:
        deaths = dict_list[country_key]["All"]["deaths"]
        deaths_list.append(deaths)
    #print(deaths_list)
    #print(len(deaths_list))
    return deaths_list

def create_full_dictionary():
    country_list = get_countries_from_api()
    cases_list = get_cases_from_api()
    deaths_list = get_deaths_from_api()

    tuples_list = []
    for i in range(len(country_list)):
        tup = (country_list[i], cases_list[i], deaths_list[i])
        tuples_list.append(tup)
    #print(tuples_list)
    data_dictionary = {}
    sub_dict_list = []
    
    for tup in tuples_list:
        sub_dict = {}
        sub_dict["confirmed"] = tup[1]
        sub_dict["deaths"] = tup[2]
        sub_dict_list.append(sub_dict)
    
    for i in range(len(country_list)):
        for tup in tuples_list:
            country = tup[0]
            data_dictionary[country] = sub_dict_list[i]
    
    #print(data_dictionary)
    return data_dictionary

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

class TestCases(unittest.TestCase):
    def test_get_countries_from_api(self):
        country_list = get_countries_from_api()
        self.assertEqual(len(country_list), 197)
    
    def test_get_cases_from_api(self):
        cases_list = get_cases_from_api()
        self.assertEqual(len(cases_list), 197)

    def test_get_deaths_from_api(self):
        deaths_list = get_deaths_from_api()
        self.assertEqual(len(deaths_list), 197)
    
    def test_create_full_dictionary(self):
        data_dictionary = create_full_dictionary()
        self.assertEqual(len(data_dictionary), 197)
        self.assertEqual(list(data_dictionary.keys())[2], "Algeria")

def main():
    #print("This is main")
    get_countries_from_api()
    get_cases_from_api()
    get_deaths_from_api()
    create_full_dictionary()

main()
if __name__ == '__main__':
    unittest.main(verbosity=2)

