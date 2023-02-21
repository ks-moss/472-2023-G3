import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

colors = ['blue','green','red','cyan','magenta','yellow','purple','orange','black','pink','brown','olive','lightgreen','skyblue','gold']

# Read data from txt file
x = []
y = []
col = []
authors = []
with open('authorFileTouches.txt', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        filename, author, weeks = row
        #convert weeks to float, then int
        weeks = int(float(weeks[1:]))
        
        x.append(filename)
        y.append(weeks)
        if author not in authors:
            authors.append(author)
        #base color on author 
        col.append(colors[authors.index(author)])
#plot onto scatter graph
plt.scatter(x, y, c=col)
#remove all of the labels for files
frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
plt.xlabel("File")
plt.ylabel("Weeks")
plt.show()
