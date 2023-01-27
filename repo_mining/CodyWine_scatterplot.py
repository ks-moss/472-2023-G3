import json
import requests
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

if not os.path.exists("data"):
    os.makedirs("data")

def arrayCheck(arr,string):
    if string in arr:
        return arr.index(string)
    else:
        arr.append(string)
        return len(arr)-1

arrName = []
arrDate = []
min_date_str = "2015-05-19"
min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
colors = ['blue','green','red','cyan','magenta','yellow','purple','orange','black','pink']
ifile = open('data/file_rootbeer.csv',"rt")
csvreader = csv.reader(ifile)
plt.xlabel("File")
plt.ylabel("Weeks")

with open("authorFileTouches.txt", "w") as f:
    index = 0
    for row in csvreader:
        if len(row)>2:
            filename = row[0]
            data = row[1].split(",")
            loop1 = int(data[0][1:])
            for i in range(loop1):
                if i % 2 == 0:
                    name = data[i+1][2:-1]
                    if name not in arrName:
                        arrName.append(name)
                    name_index = arrName.index(name)
                if i % 2 != 0:
                    new_date = datetime.strptime(data[i+1][2:-11],"%Y-%m-%d")
                    week_date = (new_date - min_date).days / 7
                    if week_date not in arrDate:
                        arrDate.append(week_date)
                    date_index = arrDate.index(week_date)
                    f.write(f"{filename},{name},{new_date}\n")
                    plt.scatter(name_index, date_index*10, c=colors[arrName.index(name) % len(colors)])
                    index += 1
plt.xlabel("File")
plt.ylabel("Weeks")
plt.show()
