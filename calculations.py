import sqlite3
import unittest
import os
import matplotlib.pyplot as plt

#_______'S CALCULATION
#get people_vaccinated from CovidInfo and divide by population from Country_Information using JOIN
def calc_percent_vaccinated(cur, conn):
    pass

#LAUREN'S CALCULATION
#get mean_wealth from WealthDB and sub_region from Country_Information using JOIN
def get_wealth_of_subreg(cur, conn):
    cur.execute('''SELECT Wealth.mean_wealth, Country_Information.sub_region 
    FROM Wealth 
    JOIN Country_Information 
    ON Wealth.country_name=Country_Information.country_territory_name
    ''')
    all_data = cur.fetchall()
    conn.commit()
    return all_data

#return a dict that has the subregion as a key, and a list as the key with the wealths?? 
def create_subreg_mean_dict(full_list):
    subreg_dict = {}
    for country in full_list:
        if not country[1] in subreg_dict.keys():
            new_list = [country[0]]
            subreg_dict[country[1]] = new_list
        else:
            subreg_dict[country[1]].append(country[0])
    return subreg_dict

#return an organized dict that has just the subregion as key and avg wealth as value
def calc_avg_wealth(full_dict):
    org_dict = {}
    for subreg in full_dict.keys():
        cur_length = len(full_dict[subreg])
        cur_list = full_dict[subreg]
        sum = 0
        for mean in cur_list:
            if ',' in str(mean):
                cur_mean = mean.replace(',','')
                final = int(cur_mean)
            else:
                final = int(mean)
            sum = sum + final
        average = sum / cur_length
        rounded = round(average, 2)
        org_dict[subreg] = rounded
    return org_dict

<<<<<<< HEAD
def create_wealth_subreg_vis(org_dict):
    pass
    y = []
    x = []
    for key in org_dict.keys():
        y.append(key)
        x.append(org_dict[key])
    plt.barh(y,x)
    plt.ylabel("Sub Region")
    plt.xlabel("Average Wealth")
    plt.title("Average Wealths of Sub Regions")
    plt.show()

=======
def create_wealth_subreg_vis():
    pass
>>>>>>> 64691494fec3ed69cb2ef1960ef99b19482c00df
        
#________'S CALCULATION
#get avg life_expectancy from CovidInfo for each continent (get continent_id using JOIN from Continents and CovidInfo)??
def calc_avg_life_exp_of_cont(cur, conn):
    pass

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'Combined.db')
        self.cur = self.conn.cursor()

    def test_calc_avg_mean_wealth_of_subreg(self):
        yuh = get_wealth_of_subreg(self.cur, self.conn)
        self.assertEqual(type(yuh), list)
        print(yuh[0])
        print(len(yuh))

    def test_create_subreg_mean_dict(self):
        full_list = get_wealth_of_subreg(self.cur, self.conn)
        full_dict = create_subreg_mean_dict(full_list)
        self.assertEqual(type(full_dict), dict)
        #print(full_dict['Southern Asia'])
        #print(type(full_dict['Southern Asia'][0]))

    def test_calc_avg_wealth(self):
        full_list = get_wealth_of_subreg(self.cur, self.conn)
        full_dict = create_subreg_mean_dict(full_list)
        org_dict = calc_avg_wealth(full_dict)
        self.assertEqual(len(org_dict), 22)
<<<<<<< HEAD
        create_wealth_subreg_vis(org_dict)
=======
        print(org_dict)
>>>>>>> 64691494fec3ed69cb2ef1960ef99b19482c00df

def main():
    pass

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
