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
root_directory = "/Volumes/Video/DuplicateTest"
#root_directory = "/Volumes/Video/Google Takeout"
#root_directory = "/Volumes/Video"
exclude_files = ['.DS_Store', 'some_file.txt']  # Add any file names you want to exclude
exclude_extensions = ['.json','.zip', '.theatre', 'imovielibrary', 'ini', 'db']  # Add any file extensions you want to exclude

# Specify the output file
hash_csv = 'output/combined_duplicate_file_hashes.csv'

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

def confirm_duplicates(duplicate_dict: dict):
    duplicate_list = []
    overall_dict = {}
    total_count = len(duplicate_dict)
    progress_increment = total_count // 100  # 10% increments
    current_count = 0


    start_function_time = time.time()

    for key in duplicate_dict.keys():
        hash_list = []

        if key not in overall_dict:
            overall_dict[key] = []

        for file_path in duplicate_dict[key]:
            hash = hash_file(file_path)
            hash_list.append(hash)
  
        while len(hash_list) > 0:
            if hash_list.count(hash_list[0]) > 1:
                path_dict = {'location': duplicate_dict[key][0],'hash':hash_list[0], 'Status': 'Duplicate'}
                logger.debug("File is a duplicate: %s", duplicate_dict[key][0])
                overall_dict[key].append(path_dict)
                duplicate_list.append(duplicate_dict[key].pop(0))
            else:
                path_dict = {'location': duplicate_dict[key][0],'hash':hash_list[0], 'Status': 'Unique'}
                logger.debug("File is unique: %s", duplicate_dict[key][0])
                overall_dict[key].append(path_dict)
                duplicate_dict[key].pop(0)
            hash_list.pop(0)
        
                # Update the progress
        current_count += 1
        try: 
            if (current_count % progress_increment == 0) or (current_count / total_count == 1):
                percentage_completion = (current_count / total_count) * 100
                print(f"Progress: {percentage_completion:.0f}%")
        except ZeroDivisionError:
            logger.error("Too few files for progress updates. ZeroDivisionError")
            pass

    end_function_time = time.time()
    elapsed_function_time = end_function_time - start_function_time

    return duplicate_list, overall_dict, elapsed_function_time

def hash_file(file_path):
    """
    Hashes a file.
    """
    file_hash = hashlib.sha256()

    # Lambda GPT evil
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            file_hash.update(byte_block)

    return file_hash.hexdigest()


def write_dict_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Status', 'Hash', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()

        # Iterate through the dictionary and write each row
        for filename, file_data in data.items():
            for file_info in file_data:
                writer.writerow({
                    'Filename': filename,
                    'Status': file_info['Status'],
                    'Hash': file_info['hash'],
                    'Location': file_info['location']
                })


if __name__ == "__main__":
    # Configure pycallgraph
    graphviz = GraphvizOutput()
    graphviz.output_file = 'output/combine_function_call_graph.png'
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

        end_function_time = time.time()
        elapsed_function_time = end_function_time - start_time
        formatted_seconds = "{:.2f}".format(elapsed_function_time)
        print(f"Elapsed Time scan and identify duplicates: {formatted_seconds} seconds")
        

        final_output, overall_dict, time_spent = confirm_duplicates(duplicate_files)
        formatted_seconds = "{:.2f}".format(time_spent)
        print(f"Hashing files and identify duplicates Elapsed Time: {formatted_seconds} seconds")

        write_dict_to_csv(overall_dict, hash_csv)

        # Record end time
        end_time = time.time()
def write_dict_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Status', 'Hash', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()

        # Iterate through the dictionary and write each row
        for filename, file_data in data.items():
            for file_info in file_data:
                writer.writerow({
                    'Filename': filename,
                    'Status': file_info['Status'],
                    'Hash': file_info['hash'],
                    'Location': file_info['location']
                })
        # Calculate elapsed time
        elapsed_time = end_time - start_time
        formatted_seconds = "{:.2f}".format(elapsed_time)
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = int (elapsed_time % 60)

        formatted_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
        print(formatted_time)

        # Print the elapsed time
        print(f"Elapsed Time: {formatted_seconds} seconds")
        print(f"Elapsed Time: {formatted_time}")

        logger.info("***************************")
        logger.info("Ethan's Duplicate File Finder, completed on: %s", current_date)
        logger.info("Elapsed Time: %s seconds", elapsed_time)
        logger.info("Elapsed Time: %s", formatted_time)
        logger.info("***************************")

