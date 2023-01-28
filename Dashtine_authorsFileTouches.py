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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo


def grabAuthorDates(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    rows = ["Filename", "Author", "Date"]
    fileCSV = open('authorData.csv', 'w')
    writer = csv.writer(fileCSV)
    writer.writerow(rows)
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                auth = shaObject['commit']['author']['name']
                touchDate = shaObject['commit']['author']['date']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    print(filename)
                    name_split = os.path.splitext(filename)
                    file_ext = name_split[1]
                    if file_ext == '.java':
                        rows = [filename, auth, touchDate]
                        writer.writerow(rows)
                        
                    
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    fileCSV.close()

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

dictfiles = dict()
fileName = {}
with open('file_rootbeer.csv', 'r') as dataFile:
    for line in csv.DictReader(dataFile):
       filename = line['Filename']
       name_split = os.path.splitext(filename)
       file_ext = name_split[1]
       if file_ext == '.java':
            dictfiles[filename] = {}
dataFile.close()
grabAuthorDates(dictfiles, lstTokens, repo)

