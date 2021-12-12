#Combined code to link DBs and create visualizations
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

#COVID DATA
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
    country_id = 0
    for tup in tuples_list:
        sub_dict = {}
        sub_dict["people_vaccinated"] = tup[1]
        sub_dict["life_expectancy"] = tup[2]
        sub_dict["continent"] = tup[3]
        sub_dict["country_id"] = country_id
        sub_dict_list.append(sub_dict)
        country_id +=1 
    #print(sub_dict_list)
    
    for i in range(len(country_list)):
        country = tuples_list[i][0]
        data_dictionary[country] = sub_dict_list[i]
    print(data_dictionary)
    return data_dictionary

#create the table for continents and ids
def create_continents_table(cur, conn, data_dictionary):
    continent_list = []
    for country in data_dictionary.keys():
        continent = data_dictionary[country]["continent"]
        if continent not in continent_list:
            continent_list.append(continent)
    
    #cur.execute("DROP TABLE IF EXISTS Continents")
    cur.execute("CREATE TABLE IF NOT EXISTS Continents (id INTEGER PRIMARY KEY, continent TEXT)")
    count = 0

    for i in range(len(continent_list)):
        cur.execute("INSERT OR IGNORE INTO Continents (id, continent) VALUES (?,?)",(i,continent_list[i]))   
        
    conn.commit()   

#create the table for country, cases, deaths, continent_id
def create_covid_info_table(cur, conn, data_dictionary):
    #cur.execute("DROP TABLE IF EXISTS CovidInfo")
    cur.execute("CREATE TABLE IF NOT EXISTS CovidInfo (country_id INTEGER PRIMARY KEY, country TEXT UNIQUE, people_vaccinated INTEGER, life_expectancy INTEGER, continent_id INTEGER)")
    count = 0
    for country in data_dictionary:
        name = country
        vaxxed = data_dictionary[country]["people_vaccinated"]
        life_exp = data_dictionary[country]["life_expectancy"]
        continent_name = data_dictionary[country]["continent"]
        country_id = data_dictionary[country]["country_id"]
    
        cur.execute("SELECT id FROM Continents WHERE continent = ?", (continent_name,))
        continent_ids = cur.fetchall()
        for cont in continent_ids:
            continent_id = cont[0]
        cur.execute("INSERT OR IGNORE INTO CovidInfo (country_id, country, people_vaccinated, life_expectancy, continent_id) VALUES (?,?,?,?,?)", (country_id, name, vaxxed, life_exp, continent_id))
        if cur.rowcount == 1:
            count += 1
            if count == 25:
                break
    #cur.execute("SELECT * FROM CovidInfo")
   
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

#set up weath db
#could either have everything in one file, and would have to 
# organize the stuff in a different way. This was we could add 
def setUpWealthDB(cur, conn, wealth_dict):
    cur.execute("DROP TABLE IF EXISTS Wealth")
    cur.execute("CREATE TABLE IF NOT EXISTS Wealth (country_name TEXT PRIMARY KEY, mean_wealth INTEGER, median_wealth INTEGER)")
    for key in wealth_dict.keys():
        cur_key = key
        name = wealth_dict[cur_key]['name']
        mean = wealth_dict[cur_key]['mean']
        median = wealth_dict[cur_key]['median']
        cur.execute("INSERT INTO Wealth (country_name, mean_wealth, median_wealth) VALUES (?,?,?)", (name,mean,median))
    conn.commit()

#COUNTRY DATA
#functions
def get_europe_data():
    url = 'https://restcountries.com/v3.1/region/europe'
    request = requests.get(url)
    data = request.text
    new_data = json.loads(data)
    europe_list = []
    for lst in new_data:
        country = lst['name']['common']
        population = lst['population']
        sub_region = lst['subregion']
        europe_list.append((country, population, sub_region,))
    return europe_list
    
def get_americas_data():
    url = 'https://restcountries.com/v3.1/region/americas'
    request = requests.get(url)
    data = request.text
    new_data = json.loads(data)
    americas_list = []
    for lst in new_data:
        country = lst['name']['common']
        population = lst['population']
        sub_region = lst['subregion']
        americas_list.append((country, population, sub_region))
    return americas_list

def get_africa_data():
    url = 'https://restcountries.com/v3.1/region/africa'
    request = requests.get(url)
    data = request.text
    new_data = json.loads(data)
    africa_list = []
    for lst in new_data:
        country = lst['name']['common']
        population = lst['population']
        sub_region = lst['subregion']
        africa_list.append((country, population, sub_region))
    return africa_list

def get_oceania_data(): 
    url = 'https://restcountries.com/v3.1/region/oceania'
    request = requests.get(url)
    data = request.text
    new_data = json.loads(data)
    oceania_list = []
    for lst in new_data:
        country = lst['name']['common']
        population = lst['population']
        sub_region = lst['subregion']
        oceania_list.append((country, population, sub_region))
    return oceania_list

def get_asia_data():
    url = 'https://restcountries.com/v3.1/region/asia'
    request = requests.get(url)
    data = request.text
    new_data = json.loads(data)
    asia_list = []
    for lst in new_data:
        country = lst['name']['common']
        population = lst['population']
        sub_region = lst['subregion']
        asia_list.append((country, population, sub_region))
    return asia_list

def combine_list(europe, americas, africa, oceania, asia):
    country_list = europe + americas + africa + oceania + asia
    sorted_list = sorted(country_list, key = lambda x: x[0])
    country_id = 1
    sorted_country_list = []
    for data in sorted_list:
        sorted_country_list.append((country_id, data))
        country_id += 1
    return sorted_country_list
    
def setUpCountryDatabase(cur, conn, country_list):
    cur.execute("CREATE TABLE IF NOT EXISTS Country_Information (country_id INTEGER PRIMARY KEY, country_territory_name TEXT UNIQUE, sub_region TEXT, population INTEGER)")
    count = 0
    for item in country_list:
        id = item[0]
        country = item[1][0]
        population = item[1][1]
        sub_region = item[1][2]
        cur.execute("INSERT OR IGNORE INTO Country_Information (country_id, country_territory_name, sub_region, population) VALUES (?,?,?,?)", (id , country, sub_region, population))
        if cur.rowcount == 1:
            count += 1
            if count == 25:
                break
    conn.commit()

#COMBINED FUNCTIONS

#to set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#def get_all_data(cur, conn):
#    cur.execute('''SELECT Wealth.country_name,CovidInfo.confirmed_cases,CovidInfo.confirmed_deaths,Wealth.mean_wealth,Wealth.median_wealth,Country_Information.sub_region,Country_Information.population 
#                FROM  CovidInfo
#                JOIN (Wealth JOIN Country_Information
#                ON Wealth.country_name=Country_Information.country_territory_name)
#                ON CovidInfo.country=Wealth.country_name''')
#    big_list = cur.fetchall()
#    conn.commit()
#    return big_list

#ef create_final_table(cur, conn, data):
#    cur.execute('''CREATE TABLE IF NOT EXISTS Complete 
#    (country TEXT PRIMARY KEY, confirmed_cases INTEGER, deaths INTEGER, 
#    mean_wealth INTEGER, median_wealth INTEGER, subregion TEXT, population INTEGER)
#    ''')
#    for tup in data:
#        country = tup[0]
#        confirmed = tup[1]
#        deaths = tup[2]
#        mean = tup[3]
#        median = tup[4]
#        subreg = tup[5]
#        pop = tup[6]
#        cur.execute('INSERT INTO Complete (country, confirmed_cases, deaths, mean_wealth, median_wealth, subregion, population) VALUES (?,?,?,?,?,?,?)', (country, confirmed, deaths, mean, median, subreg, pop))
#    conn.commit()
#    pass


def main():

    cur, conn = setUpDatabase("Combined.db")

    #covid database
    get_countries_from_api()
    get_continents_from_api()
    get_ppl_vax_from_api()
    get_life_ex_from_api()
    data_dictionary = create_full_dictionary()
    create_continents_table(cur, conn, data_dictionary)
    create_covid_info_table(cur, conn, data_dictionary)
    
    #wealth tables
    name = get_country_name()
    means = get_dist_weath_mean()
    medians = get_dist_wealth_median()
    full_dict = create_dict(name, means, medians)
    setUpWealthDB(cur, conn, full_dict)

    #country tables
    country_list = combine_list(get_europe_data(), get_americas_data(), get_africa_data(), get_oceania_data(), get_asia_data())
    setUpCountryDatabase(cur, conn, country_list)

    #combine tables
#    all = get_all_data(cur,conn)
#    print(all[0])
#    print(len(all))
#    print(type(all))

#    create_final_table(cur, conn, all)

    conn.close()

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
