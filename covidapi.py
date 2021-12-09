
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

#get continent
def get_continents_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    continents_list = []
    for country_key in dict_list:
        try:
            continent = dict_list[country_key]["All"]["continent"]
            continents_list.append(continent)
        except KeyError:
            continents_list.append("N/A")
    #print(continents_list)
    #print(len(continents_list))
    return continents_list

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
    continents_list = get_continents_from_api()
    cases_list = get_cases_from_api()
    deaths_list = get_deaths_from_api()

    tuples_list = []
    for i in range(len(country_list)):
        tup = (country_list[i], cases_list[i], deaths_list[i], continents_list[i])
        tuples_list.append(tup)
    #print(tuples_list)
    data_dictionary = {}
    sub_dict_list = []
    
    for tup in tuples_list:
        sub_dict = {}
        sub_dict["confirmed"] = tup[1]
        sub_dict["deaths"] = tup[2]
        sub_dict["continent"] = tup[3]
        sub_dict_list.append(sub_dict)
    
    for i in range(len(country_list)):
        for tup in tuples_list:
            country = tup[0]
            data_dictionary[country] = sub_dict_list[i]
    
    #print(data_dictionary)
    return data_dictionary

#set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#create the table for continents and ids
def create_continents_table(cur, conn, data_dictionary):
    cur.execute("DROP TABLE IF EXISTS Continents")
    cur.execute("CREATE TABLE IF NOT EXISTS Continents (id INTEGER PRIMARY KEY, continent TEXT)")
    
    continent_list = []
    for country in data_dictionary.keys():
        continent = data_dictionary[country]["continent"]
        continent_list.append(continent)
    
    for i in range(len(data_dictionary)):
        cur.execute("INSERT INTO Continents (id, continent) VALUES (?,?)",(i,continent_list[i]))   

    conn.commit()   


#create the table for country, cases, deaths, continent_id
def create_covid_deaths_database(cur, conn, data_dictionary):
    cur.execute("DROP TABLE IF EXISTS CovidInfo")
    cur.execute("CREATE TABLE IF NOT EXISTS CovidInfo (country TEXT PRIMARY KEY, confirmed_cases INTEGER, confirmed_deaths INTEGER, continent_id INTEGER)")
    
    for country in data_dictionary.keys():
        name = country
        cases = data_dictionary[country]["confirmed"]
        deaths = data_dictionary[country]["deaths"]
        continent_name = data_dictionary[country]["continent"]
    
        cur.execute("SELECT id FROM Continents WHERE continent = ?", continent_name)
        continent_ids = cur.fetchall()
        for cont in continent_ids:
            continent_id = cont[0]
    

        
    cur.execute("INSERT INTO CovidIndo (country, confirmed_cases, confirmed_deaths, continent_id) VALUES (?,?,?,?)", (name, cases, deaths, continent_id))
    conn.commit()
    
    
    
           
    pass 


class TestCases(unittest.TestCase):
    def test_get_countries_from_api(self):
        country_list = get_countries_from_api()
        self.assertEqual(len(country_list), 197)

    def test_get_continents_from_api(self):
        continent_list = get_continents_from_api()
        self.assertEqual(len(continent_list), 197)
    
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
    get_continents_from_api()
    get_cases_from_api()
    get_deaths_from_api()
    
    data_dictionary = create_full_dictionary()
    
    cur, conn = setUpDatabase("CovidInfo.db")
    create_continents_table(cur, conn, data_dictionary)
    create_covid_deaths_database(cur, conn, data_dictionary)
    

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)

