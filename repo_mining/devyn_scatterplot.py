from devyngilliam_authorsFileTouches import dictfiles, requests
from datetime import datetime
import matplotlib.pyplot as plt
import random

# Dictinoary array to store commit information
scatterplot_array = []

# Used to increment the x value when reviewing a new file
x = 0

# Replace with your repository name
repo_name = 'scottyab/rootbeer'

# For loop to iterate throughout the source files (.java)
for file_path in list(dictfiles):

    # Get the commit history for the file
    url = f"https://api.github.com/repos/{repo_name}/commits?path={file_path}"
    response = requests.get(url)

    # Extract the authors & dates from the commit history
    for commit in response.json():
        author = commit["commit"]["author"]["name"]
        date = commit["commit"]["author"]["date"]

        # Convert the given dates to how many weeks ago it was
        # Convert the string to a datetime object
        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

        # Convert input strings to datetime object
        date = datetime.strptime(str(date_object.year) + str(date_object.month) + str(date_object.day), "%Y%m%d")

        # Get current date
        now = datetime.now()

        # Calculate difference between current date and given date
        difference = now - date

        # Convert difference to weeks
        weeks_ago = difference.days / 7

        # Set the seed for the author color based upon their name
        random.seed(author)

        # Generate a random number
        random_num = random.randint(1, 255)

        # Create a dictionary based upon the commit info
        scatter_plot = {"Color": random_num, "Weeks_Ago": weeks_ago, "X_Value": x}

        # Append the current dictionary to the dictionary array
        scatterplot_array.append(scatter_plot)

    # Increment the variable & grab the next file if available
    x += 1

# Extract x and y coordinates from the list, also extract the author colors
x = [d['X_Value'] for d in scatterplot_array]
y = [d['Weeks_Ago'] for d in scatterplot_array]
color = [d['Color'] for d in scatterplot_array]

# Create the scatter plot
plt.scatter(x, y, c = color)

# Add labels and title
plt.xlabel('Files')
plt.ylabel('Weeks')

# Show the plot
plt.show()