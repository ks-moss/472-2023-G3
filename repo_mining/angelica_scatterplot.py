import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import OrderedDict

filename="data/fileAuthors_rootbeer.csv"

plt.style.use('_mpl-gallery')
index = 0
fileDict = dict()
authDict = {}

with open(filename,'r') as data:
    for line in csv.DictReader(data):
            # Check if file has been keyed in dictionary
            # If it exists, append to appropriate file key
            if line["Filename"] in fileDict.values():
                key = list(fileDict.values())
                keyPos = key.index(line["Filename"])
                authDict[keyPos].extend([line["Author Name"], line["Date"]])
            # Otherwise assign it a key
            else:
                fileDict[index] = line["Filename"]
                authDict.update({index: [line["Author Name"], line["Date"]]})
                index += 1


for key, value in authDict.items():
   print(key)
   x = key
   valueList = authDict[key]
   print(valueList)
   temp = 0
   for plotThis in valueList:
        ##print(plotThis)
        temp+=1
        #print(temp)
        if (temp % 2) == 0:
            #print("temp is even")
            y = plotThis
        else:
            #print("temp is odd")
            '''''
            match plotThis:
                case "Matthew Rollings":
                    colors = np.random.uniform(15, 80, len(x))
                case "Scott Alexander-Bown":
                    colors = np.random.uniform(15, 80, len(x))
                case "Slim Namouchi":
                    colors = np.random.uniform(15, 80, len(x))
                case "Fi5t":
                    colors = np.random.uniform(15, 80, len(x))
                case "mat":
                    colors = np.random.uniform(15, 80, len(x))
                case "Daniel Kutik":
                    colors = np.random.uniform(15, 80, len(x))
                case "Ivan Vlasov":
                    colors = np.random.uniform(15, 80, len(x))
                case "altvnv":
                    colors = np.random.uniform(15, 80, len(x))
                case "matthew":
                    colors = np.random.uniform(15, 80, len(x))
                case "Frieder Bluemle":
                    colors = np.random.uniform(15, 80, len(x))
                case "Ali Waseem":
                    colors = np.random.uniform(15, 80, len(x))
                case "LeonKarabchevsky":
                    colors = np.random.uniform(15, 80, len(x))
                case "vyas":
                    colors = np.random.uniform(15, 80, len(x))
                case "leocadiotine": 
                    colors = np.random.uniform(15, 80, len(x))
                case "Andy Barber":
                    colors = np.random.uniform(15, 80, len(x))
                case "Mohammed Ezzat":
                    colors = np.random.uniform(15, 80, len(x))
                '''
    # plot
    #fig, ax = plt.subplots()

    #ax.scatter(x, y, s=100, vmin=0, vmax=100)

    
# size and color:
            
#colors = np.random.uniform(15, 80, len(x))

for key, value in fileDict.items():
    print(key, ":", value)



#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#   ylim=(0, 8), yticks=np.arange(1, 8))
plt.show()