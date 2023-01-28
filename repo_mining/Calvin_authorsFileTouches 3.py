import json
import requests
import csv

import os

import numpy as np
import matplotlib.pyplot as plt

from array import *


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
    ct = 0  # token counter


    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'  #combines repo string with others
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
                commitjson = shaDetails['commit']  
                authorjson = commitjson['author']           
                print(authorjson['name'])
                print(authorjson['date'])               #prints name and date correctly

                for filenameObj in filesjson:    #NEED TO FILTER SOURCE FILES HERE
                    filename = filenameObj['filename'] #This creates string of filename - filenameObj does not contain author
                    nameLength = len(filename) #.java is five characters so find the final five of string and compare
                    ending = filename[nameLength - 5: nameLength] #slicing to find final five of file
                    desiredEnding = ".java"             #we want to check sliced string against this 'desired' string
                    if(ending == desiredEnding):       #if file ends in .java, add it
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        #print(filename)
                    
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
#lstTokens = ["fd02a694b606c4120b8ca7bbe7ce29229376ee",
                #"16ce529bdb32263fb90a392d38b5f53c7ecb6b",
                #"8cea5715051869e98044f38b60fe897b350d4a"]
                
#REMOVE BEFORE COMMITTING
#lstTokens = ["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"]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)


bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')



