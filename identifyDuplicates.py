# Specify the root folder
#root_folder = '/Volumes/Video/takeOutoutput'
import hashlib
import os
import csv
from collections import defaultdict
import os

def get_all_files(root_folder):
    return [os.path.join(foldername, filename) for foldername, _, filenames in os.walk(root_folder) for filename in filenames]

def identify_duplicate_files(file_list):
    file_locations = defaultdict(list)
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        file_locations[file_name].append(file_path)
    duplicate_files = {name: locations for name, locations in file_locations.items() if len(locations) > 1}
    return duplicate_files

def write_to_csv(duplicate_files, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Locations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file_name, locations in duplicate_files.items():
            writer.writerow({'File Name': file_name, 'Locations': ', '.join(locations)})

def hash_duplicates(duplicate_files):

    hashed_files = {}
            
    for key, value_list in duplicate_files.items():
        print(f"Items for key '{key}':")
    
    # Iterate through each item in the list
        for item in value_list:
            # Hash the file
            hash_value = hash_file(item)
            print(f"Hash value for {item}: {hash_value}")


            # Add the hash value to the dictionary
            if key in hashed_files:
                hashed_files[key].append(item)
                hashed_files[key].append(hash_value)
            else:
                hashed_files[key] = [item]
                hashed_files[key].append(hash_value)
    return hashed_files

            

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Specify the root folder
root_folder = 'test'
output_csv = 'output/duplicate_files.csv'

# Get a list of all files in subfolders
all_files_list = get_all_files(root_folder)

# Identify duplicate file names and their locations
duplicate_files = identify_duplicate_files(all_files_list)

# Write the output to a CSV file
write_to_csv(duplicate_files, output_csv)
print(f"Duplicate file information written to {output_csv}.")

print(hash_duplicates(duplicate_files))