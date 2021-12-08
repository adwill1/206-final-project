
# SI 206 Final Project- country wealth web scrape
# Name: 

import json
import unittest
import os
import requests
from bs4 import BeautifulSoup
import requests
import re
import csv
import matplotlib

#web scrape to get...
#median wealth per US adult for each country
#mean wealth per US adult for each country
#put them into a database with country id as row border, 
# then country name, wealth dist mean, wealth dist median as column borders

# return a dict with a country id for each country name as the key and the name as the val
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


#will return a dict with each key:val as a country name:wealth median
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

#will create table if not exists with a country id
def create_wealth_db():
    pass

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




def main():
    yuh = get_country_name()
    print(yuh)

main()
if __name__ == '__main__':
    unittest.main(verbosity=2)

