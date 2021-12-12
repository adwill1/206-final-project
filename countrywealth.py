
# SI 206 Final Project- country wealth web scrape
# Name: Lauren Fulcher

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

#web scrape to get...
#median wealth per US adult for each country
#mean wealth per US adult for each country
#put them into a database with country id as row border, 
# then country name, wealth dist mean, wealth dist median as column borders

# return a list with a country id for each country name as the first tuple element and the name as the second
# will have every country listed in the table of the wiki page
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
    cur.execute("DROP TABLE IF EXISTS Wealth")
    cur.execute("CREATE TABLE IF NOT EXISTS Wealth (country_name TEXT PRIMARY KEY, mean_wealth INTEGER, median_wealth INTEGER)")
    for key in wealth_dict.keys():
        cur_key = key
        name = wealth_dict[cur_key]['name']
        mean = wealth_dict[cur_key]['mean']
        median = wealth_dict[cur_key]['median']
        cur.execute("INSERT INTO Wealth (country_name, mean_wealth, median_wealth) VALUES (?,?,?)", (name,mean,median))
    conn.commit()


#creates a visual for median vs mean 
def create_visual():
    pass


class TestCases(unittest.TestCase):

    def test_get_country_name(self):
        id = get_country_name()
        self.assertEqual(len(id), 168)
        self.assertEqual(type(id), list)
        self.assertEqual(type(id[0]), tuple)
        self.assertEqual(type(id[0][0]), int)
        self.assertEqual(type(id[0][1]), str)
        self.assertEqual(id[3][0], 4)

    def test_get_wealth_mean(self):
        mean = get_dist_weath_mean()
        self.assertEqual(len(mean), 168)
        self.assertEqual(type(mean), list)
        self.assertEqual(mean[0][1], '1,744')

    def test_get_wealth_median(self):
        median = get_dist_wealth_median()
        self.assertEqual(len(median), 168)
        self.assertEqual(type(median), list)
        self.assertEqual(median[0][1], '734')

    def test_create_dict(self):
        name = get_country_name()
        means = get_dist_weath_mean()
        medians = get_dist_wealth_median()
        cur_dict = create_dict(name, means, medians)
        self.assertEqual(len(cur_dict), 168)
        self.assertEqual(type(cur_dict), dict)
        first_key = list(cur_dict.keys())[0]
        first_val = list(cur_dict.values())[1]
        self.assertEqual(type(first_key), int)
        self.assertEqual(type(first_val), dict)
        self.assertEqual(first_key, 1)
        self.assertEqual(len(first_val), 3)

def main():
    cur, conn = setUpDatabase("wealthData.db")
    name = get_country_name()
    means = get_dist_weath_mean()
    medians = get_dist_wealth_median()
    full_dict = create_dict(name, means, medians)
    setUpWealthDB(cur, conn, full_dict)

    conn.close()


main()
if __name__ == '__main__':
    unittest.main(verbosity=2)
