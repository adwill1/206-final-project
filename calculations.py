from logging import info
import sqlite3
import unittest
import os
import matplotlib.pyplot as plt
import csv

#ABBY'S CALCULATION
#get people_vaccinated from CovidInfo and divide by population from Country_Information using JOIN
def calc_percent_vaccinated(cur, conn):
   cur.execute('''SELECT Wealth.mean_wealth, CovidInfo.people_vaccinated, Country_Information.population, CovidInfo.country
   FROM (CovidInfo
   JOIN Wealth ON CovidInfo.country=Wealth.country_name)
   JOIN Country_Information
   ON CovidInfo.country=Country_Information.country_territory_name
   ''')
   d = cur.fetchall()
   conn.commit()  
   print(d)
   percent_dict = {}
   for x in d:
       wealth = x[0]
       pop = x[2]
       vax = x[1]
       country = x[3]
       percent = vax/pop
       if percent <= 1:
           if country not in percent_dict:
               percent = percent * 100
               percent_dict[country] = ((wealth, round(percent)))
   print(percent_dict)
   return percent_dict
 
def create_percent_vax_vis(percent_dict):
  x = []
  y = []
  for key in percent_dict.keys():
     cur_x = percent_dict[key][0]
     cur_y = percent_dict[key][1]
     if ',' in str(cur_x):
         cur_x = percent_dict[key][0].replace(',','')
     if ',' in str(cur_y):
         cur_y = percent_dict[key][1].replace(',','')
     cur_x = float(cur_x)
     cur_y = float(cur_y)
     if cur_x < 9000 or cur_x > 550000:
         continue
     x.append(cur_x)
     y.append(cur_y)
  plt.scatter(x,y)
  plt.ylabel("Vaccination Percentage")
  plt.xlabel("Mean Wealth (in USD)")
  plt.title("Percent Vaccinated vs Wealth")
  plt.show()


def write_csv(file_name, percent_dict):
    with open(file_name, "w", newline="") as fileout:
        header =  ["Country"] + ["Percent Vaccinated"]
        csv_write = csv.writer(fileout, delimiter= ',')
        csv_write.writerow(header)
        for info in percent_dict:
            country_list = []
            country_list.append(info)
            country_list.append(percent_dict[info][1])
            csv_write.writerow(country_list)
    return None


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

def create_wealth_subreg_vis(org_dict):
    y = []
    x = []
    for key in org_dict.keys():
        y.append(key)
        x.append(org_dict[key])
    plt.barh(y,x)
    plt.ylabel("Sub Region")
    plt.yticks(rotation=45, ha='right')
    plt.xlabel("Average Wealth (in USD)")
    plt.title("Average Wealths of Sub Regions")
    plt.show()
        

#SARAH'S CALCULATION
#get country info and people_vaccinated info from CovidInfo and continent info from continent using JOIN
def get_continent_vaxxes(cur, conn):
    cur.execute('''SELECT CovidInfo.country, CovidInfo.people_vaccinated, Continents.continent 
    FROM CovidInfo 
    JOIN Continents 
    ON CovidInfo.continent_id=Continents.id
    ''')
    data = cur.fetchall()
    conn.commit()
    # print(data)
    return data

def create_cont_vax_dict(info_list):
    cont_vax_dict={}
    
    for tup in info_list:
        country = tup[0]
        vaxxes = tup[1]
        cont = tup[2]
        if cont not in cont_vax_dict.keys():
            cont_vax_dict[cont] = []
        cont_vax_dict[cont].append(vaxxes)
    # print(cont_vax_dict)
    return cont_vax_dict 

def calc_cont_vax_total(cont_vax_dict):
    total_dict = {}

    for continent, vax_list in cont_vax_dict.items():
        vax_total = 0
        for num in vax_list:
            vax_total += num
        total_dict[continent] = (vax_total/1000000000)
    print(total_dict)
    return total_dict

#create visual comparing vaccination numbers by continent
def create_cont_vax_visual(total_dict): 
    x_continents = []
    y_vaccine_totals = []
    for cont in total_dict:
        x_continents.append(cont)
        y_vaccine_totals.append(total_dict[cont])
    x_continents = x_continents[0:6]
    y_vaccine_totals = y_vaccine_totals[0:6]
    plt.bar(x_continents,y_vaccine_totals)
    plt.ylabel("Vaccination Numbers (in Billions)")
    plt.xlabel("Continent")
    plt.title("Vaccination Totals by Continent")
    plt.show()

#EXTRA CALCULATION- line graph of median_wealth on x axis and life expectancy on y axis
#get median_wealth from Wealth and life expectancy from CovidInfo, return list of tups
def calc_avg_life_exp_of_cont(cur, conn):
   cur.execute('''SELECT Wealth.median_wealth,CovidInfo.life_expectancy
   FROM Wealth
   JOIN CovidInfo
   ON CovidInfo.country=Wealth.country_name
   ''')
   list_both = cur.fetchall()
   conn.commit()
   new_list = []
   for tup in list_both:
       if tup[0]=="N/A" or tup[1]=="N/A" or not type(tup[1])==float:
           continue
       else:
           cur_tup = (tup[0], tup[1])
           new_list.append(cur_tup)
   return new_list
  
def create_extra_vis(list_tups):
   list_x = []
   list_y = []
   for tup in list_tups:
       cur_x = tup[0]
       cur_y = tup[1]
       if ',' in str(cur_x):
           cur_x = tup[0].replace(',','')
       if ',' in str(cur_y):
           cur_y = tup[1].replace(',','')
       cur_x = float(cur_x)
       cur_y = float(cur_y)
       if cur_x > 150000:
           continue
       list_x.append(cur_x)
       list_y.append(cur_y)
 
   plt.scatter(list_x,list_y)
   plt.title('Wealth vs Life Expectancy')
   plt.xlabel('Median Wealth per Adult (in USD)')
   plt.ylabel('Life Expectancy')
   plt.show()

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
        #create_wealth_subreg_vis(org_dict)

    
    def test_get_cont_vax(self):
        info_list = get_continent_vaxxes(self.cur, self.conn)
        #create_cont_vax_dict(info_list)

    def test_calc_percent_vaccinated(self):
       calc_percent_vaccinated(self.cur, self.conn)
    
    def test_create_cont_vax_visual(self):
        cont_vax_data = get_continent_vaxxes(self.cur, self.conn)
        cont_vax_dict = create_cont_vax_dict(cont_vax_data)
        cont_vax_total = calc_cont_vax_total(cont_vax_dict)
        #create_cont_vax_visual(cont_vax_total)

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Combined.db')
    cur = conn.cursor()
    write_csv("percent_vaccinated.csv", calc_percent_vaccinated(cur, conn))

    #Visual 1
    percent_dict = calc_percent_vaccinated(cur, conn)
    create_percent_vax_vis(percent_dict)

    #Visual 2 
    all_data = get_wealth_of_subreg(cur, conn)
    full_dict = create_subreg_mean_dict(all_data)
    org_dict = calc_avg_wealth(full_dict)
    create_wealth_subreg_vis(org_dict)

    #Visual 3
    data = get_continent_vaxxes(cur, conn)
    cont_vax_dict = create_cont_vax_dict(data)
    cont_vax_total = calc_cont_vax_total(cont_vax_dict)
    create_cont_vax_visual(cont_vax_total)

    #Visual 4
    new_list = calc_avg_life_exp_of_cont(cur, conn)
    create_extra_vis(new_list)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
