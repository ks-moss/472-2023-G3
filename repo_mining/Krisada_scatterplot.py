import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import os
import math
import numpy as np



# Read input file
file_path = "commit_author_date.txt"
file_content = []

if os.path.isfile(file_path):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            for row in file:
                file_content.append(row)
    except IOError as e:
        print(f"An error occurred while opening the file: {e}")
else:
    print("The file could not be found")



# Split file paths away from author's name and dates
#  Save all file paths
file_path_data = []
author_and_date = []

for x in range(len(file_content)):
    data = file_content[x].split(";")   # file path; name, date, name, date, name, date, ...
    file_path_data.append(data[0])      # file path
    author_and_date.append(data[1].split(","))  # name, date, name, date, ...



# Split authors and dates from author_date
# Store authors and dates in its own variable
# Store data in sort_dates and get ready for sortin
authors_2D_array = []
dates_2D_array = []
temp_authors = []
temp_dates = []
sort_dates = []

for i in range(len(author_and_date)):
    temp_author_date = author_and_date[i]

    for j in range(len(temp_author_date)):
        if (j%2)==0:     
            temp_authors.append(temp_author_date[j])
        
        if (j%2)==1:
           
            temp = temp_author_date[j].replace("\n", "").split("T")
            temp = temp[0].replace("-", ",")
            
            temp_dates.append(temp)
            sort_dates.append(temp.split(","))

    authors_2D_array.append(temp_authors)
    dates_2D_array.append(temp_dates)
    temp_authors = []
    temp_dates = []



# Sort all dates from oldest to latest date
# Get the oldest date from the list
def get_week_diff(sorted_dates):
    input_date = date(int(sorted_dates[0][0]),int(sorted_dates[0][1]),int(sorted_dates[0][2]))
    sorted_dates.reverse()
    latest_date_temp = date(int(sorted_dates[0][0]),int(sorted_dates[0][1]),int(sorted_dates[0][2]))
    diff = latest_date_temp - input_date
    return math.ceil(diff.days / 7)

sorted_dates = sorted(sort_dates, key=lambda x: datetime(int(x[0]), int(x[1]), int(x[2])))
oldest_date = date(int(sorted_dates[0][0]),int(sorted_dates[0][1]),int(sorted_dates[0][2]))
total_weeks = get_week_diff(sorted_dates)
latest_date = date(int(sorted_dates[0][0]),int(sorted_dates[0][1]),int(sorted_dates[0][2]))



# Find number of weeks away from the oldest date
# static_date is assigned to be the oldest date in the list
weeks_away_2D_array = []
var_week = []

for i in range(len(dates_2D_array)):
    temp_week = dates_2D_array[i]

    for j in range(len(temp_week)):
        temp = temp_week[j].split(",")
        delta = latest_date - date(int(temp[0]), int(temp[1]), int(temp[2]))
        var_week.append(delta.days // 7)

    weeks_away_2D_array.append(var_week)
    var_week = []



# Get individual author name
# No duplicated name
# Get ready for assigning colors for each author
individual_author = []
authors_1D_array = [author for sublist in authors_2D_array for author in sublist]
      
for i in range(len(authors_1D_array)):
    temp = authors_1D_array[i]
    duplicated = False
    
    if (len(individual_author)) == 0:
        individual_author.append(temp)
    else:
        for j in range(len(individual_author)):
            if (individual_author[j]) == temp:
                    duplicated = True
        if(duplicated == False):
            individual_author.append(temp)



# Get total number of weeks
# Get total number of files
number_files  = [] # 0 ... n
number_weeks = [] # 0 ... n

for j in range(len(file_path_data)):
    number_files.append(j)

for i in range(total_weeks):
    number_weeks.append(i)



# Assign color for each author
# Create a list of unique authors
unique_authors = list(set(individual_author))
# Create a list of random colors
colors = np.random.rand(len(unique_authors),3)
# Use enumerate to assign a unique color to each author
author_color = {author:colors[i] for i, author in enumerate(unique_authors)}

# Plot
fig, ax = plt.subplots()

print("\n\nPlotting, please wait ...\n\n")


for i, authors in enumerate(authors_2D_array):
    for author in authors:
        weeks_away = weeks_away_2D_array[i]
        color_values = [author_color[a] for a in authors]
        for j, week in enumerate(weeks_away):
            ax.scatter(number_files[i], number_weeks[week], color=color_values[j])

ax.set_xlabel('Files')
ax.set_ylabel('Weeks')

plt.show()