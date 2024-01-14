## TO DO:
# Add a method to get the file size, so I can ignore smaller files
# In this one, I want to have the folder names in the csv file
# Need to remove files that include iMovie

from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from pycallgraph2 import GlobbingFilter
from pycallgraph2 import Config

import hashlib
import os
import csv
from collections import defaultdict
import os
import time
import datetime
import logging
import pprint

config = Config()
## Setting filter for Call Graph
config.trace_filter = GlobbingFilter(exclude=[
    'logging.*',
    'pycallgraph2.*',
])

## Attributes that are changed regularly
# Identifies root folder and gets a list of all files
log_Level = "INFO" # DEBUG is everything, INFO is less
#root_directory = '/Users/Joe/OneDrive/Code/photoBackup/googleTest'
#root_directory = "/Volumes/Video/Google Takeout"
root_directory = "/Volumes/Video/DuplicateTest"
#root_directory = "/Volumes/Video"
exclude_files = ['.DS_Store', 'some_file.txt']  # Add any file names you want to exclude
exclude_extensions = ['.json','.zip', '.theatre', 'imovielibrary', 'ini', 'db']  # Add any file extensions you want to exclude

# Specify the output file
hash_csv = 'output/duplicate_file_hashes.csv'

def get_all_files(root_folder, exclude_names=None, exclude_extensions=None):
    exclude_names = exclude_names or []
    exclude_extensions = exclude_extensions or []
    
    return [
        os.path.join(foldername, filename)
        for foldername, _, filenames in os.walk(root_folder)
        for filename in filenames
        if filename not in exclude_names and not filename.endswith(tuple(exclude_extensions))
    ]

def identify_duplicate_files(file_list):
    file_locations = defaultdict(list)
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        file_locations[file_name].append(file_path)
    duplicate_files = {name: locations for name, locations in file_locations.items() if len(locations) > 1}
    return duplicate_files

def hash_duplicates(duplicate_files):

    total_count = len(duplicate_files)
    progress_increment = total_count // 100  # 10% increments
    current_count = 0
    hashed_files = {}
            
    for key, value_list in duplicate_files.items():
    
    # Iterate through each item in the list
        for item in value_list:
            # Hash the file
            hash_value = hash_file(item)
            dictionary_item = {'location': item, 'hash': hash_value}
            # Add the hash value to the dictionary
            if key in hashed_files:
                hashed_files[key].append(dictionary_item)
            else:
                hashed_files[key] = [dictionary_item]

        # Update the progress
        current_count += 1
        if (current_count % progress_increment == 0) or (current_count / total_count == 1):
            percentage_completion = (current_count / total_count) * 100
            print(f"Progress: {percentage_completion:.0f}%")
    return hashed_files

def hash_file(file_path):

    try:
        with open(file_path, 'rb') as f:
            # Try to create a hash object
            try:
                hash_object = hashlib.md5(f.read()).hexdigest()
                logger.debug("File hashed successfully: %s", file_path)
            except ValueError:
                hash_object = None
                logger.error("There was an error hashing the file: %s", file_path)
    except FileNotFoundError:
        hash_object = None
        logger.error("File not found: %s", file_path)
    except Exception as e:
        hash_object = None
        logger.error("An unexpected error occurred: %s", str(e))
    

    return hash_object
    
def check_duplicate_hash(hashed_files):

    duplicateCount = 0
    mismatchCount = 0
    deletedFiles = 0

    for filename, records in hashed_files.items():
        # Iterate through the list of records for each file
        for i in range(len(records) - 1):

            file1 = records[i]
            file2 = records[i + 1]
            hash1 = file1['hash']
            hash2 = file2['hash']
            
            # Compare hash values
            if hash1 == hash2:
                logger.debug(f"Hash values match for locations {file1['location']} and {file2['location']}")
                file1['Duplicate'] = True
                file2['Duplicate'] = True
                duplicateCount += 1             
               
                # Check which file is in the main folder and delete the other
                if file1['location'].startswith('/Volumes/Video/Google Takeout/Takeout/'):
                    file1['Plan'] = 'Keep'
                    file2['Plan'] = 'Delete'
                    # Delete the file in location not main Takeout
                    os.remove(file2['location'])
                    logger.info("File deleted: %s", file2['location'])
                    deletedFiles += 1
                elif file2['location'].startswith('/Volumes/Video/Google Takeout/Takeout/'):
                    file1['Plan'] = 'Delete'
                    file2['Plan'] = 'Keep'
                    # Delete the file in location not main Takeout
                    os.remove(file1['location'])
                    logger.info("File deleted: %s", file1['location'])
                    deletedFiles += 1
                else:
                    # if plan attribute doesn't exist, mark it as left alone, it will be updated later if it is deleted

                    if 'Plan' not in file1:
                        file1['Plan'] = 'Left Alone'            
                    if 'Plan' not in file2:
                        file2['Plan'] = 'Left Alone' 

            else:
                logger.debug(f"Hash values do not match for locations {file1['location']} and {file2['location']}")
                file1['Duplicate'] = False
                file2['Duplicate'] = False
                mismatchCount += 1
    
    return duplicateCount, mismatchCount, deletedFiles

def get_file_size(hashed_files):
    for filename, entries in hashed_files.items():
        for entry in entries:
            if (entry['Duplicate'] == True):
                try:
                    bytes = os.path.getsize(entry['location'])
                    # Convert bytes to megabytes and format to 2 decimal places
                    mb = round(bytes / (1024 * 1024), 2)
                    entry['size'] = mb
                except FileNotFoundError:
                    entry['size'] = 'File not found'

def write_duplicate_files(data, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['filename', 'location', 'hash', 'Duplicate', 'size', 'Plan']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for filename, entries in data.items():
            for entry in entries:
                if (entry['Duplicate'] == True):
                    writer.writerow({'filename': filename, 'location': entry['location'], 'hash': entry['hash'], 'Duplicate': entry['Duplicate'], 'size': entry['size'], 'Plan': entry['Plan']})

if __name__ == "__main__":
    # Configure pycallgraph
    graphviz = GraphvizOutput()
    graphviz.output_file = 'output/function_call_graph.png'
    with PyCallGraph(output=graphviz, config=config):

        # Get the current date and time
        current_date = datetime.datetime.now()

        # Format the date as a string (e.g., '2023-03-15')
        formatted_date = current_date.strftime('%Y-%m-%d')

        # Specify a file for logging that includes current date
        logFile=(f'output/log_{formatted_date}.log')

        # Configure the logging system
        logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s')

        # Create a logger and sets 
        logger = logging.getLogger('my_logger')
        logger.setLevel(log_Level)

        # Record start time
        start_time = time.time()

        # Start the logging
        logger.info("**************************************************************")
        logger.info("Duplicate Identification Started")
        logger.info("Root Directory: %s", root_directory)
        logger.info("Exclude Files: %s", exclude_files)
        logger.info("Exclude Extensions: %s", exclude_extensions)
        logger.info("**************************************************************")

        # Get a list of all files in the root directory
        all_files_list = get_all_files(root_directory, exclude_files, exclude_extensions)

        logger.info("Total Number of Files Found: %s", len(all_files_list))

        # Identify duplicate file names and their locations
        duplicate_files = identify_duplicate_files(all_files_list)

        logger.info("Number of Duplicate File Names Found: %s", len(duplicate_files))

        # Hashes the files, stores the results in a dictionary, and keeps track of % completed
        hashed_files = hash_duplicates(duplicate_files)
        duplicateCount, mismatchCount, deletedFiles = check_duplicate_hash(hashed_files)

        # Get the size of the files
        get_file_size(hashed_files)

        #pprint.pprint(hashed_files)

        # Write the output showing which duplicate file names have the same has
        write_duplicate_files(hashed_files, hash_csv)

        # Record end time
        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = (elapsed_time % 60)

        formatted_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
        print(formatted_time)

        # Print the elapsed time
        print(f"Elapsed Time: {elapsed_time} seconds")
        print(f"Elapsed Time: {formatted_time}")

        #use logger to track how many duplicates were found and how long it took
        logger.info("**************************************************************")
        logger.info("Duplicate Identification Completed")
        logger.info("Total Number of Files Found: %s", len(all_files_list))
        logger.info("Number of Duplicate File Names Found: %s", len(duplicate_files))
        logger.info("Number of Duplicate Hash Values Found: %s", duplicateCount)
        logger.info("Number of Deleted Files: %s", deletedFiles)
        logger.info("Number of Mismatched Hash Values Found: %s", mismatchCount)
        logger.info("Elapsed Time: %s seconds", elapsed_time)
        logger.info("Elapsed Time: %s seconds", formatted_time)
        logger.info("**************************************************************")