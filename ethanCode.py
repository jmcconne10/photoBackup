## To Do
## Add logging capability to the remaining functions
## Ensure is_accessbile does what it needs to
## Review the exclude_extensions capability
## Add in the method to track % complete


import hashlib
import os
import csv
from collections import defaultdict
import os
import time
import datetime
import logging
import pprint

## Attributes that are changed regularly
# Identifies root folder and gets a list of all files
log_Level = "DEBUG" # DEBUG is everything, INFO is less
root_directory = '/Users/Joe/OneDrive/Code/photoBackup/googleTest'
#root_directory = "/Volumes/Video/Google Takeout"
#root_directory = "/Volumes/Video"
exclude_files = ['.DS_Store', 'some_file.txt']  # Add any file names you want to exclude
exclude_extensions = []  # Add any file extensions you want to exclude

# Specify the output file
hash_csv = 'output/ethan_output.csv'

EXCLUDED_FILE_TYPES = ("DS_Store", "localized", "zip", "json","zip", "theatre", "imovielibrary", "ini", "db", ".DS_Store")


def is_accessible(folder_path: str) -> bool:
    """
    Checks if a folder exists and is readable.
    """

    try:
        os.access(folder_path, os.R_OK)
    except (FileExistsError, PermissionError):
        logger.error("There was an error accessing the folder: %s", folder_path)
        return False
    return True


def get_file_extension(file_name):
    """
    Returns the extension of a file.
    Doesn't work on files that are missing the extension in the name.
    """

    extension = ""

    for iterator in range(1, len(file_name)):
        if file_name[-iterator] == ".":
            break
        else:
            extension = file_name[-iterator] + extension
        
    return extension


def hash_folder_contents(folder_path: str) -> list:
    """
    Returns a list containing the hashed name of every non-excluded file in a folder.\n
    Returns 'None' if the folder wasn't accessible.
    """

    # Checks if the folder is even accessible.
    if not is_accessible(folder_path):
        return None

    # Creates a list of every file that's type isn't excluded.
    file_name_list = [
        file_name
        for file_name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, file_name)) == False
        and get_file_extension(file_name) not in EXCLUDED_FILE_TYPES
    ]

    try:
        # Returns a list of hashed file names.
        return [hash(file_name) for file_name in file_name_list]
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return None


def create_file_dictionary(hash_list: int, hash_folder_path_list: list) -> dict:
    """
    Returns a dictionary of file names and their locations.
    """

    file_dict = dict()

    for iterator in range(len(hash_list)):
        hash_file_name = None

        file_name_list = [
            file_name
            for file_name in os.listdir(hash_folder_path_list[iterator][0])
            if os.path.isdir(
                os.path.join(hash_folder_path_list[iterator][0], file_name)
            )
            == False
            and get_file_extension(file_name) not in EXCLUDED_FILE_TYPES
        ]

        for file_name in file_name_list:
            if hash(file_name) == hash_list[iterator]:
                hash_file_name = file_name
                break

        hash_file_paths = [
            os.path.join(folder_path, hash_file_name)
            for folder_path in hash_folder_path_list[iterator]
        ]

        file_dict[hash_file_name] = hash_file_paths

    return file_dict


def scan_folder(root_path: str) -> dict:
    """
    Recursively scans a folder for files with duplicate names.\n
    Returns a dictionary where the keys are file names\n
    And each name returns a list of file paths for files with that name.
    """

    if not is_accessible(root_path):
        raise ValueError(f"{root_path} could not be accessed.", end="\n\n")

    # Folder paths and a list of the hashes in that folder.
    folder_path_list = [dirpath for dirpath, dirnames, filenames in os.walk(root_path)]
    folder_hash_list = [
        hash_folder_contents(folder_path) for folder_path in folder_path_list
    ]

    # Removes any empty or unaccessible folders from the lists.
    index = 0
    while index < len(folder_path_list):
        if folder_hash_list[index] is None or len(folder_hash_list[index]) == 0:
            folder_path_list.pop(index)
            folder_hash_list.pop(index)
        else:
            index += 1

    # Hashes with multiple instances and their parent folder paths.
    duplicate_hash_list = []
    duplicate_hash_path_list = []

    """
    Gets every hash from a folder and compares it to the hashes of other folders.
    Stores the value and folder paths of hashes with multiple instances.
    """
    while len(folder_path_list) > 1:
        # Pops the first folder from the main path and hash list.
        temp_hash_list = folder_hash_list.pop(0)
        temp_folder_name = folder_path_list.pop(0)

        for hash in temp_hash_list:
            # Stores the folder paths of duplicate hashes.
            temp_duplicate_hash_path_list = []

            # Iterates through folders and logs duplicate positions.
            for index in range(len(folder_path_list)):
                if hash in folder_hash_list[index]:
                    temp_duplicate_hash_path_list.append(folder_path_list[index])
                    folder_hash_list[index].remove(hash)
                    continue

            # Stores duplicate info if needed.
            if len(temp_duplicate_hash_path_list) > 0:
                duplicate_hash_list.append(hash)
                temp_duplicate_hash_path_list.append(temp_folder_name)
                duplicate_hash_path_list.append(temp_duplicate_hash_path_list)

    return create_file_dictionary(duplicate_hash_list, duplicate_hash_path_list)


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


def confirm_duplicates(duplicate_dict: dict):
    duplicate_list = []
    overall_dict = {}
    total_count = len(duplicate_dict)
    progress_increment = total_count // 2  # 10% increments
    current_count = 0

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
        if (current_count % progress_increment == 0) or (current_count / total_count == 1):
            percentage_completion = (current_count / total_count) * 100
            print(f"Progress: {percentage_completion:.0f}%")

    return duplicate_list, overall_dict

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

    # Record start time
    start_time = time.time()
    
    ##############################
    ## Logging configuration
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

    ## Logging configuration
    ##############################
    
    logger.info("***************************")
    logger.info("Ethan's Duplicate File Finder, began on: %s", current_date)
    logger.info("These extensions are excluded: %s", EXCLUDED_FILE_TYPES)
    logger.info("***************************")

    os.system("clear")

    file_dict = scan_folder(root_directory)

    final_output, overall_dict = confirm_duplicates(file_dict)

    write_dict_to_csv(overall_dict, hash_csv)

    # Record end time
    end_time = time.time()

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

