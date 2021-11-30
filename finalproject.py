from bs4 import BeautifulSoup
import requests
import re
import csv
import json
import unittest
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import math

#
# Your name: Ruthie Dingeldein and Clare McAuliffe
#

#setting up database
db_name = 'Population Analysis'
def set_up(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute('SELECT city, population_density, Salaries.ranking, Salaries.average_hourly, population FROM Populations INNER JOIN Salaries ON Populations.city = Salaries.citystate')
    rest = cur.fetchall()
    conn.commit()
    return rest

#first figure 
def figure_one():
    plt.ylabel('Hourly Salary')
    plt.xlabel('Population Density')
    plt.title("Relationship between uber/lyft salaries and population density")
    hourlysalaries = []
    popdensities = []
    for city in reversed(set_up(db_name)):
        density = city[1].replace(",","")
        popdensities.append(int(density))
        sal = city[3].replace("$","")
        hourlysalaries.append((sal))
    plt.scatter(popdensities, hourlysalaries, color='r')

    plt.show()

#second figure (relation between pop and salary)
def figure_two():
    plt.ylabel('Hourly Salary')
    plt.xlabel('Population')
    plt.title("Relationship between uber/lyft salaries and population")
    hourlysalaries = []
    popdensities = []
    for city in reversed(set_up(db_name)):
        density = city[4].replace(",","")
        popdensities.append(int(density))
        sal = city[3].replace("$","")
        hourlysalaries.append((sal))
    plt.scatter(popdensities, hourlysalaries, color='g')

    plt.show()


#average salary by city type/third figure
def figure_three():
    small_total = 0
    small_count = 0
    medium_total = 0
    medium_count = 0
    large_total = 0
    large_count = 0
    for city in set_up(db_name):
        if int(city[1].replace(',', '')) < 5000:
            small_total += float(city[3][1:])
            small_count += 1
        elif int(city[1].replace(',', '')) < 10000:
            medium_total += float(city[3][1:])
            medium_count += 1
        else:
            large_total += float(city[3][1:])
            large_count += 1
    small_average = small_total/small_count
    medium_average = medium_total/medium_count
    large_average = large_total/large_count

    plt.ylabel('Average Hourly Salary')
    plt.xlabel('City Size')
    plt.title("Relationship between uber/lyft salaries and city size")

    size = ('Small', 'Medium', 'Large')
    y_pos = np.arange(len(size))
    hourly = [small_average, medium_average, large_average]

    plt.bar(y_pos, hourly, align='center', alpha=0.5, color = 'b', edgecolor='blue')
    plt.xticks(y_pos, size)
    plt.show()

#fourth figure
def figure_four(cur, conn):
    cur.execute('SELECT citystate FROM Salaries')
    topthree = cur.fetchall()
    topthree = topthree[0:3]

    #map plotting that works
    fig = plt.figure(figsize=(7, 7))
    m = Basemap(projection='lcc', resolution=None,
                width=8E6, height=8E6, 
                lat_0=45, lon_0=-100,)
    m.etopo(scale=0.5, alpha=0.5)

    # Map (long, lat) to (x, y) for plotting
    x, y = m(-122.3, 39)
    plt.plot(x, y, 'ok', markersize=3)
    plt.text(x, y, topthree[0][0], fontsize=8)
    #second
    x, y = m(-122.3, 47)
    plt.plot(x, y, 'ok', markersize=3)
    plt.text(x, y, topthree[1][0], fontsize=8)
    #third
    x, y = m(-121, 36)
    plt.plot(x, y, 'ok', markersize=3)
    plt.text(x, y, topthree[2][0], fontsize=8)
    plt.show()

#writing to a csv
def write_csv(datalist):
    with open('data', 'w', newline='') as file:
        writer = csv.writer(file)
        labels = ("City and State", "Population Density", "Ranking", "Hourly Salary", "Population")
        writer.writerow(labels)
        for entries in datalist:
            writer.writerow(entries)
            #file.flush()
        file.close()
        myfile = open("data", "r")
        #print(myfile.read())
        path = os.path.abspath('data')
        directory = os.path.dirname(path)
        #print(directory)
        myfile.close()


def main():
    datalist = set_up(db_name)
    figure_one()
    figure_two()
    figure_three()
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    figure_four(cur, conn)
    write_csv(datalist)
    conn.close()
    


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)


