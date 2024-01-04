#This is just a start, no testing

import os
import pprint
# Set the root directory
root_dir = "/Users/Joe/OneDrive/Code/photoBackup/googleTest"
consolidated_dir = "/Users/Joe/OneDrive/Code/photoBackup/googleTest/Takeout/"

# Set the output directory
output_dir = "output"

# Find all files in subfolders, except those that start with  consolidated
files = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f)) and not f.startswith(consolidated_dir)]

pprint.pprint(files)
