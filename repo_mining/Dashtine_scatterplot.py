import json
import requests
import csv
import random
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime
import numpy as np
#Creating a dictionary from the CSV file containing file name, author, date

dictFiles = dict()
auth_colors = dict()
r = random.random()
g = random.random()
b = random.random()
rand_color = (r,g,b)
lst_filenames = []
index = 0
lst = ['random', 'listhere']
details = defaultdict(list)
fileNum = dict()
index = 0
newest_date = 0
oldest_date = 0
with open("authorData.csv", 'r') as file:
    read = csv.DictReader(file)

    for line in csv.DictReader(file):
        #assigning random color to each author
        auth_colors[line['Author']] = rand_color
        file_name = line['Filename']
        if file_name in dictFiles.keys(): 
            dictFiles[file_name].append(line['Author'])
            date1 = line['Date'].split('-')
            date2 = date1[2].split('T')
            date = [date1[0], date1[1],date2[0]]
            week_num = datetime.date(int(date1[0]), int(date1[1]), int(date2[0])).isocalendar()[1]
            dictFiles[file_name].append(week_num)
        else:
            lst_filenames.append(file_name) 
            dictFiles[file_name] = []
            dictFiles[file_name].append(line['Author'])
            date1 = line['Date'].split('-')
            date2 = date1[2].split('T')
            date = [date1[0], date1[1],date2[0]]
            week_num = datetime.date(int(date1[0]), int(date1[1]), int(date2[0])).isocalendar()[1]
            dictFiles[file_name].append(week_num)
            fileNum[file_name] = index
            index += 1


for file in lst_filenames:
    list_length = len(dictFiles[file])
    j = 0
    for i in range(list_length-1):
        x = []
        y = []
        auth = dictFiles[file][j]
        week = dictFiles[file][j+1]
        x.append(auth)
        y.append(week) 
        plt.scatter(x,y, color=auth_colors[auth])


plt.xlabel("File")
plt.ylabel("Week") 
plt.show()