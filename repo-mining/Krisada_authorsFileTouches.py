import subprocess
from datetime import datetime
import os

file_path = "/Users/krisadasinamkam/Desktop/CS 472/472-2023/repo_mining/data/file_rootbeer.csv"

lstTokens = ["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",
                "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",
                "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"]

file_contents = []
newlist = []

# Open the file using the path
try:
    # Get the absolute path of the file_rootbeer.csv
    file_path = os.path.abspath(file_path)
    # Get the directory that the file is in
    file_dir = os.path.dirname(file_path)
    # Change the current working directory to the directory that the file is in
    os.chdir(file_dir)
    with open(file_path, 'r') as file:
        # Read the contents of the file
        file_contents = file.readlines()
        file.close()
except FileNotFoundError:
    print(f"{file_path} not found.")
except:
    print("An error occurred.")



if __name__ == '__main__':
    for x in range (1, len(file_contents), 1):
        word = file_contents[x].replace("\n", "").split(",")
        newlist.append(word[0])
        print(word[0])

   
