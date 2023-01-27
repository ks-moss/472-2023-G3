import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from Levenshtein import distance

fileNames = []
fileAuthors = []
fileTimes = []

source = open("plotdata.txt", "r")
contents = source.read()
source.close()

target = "fileNames"
fileName = ""
fileAuthor = ""
fileTime = ""

for c in contents:
    if c != ',' and c != '\n':
        if target == "fileNames":
            fileName = fileName + c
        if target == "fileAuthors":
            fileAuthor = fileAuthor + c
        if target == "fileTimes":
            fileTime = fileTime + c
    else:
        if target == "fileNames":
            fileNames.append(fileName)
            fileName = ""
            target = "fileAuthors"
        elif target == "fileAuthors":
            fileAuthors.append(fileAuthor)
            fileAuthor = ""
            target = "fileTimes"
        elif target == "fileTimes":
            fileTimes.append(fileTime)
            fileTime = ""
            target = "fileNames"
#fileTimes.append(fileTime)

#convert time string to date object
for i in range(0, len(fileTimes)):
    year = fileTimes[i][:4]
    fileTimes[i] = fileTimes[i][5:]
    month = fileTimes[i][:2]
    fileTimes[i] = fileTimes[i][3:]
    day = fileTimes[i][:2]
    fileTimes[i] = int(date(int(year), int(month), int(day)).toordinal() / 7)

minTime = fileTimes[0]
for i in range(0, len(fileTimes)):
    if (fileTimes[i] < minTime):
        minTime = fileTimes[i]

for i in range(0, len(fileTimes)):
    fileTimes[i] = fileTimes[i] - minTime + 1

#convert fileAuthors to levenshtein values
base = fileAuthors[0]
for i in range(0, len(fileAuthors)):
    fileAuthors[i] = int(distance(base, fileAuthors[i]))
max = fileAuthors[0]
for i in range(0, len(fileAuthors)):
    if max < fileAuthors[i]:
        max = fileAuthors[i]
for i in range(0, len(fileAuthors)):
    fileAuthors[i] = fileAuthors[i] / max

#convert fileNames to levenshtein values
base = fileNames[0]
for i in range(0, len(fileNames)):
    fileNames[i] = int(distance(base, fileNames[i]))


print(len(fileNames))
print(len(fileAuthors))
print(len(fileTimes))

plt.scatter(fileNames, fileTimes, c=fileAuthors)
plt.gray()
plt.show()