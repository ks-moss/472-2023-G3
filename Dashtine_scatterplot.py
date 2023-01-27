import json
import requests
import csv
import random
import os
import matplotlib.pyplot as plt


#Creating a dictionary from the CSV file containing file name, author, date

dictFiles = {}
auth_colors = dict()
r = random.random()
g = random.random()
b = random.random()
rand_color = (r,g,b)
lst = ()
with open("myCSV.csv", 'r') as file:
    read = csv.DictReader(file)

    for line in csv.DictReader(file):
        auth_colors[line['Author']] = rand_color
        file_name = os.path.basename(line['Filename'])
        check_file = dictFiles.get(file_name)
        if check_file is not None: 
            check_auth = dictFiles.get(file_name, {}).get(line['Author'])
            if check_auth is not None:
                authdates = [dictFiles[file_name].get(line['Author'], ',') for pkey in dictFiles[file_name]]
                dictFiles[file_name][line['Author']] = []
                dictFiles[file_name][line['Author']] = authdates
               
        else:
            dictFiles[file_name] = {}
            dictFiles[file_name][line['Author']] = line['Date']


x =[3, 2, 1]
 
y =[1, 2, 3]
 
plt.scatter(x, y, c =rand_color)
plt.xlabel("File")
plt.ylabel("Week")

# To show the plot
plt.show()
