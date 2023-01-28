import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv
import datetime


files = []
authors = []
datesString = []
with open('data/commits_rootbeer.csv') as file:
    csvFile = csv.DictReader(file)
    for row in csvFile:
        files.append(row['Filename'])
        authors.append(row['Author'])
        datesString.append(row['Date'])


# reformat the dates
dates = []
init_date = datetime.date(datetime.MAXYEAR, 12, 31)
for d in datesString:
    d_ = d[:10].split('-')
    d_ = [int(i) for i in d_]
    date = datetime.date(d_[0], d_[1], d_[2])
    if (date < init_date):
        init_date = date
    dates.append(date)

# convert dates to weeks starting from beginning commit
weeks = []
for d in dates:
    datedelta = d - init_date
    weeks.append(datedelta.days / 7)


# get a unique list of authors
authorsUnique = []
for a in authors:
    if a not in authorsUnique:
        authorsUnique.append(a)

# create cmap array of floats for each author
cmap = matplotlib.cm.get_cmap('tab20')
colorsList = []
norm = colors.Normalize(0, len(authorsUnique) - 1)
for a in authors:
    val = norm(authorsUnique.index(a))
    colorsList.append(cmap(val))

colorsUnique = []
for c in colorsList:
    if c not in colorsUnique:
        colorsUnique.append(c)


# get a unique list of files
filesUnique = []
for f in files:
    if f not in filesUnique:
        filesUnique.append(f)

# convert files list to number
fileID = [filesUnique.index(f) + 1 for f in files]

# organize lists by author
touches = dict()
for f, w, c, a in zip(fileID, weeks, colorsList, authors):
    touches[a] = touches.get(a, {'files': [], 'week': [], 'color': c})
    touches[a]['files'].append(f)
    touches[a]['week'].append(w)


# display scatter plot
fig, ax = plt.subplots()
for a in authorsUnique:
    ax.scatter(touches[a]['files'], touches[a]['week'], c=touches[a]['color'], label=a)
ax.legend(loc='upper left', title='Authors', bbox_to_anchor=(1, 1))
ax.grid(True)
plt.show()