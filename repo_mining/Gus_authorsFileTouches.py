import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

class touch:
    def __init__(self, author, date, file):
        self.author = author
        self.date = date
        self.file = file

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
def counttouches(dictfiles, lsttokens, repo, lsttouches):
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
                commitDetails = shaDetails['commit']
                authorDetails = commitDetails['author']
                name = authorDetails['name']
                date = authorDetails['date']
                lstfilestouched = []
                for filenameObj in filesjson:
                    if (filenameObj['filename'].endswith('.java') or filenameObj['filename'].endswith('.kt') 
                        or filenameObj['filename'].endswith('.c') or filenameObj['filename'].endswith('.cpp') 
                        or filenameObj['filename'].endswith('.cmake')): 
                        filename = filenameObj['filename']
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        lstfilestouched.append(filename)
                for touchedfile in lstfilestouched:
                    lsttouches.append(touch(name, date, touchedfile))
                    # print('Author\'s name: ' + name + ' Date touched: ' + date + ' File: ' + filename)
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
lstTokens = ["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"]

dictfiles = dict()
lsttouches = []
counttouches(dictfiles, lstTokens, repo, lsttouches)

print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '_touches.csv'
rows = ["Author", "Date", "Filename"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for touchObj in lsttouches:
    author = touchObj.author
    date = touchObj.date
    filename = touchObj.file
    rows = [author, date, filename]
    writer.writerow(rows)
fileCSV.close()