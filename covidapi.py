
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
    url = "https://covid-api.mmediagroup.fr/v1/vaccines"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    country_list = list(dict_list.keys()) 
    #print(country_list)
    #print(len(country_list))
    return country_list

#get continent
def get_continents_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/vaccines"
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

def get_ppl_vax_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/vaccines"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)
    vax_list = []
    for country_key in dict_list:
        vaxxed = dict_list[country_key]["All"]["people_vaccinated"]
        vax_list.append(vaxxed)
    #print(vax_list)
    #print(len(vax_list))
    return vax_list

def get_life_ex_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/vaccines"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)
    life_ex_list = []
    for country_key in dict_list:
        try:
            cur_life_ex = dict_list[country_key]["All"]["life_expectancy"]
            life_ex_list.append(cur_life_ex)
        except KeyError:
            life_ex_list.append("N/A")
    #print(life_ex_list)
    #print(len(life_ex_list)
    return life_ex_list

def create_full_dictionary():
    country_list = get_countries_from_api()
    continents_list = get_continents_from_api()
    vaxxed_list = get_ppl_vax_from_api()
    life_exp_list = get_life_ex_from_api()
    tuples_list = []
    for i in range(len(country_list)):
        tup = (country_list[i], vaxxed_list[i], life_exp_list[i], continents_list[i])
        tuples_list.append(tup)
    #print(tuples_list)
    
    data_dictionary = {}
    sub_dict_list = []
    for tup in tuples_list:
        sub_dict = {}
        sub_dict["people_vaccinated"] = tup[1]
        sub_dict["life_expectancy"] = tup[2]
        sub_dict["continent"] = tup[3]
        sub_dict_list.append(sub_dict)
    #print(sub_dict_list)
    
    for i in range(len(country_list)):
        country = tuples_list[i][0]
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
    continent_list = []
    for country in data_dictionary.keys():
        continent = data_dictionary[country]["continent"]
        if continent not in continent_list:
            continent_list.append(continent)
    
    cur.execute("DROP TABLE IF EXISTS Continents")
    cur.execute("CREATE TABLE IF NOT EXISTS Continents (id INTEGER PRIMARY KEY, continent TEXT)")
    
    for i in range(len(continent_list)):
        cur.execute("INSERT INTO Continents (id, continent) VALUES (?,?)",(i,continent_list[i]))   

    conn.commit()   


#create the table for country, cases, deaths, continent_id
def create_covid_info_table(cur, conn, data_dictionary):
    cur.execute("DROP TABLE IF EXISTS CovidInfo")
    cur.execute("CREATE TABLE IF NOT EXISTS CovidInfo (country TEXT PRIMARY KEY, people_vaccinated INTEGER, life_expectancy INTEGER, continent_id INTEGER)")
    
    for country in data_dictionary:
        name = country
        vaxxed = data_dictionary[country]["people_vaccinated"]
        life_exp = data_dictionary[country]["life_expectancy"]
        continent_name = data_dictionary[country]["continent"]
    
        cur.execute("SELECT id FROM Continents WHERE continent = ?", (continent_name,))
        continent_ids = cur.fetchall()
        for cont in continent_ids:
            continent_id = cont[0]
        cur.execute("INSERT INTO CovidInfo (country, people_vaccinated, life_expectancy, continent_id) VALUES (?,?,?,?)", (name, vaxxed, life_exp, continent_id))
    cur.execute("SELECT * FROM CovidInfo")
    print(cur.rowcount)
    conn.commit() 



     
     
class TestCases(unittest.TestCase):
    def test_get_countries_from_api(self):
        country_list = get_countries_from_api()
        self.assertEqual(len(country_list), 197)

    def test_get_continents_from_api(self):
        continent_list = get_continents_from_api()
        self.assertEqual(len(continent_list), 197)
    
    def test_get_ppl_vax_from_api(self):
        vax_list = get_ppl_vax_from_api()
        self.assertEqual(len(vax_list), 197)

    def test_get_life_ex_from_api(self):
        life_ex_list = get_life_ex_from_api()
        self.assertEqual(len(life_ex_list), 197)
    
    def test_create_full_dictionary(self):
        data_dictionary = create_full_dictionary()
        self.assertEqual(len(data_dictionary), 197)
        self.assertEqual(list(data_dictionary.keys())[2], "Algeria")
        self.assertEqual(data_dictionary["Cambodia"]["continent"], "Asia")

def main():
    #print("This is main")
    get_countries_from_api()
    get_continents_from_api()
    get_ppl_vax_from_api()
    get_life_ex_from_api()
    
    data_dictionary = create_full_dictionary()
    
    cur, conn = setUpDatabase("CovidInfo.db")
    create_continents_table(cur, conn, data_dictionary)
    create_covid_info_table(cur, conn, data_dictionary)
    conn.close()

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)

