<<<<<<< HEAD
#Combined code to link DBs and create visualizations

=======
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
import json
import unittest
import os
import requests
from bs4 import BeautifulSoup
import requests
import re
import csv
import matplotlib
import sqlite3

<<<<<<< HEAD
=======
def select_wealth_data():
    pass

def select_covid_data():
    pass

def select_country_data():
    pass


>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
#functions
def get_countries_from_api():
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    r = requests.get(url)
    data = r.text
    dict_list = json.loads(data)

    country_list = list(dict_list.keys()) 
<<<<<<< HEAD
=======
    #print(country_list)
    #print(len(country_list))
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
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
<<<<<<< HEAD
=======
    #print(continents_list)
    #print(len(continents_list))
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
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
<<<<<<< HEAD
=======
    #print(cases_list)
    #print(len(cases_list))
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
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
<<<<<<< HEAD
=======
    #print(deaths_list)
    #print(len(deaths_list))
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
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
<<<<<<< HEAD
=======
    #print(tuples_list)
>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
    data_dictionary = {}
    sub_dict_list = []
    
    for tup in tuples_list:
        sub_dict = {}
        sub_dict["confirmed"] = tup[1]
        sub_dict["deaths"] = tup[2]
        sub_dict["continent"] = tup[3]
        sub_dict_list.append(sub_dict)
<<<<<<< HEAD
    for i in range(len(country_list)):
        country = tuples_list[i][0]
        data_dictionary[country] = sub_dict_list[i]
    return data_dictionary

=======
    #print(sub_dict_list)
    for i in range(len(country_list)):
        country = tuples_list[i][0]
        data_dictionary[country] = sub_dict_list[i]
    
    print(data_dictionary)
    return data_dictionary

#set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

>>>>>>> f52bf1243c8044b34891de0a5411fbcf45f44531
#create the table for continents and ids
def create_continents_table(cur, conn, data_dictionary):
    continent_list = []
    for country in data_dictionary.keys():
        continent = data_dictionary[country]["continent"]
        if continent not in continent_list:
            continent_list.append(continent)
    
    #cur.execute("DROP TABLE IF EXISTS Continents")
    cur.execute("CREATE TABLE IF NOT EXISTS Continents (id INTEGER PRIMARY KEY, continent TEXT)")
    
    for i in range(len(continent_list)):
        cur.execute("INSERT INTO Continents (id, continent) VALUES (?,?)",(i,continent_list[i]))   

    conn.commit()   


#create the table for country, cases, deaths, continent_id
def create_covid_info_table(cur, conn, data_dictionary):
    #cur.execute("DROP TABLE IF EXISTS CovidInfo")
    cur.execute("CREATE TABLE IF NOT EXISTS CovidInfo (country TEXT PRIMARY KEY, confirmed_cases INTEGER, confirmed_deaths INTEGER, continent_id INTEGER)")
    
    for country in data_dictionary:
        name = country
        cases = data_dictionary[country]["confirmed"]
        deaths = data_dictionary[country]["deaths"]
        continent_name = data_dictionary[country]["continent"]
    
        cur.execute("SELECT id FROM Continents WHERE continent = ?", (continent_name,))
        continent_ids = cur.fetchall()
        for cont in continent_ids:
            continent_id = cont[0]
        cur.execute("INSERT INTO CovidInfo (country, confirmed_cases, confirmed_deaths, continent_id) VALUES (?,?,?,?)", (name, cases, deaths, continent_id))
    conn.commit()
     
#WEALTH DATA
def get_country_name():
    url = "https://en.wikipedia.org/wiki/Distribution_of_wealth"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    count = 1
    list = []
    table = soup.find('table', class_='wikitable sortable')
    rows = table.findAll('a')
    for element in rows:
        cur_country = element.get('title')
        cur_tup = (count, cur_country)
        list.append(cur_tup)
        count = count + 1
    return list

#will return a list with each element as a tuple: (country id, wealth mean)
def get_dist_weath_mean():
    url = "https://en.wikipedia.org/wiki/Distribution_of_wealth"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    count = 1
    mean_list = []
    table = soup.find('table', class_='wikitable sortable')
    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        cur_data = row.find_all('td')
        if not len(cur_data) == 0:
            cur_tup = (count, cur_data[2].text)
            mean_list.append(cur_tup)
            count = count + 1
    return mean_list


#will return a list of tuples with each tuple as a (country name,wealth median)
def get_dist_wealth_median():
    url = "https://en.wikipedia.org/wiki/Distribution_of_wealth"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    count = 1
    median_list = []
    table = soup.find('table', class_='wikitable sortable')
    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        cur_data = row.find_all('td')
        if not len(cur_data) == 0:
            cur_tup = (count, cur_data[3].text)
            median_list.append(cur_tup)
            count = count + 1
    return median_list

#key = id, value = {'name': 'afghanistan', 'mean':3, 'median':7}
def create_dict(country_list, means, medians):
    data_dict = {}
    for n in range(len(country_list)):
        cur_dict = {}
        cur_dict['name'] = country_list[n][1]
        cur_dict['mean'] = means[n][1]
        cur_dict['median'] = medians[n][1]
        data_dict[country_list[n][0]] = cur_dict

    return data_dict


#to set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


#set up weath db
#could either have everything in one file, and would have to 
# organize the stuff in a different way. This was we could add 
def setUpWealthDB(cur, conn, wealth_dict):
    #cur.execute("DROP TABLE IF EXISTS Wealth")
    cur.execute("CREATE TABLE IF NOT EXISTS Wealth (country_name TEXT PRIMARY KEY, mean_wealth INTEGER, median_wealth INTEGER)")
    for key in wealth_dict.keys():
        cur_key = key
        name = wealth_dict[cur_key]['name']
        mean = wealth_dict[cur_key]['mean']
        median = wealth_dict[cur_key]['median']
        cur.execute("INSERT INTO Wealth (country_name, mean_wealth, median_wealth) VALUES (?,?,?)", (name,mean,median))
    conn.commit()


def main():
    #covid database
    get_countries_from_api()
    get_continents_from_api()
    get_cases_from_api()
    get_deaths_from_api()
    data_dictionary = create_full_dictionary()
    cur, conn = setUpDatabase("Combined.db")
    create_continents_table(cur, conn, data_dictionary)
    create_covid_info_table(cur, conn, data_dictionary)
    
    #wealth database
    name = get_country_name()
    means = get_dist_weath_mean()
    medians = get_dist_wealth_median()
    full_dict = create_dict(name, means, medians)
    setUpWealthDB(cur, conn, full_dict)

    conn.close()

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
