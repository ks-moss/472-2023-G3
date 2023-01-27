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
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    unique_authCount = 0 
    dict_authors = dict()
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

                cmtAuth = shaDetails['commit']
          #      authObj = cmtAuth.get('author')
                authObj = cmtAuth['author']
                authDate = authObj['date']
                authName = authObj['name']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    name_split = os.path.splitext(filename)
                    file_ext = name_split[1]
                    if file_ext == ".java":
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        unique_authCount += 1
                        if dict_authors.get(authName) is not None:
                            auth_val = dict_authors[authName]
                            dict_authors[authName] = auth_val + 1
                        else:
                            dict_authors[authName] = 1

                        print(filename)
                        newRow = [str(filename), str(authName), str(authDate)]
                        with open("myCSV.csv", "a") as filestream:
                            writer = csv.writer(filestream)
                            writer.writerow(newRow)
                            filestream.close()

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    print(dict_authors)
    print("Total number of authors who touched unique files = " + str(len(dict_authors)))
    

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

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'myCSV.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)
fileCSV.close()

countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))