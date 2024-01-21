#This is just a start, no testing

import os
import pprint
import shutil

def move_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file != '.DS_Store':
                source_path = os.path.join(root, file)
                
                # Extract the relative path within the source_folder
                relative_path = os.path.relpath(source_path, source_folder)
                new_relative_path = relative_path.split('/', 1)[1]

                # Create the destination path
                destination_path = os.path.join(destination_folder, new_relative_path)
                
                # Check if the destination folder exists, create it if not
                destination_dir = os.path.dirname(destination_path)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                
                # Check if the file already exists at the destination
                if os.path.exists(destination_path):
                    print(f"File already exists at destination: {destination_path}")
                else:
                    try:
                        # Move the file to the destination
                        shutil.move(source_path, destination_path)
                        print(f"From: {source_path}")
                        print(f"To: {destination_path}")
                    except shutil.Error as e:
                        print(f"Error: {e}")

# Example usage:
source_folder = "googleTest"
destination_folder = "googleTest/Takeout"



move_files(source_folder, destination_folder)
