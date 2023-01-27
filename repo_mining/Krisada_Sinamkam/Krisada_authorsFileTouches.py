import os
import csv
import json
import requests

file_path = "/Users/krisadasinamkam/Desktop/CS 472/test/data/file_rootbeer.csv"

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# GitHub access token
lstTokens = ["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  (REMOVE-THIS)",
                "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  (REMOVE-THIS)",
                "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  (REMOVE-THIS)"]

# Create an output file
out_file = open("commit_author_date.txt", "a")

file_content = []
data = []

# Read input file
if os.path.isfile(file_path):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            for row in file:
                file_content.append(row)
    except IOError as e:
        print(f"An error occurred while opening the file: {e}")
else:
    print("The file could not be found")

for x in range(1, len(file_content), 1):
    data.append(file_content[x].replace("\r\n", "").split(","))


ct=0 # token counter
for x in data:
    file_path = x[0]
    touch_count = int(x[1])

    # Get commit history for the file
    url = f"https://api.github.com/repos/{repo}/commits?path={file_path}"
    ct = ct % len(lstTokens)
    headers = {'Authorization': 'Bearer {}'.format(lstTokens[ct])}
    ct+=1
    response = requests.get(url, headers=headers)
    commits = response.json()

    if touch_count > len(commits):
        touch_count = len(commits)

    # Write file path name
    if touch_count != 0:
        # this will return a tuple of root and extension
        print(file_path)
        
        split_tup = os.path.splitext(file_path)
    
        if split_tup[1] == ".java":

            out_file.write(file_path + ";")

            for i in range(touch_count):
                # Get the author name and date
                author_name = commits[i]["commit"]["author"]["name"]
                date = commits[i]["commit"]["author"]["date"]

                # Write file path name and date
                out_file.write(author_name + "," + date)
                
                if i < (touch_count-1):
                    out_file.write(",")
            
            out_file.write("\n")

out_file.close()
