
# SI 206 Final Project- Rest Countries API
# Name: Abby Williams

import json
import unittest
import os
import requests
import matplotlib
import sqlite3


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

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

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

def main():
    print("This is main")
    cur, conn = setUpDatabase("countryData.db")
    country_list = combine_list(get_europe_data(), get_americas_data(), get_africa_data(), get_oceania_data(), get_asia_data())
    setUpCountryDatabase(cur, conn, country_list)
    conn.close()

main()
if __name__ == '__main__':
    unittest.main(verbosity=2)