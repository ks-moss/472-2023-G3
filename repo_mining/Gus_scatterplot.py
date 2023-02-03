import json
import requests

from matplotlib import pyplot
from datetime import datetime

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
    firstdate = datetime.now()
    ipage = 1  # url page counter
    ct = 0  # token counter
    cnt = 0 # filename counter

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
                dateObj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                if dateObj < firstdate:
                    firstdate = dateObj
                lstfilestouched = []
                for filenameObj in filesjson:
                    if (filenameObj['filename'].endswith('.java')):
                        filename = filenameObj['filename']
                        if dictfiles.get(filename, -1) == -1:
                            dictfiles[filename] = cnt
                            cnt += 1
                        lstfilestouched.append(filename)
                for touchedfile in lstfilestouched:
                    lsttouches.append(touch(name, dateObj, touchedfile))
                    # print('Author\'s name: ' + name + ' Date touched: ' + date + ' File: ' + filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return firstdate

def plotpoints(lsttouches, firstdate, dictfiles):
    X = []
    Y = []
    color = []
    dictauthors = dict()
    authorcnt = 0
    for touch in lsttouches:
        if dictauthors.get(touch.author, -1) == -1:
            dictauthors[touch.author] = authorcnt
            authorcnt += 1
            X.append([])
            Y.append([])
            color.append([])

    for touch in lsttouches:
        author = dictauthors[touch.author]
        date = touch.date - firstdate
        weeks = date.days / 7
        file = dictfiles[touch.file]
        X[author].append(file)
        Y[author].append(weeks)
        color[author].append(author+1)

    for key in dictauthors:
        pyplot.scatter(X[dictauthors[key]], Y[dictauthors[key]], color[dictauthors[key]])

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
firstdate = counttouches(dictfiles, lstTokens, repo, lsttouches)

plotpoints(lsttouches, firstdate, dictfiles)
pyplot.xlabel('File')
pyplot.ylabel('Time (Weeks)')

pyplot.savefig('ScatterPlot.png', bbox_inches='tight')
pyplot.show()