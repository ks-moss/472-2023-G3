import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


# @dictAuthors, empty dictionary of authors and dates
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
# @fileData, data from csv file of file names
def countfiles(dictAuthors, lsttokens, repo, fileNames):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                # Get the author and date of commit
                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename in fileNames:
                        dictAuthors.append({'file': filename, 'author': author, 'date': date})
                        print(filename, author, date)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

# collect data from file_rootbeer.csv
fileData = []
with open('data/file_rootbeer.csv') as file:
    csvFile = csv.DictReader(file)
    for row in csvFile:
        fileData.append(row['Filename'])

dictAuthors = []
countfiles(dictAuthors, lstTokens, repo, fileData)
print('Total number of commits: ' + str(len(dictAuthors)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/commits_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for x in dictAuthors:
    rows = [x['file'], x['author'], x['date']]
    writer.writerow(rows)
fileCSV.close()
