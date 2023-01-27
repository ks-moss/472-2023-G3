import json
import requests
import csv
import os
from datetime import datetime, timedelta

folder = 'C:/Users/Cody/Documents/GitHub/472-2023-G3/repo_mining/data/'

# Open a text file to write the information to
with open('authorFileTouches.txt', 'w') as f:
    current_dir = os.getcwd()
    folder = current_dir+'\\data\\file_rootbeer.csv'
    ifile = open(folder,"rt")
    csvreader = csv.reader(ifile)
    min_date_str = "2015-05-19"
    min_date = datetime.strptime(min_date_str, "%Y-%m-%d")

    for row in csvreader:
        if len(row)>2:
            filename = row[0]
            data = row[1].split(",")
            loop1 = int(data[0][1:])
            for i in range(loop1):
                if i % 2 == 0:
                    name = data[i+1][2:-1]
                if i % 2 != 0:
                    date = data[i+1][2:-11]
                    date = datetime.strptime(date,"%Y-%m-%d")
                    weeks = (date - min_date).days / 7
                    # Write the filename, name, and date (in weeks) to text file
                    f.write(f"{filename}, {name}, {weeks}\n")
