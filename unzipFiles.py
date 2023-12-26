## This will take zip files and extract them to a folder,
## while ensuring no duplciates file names are overwritten.

## To use: update the inputDirectory string
## Once completed, the output will be in the parent folder set for extract_path

#get a list of files in a folder
import os
import zipfile

# Create a list for duplicates
duplicates = []

#set the directory you want to unzip files from
inputDirectory = "/Volumes/Video/Google Takeout2023"
os.chdir(inputDirectory)

#set the directory you want to unzip files to
current_path = os.getcwd()
extract_path = os.path.dirname(current_path) + "/takeOutoutput"
os.makedirs(extract_path, exist_ok=True)
duplicates_path = extract_path + "/duplicates"
os.makedirs(duplicates_path, exist_ok=True)

for file in os.listdir():
    if file.endswith(".zip"):
        zip_path = file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                member_path = os.path.join(extract_path, member)
                if not os.path.exists(member_path):
                    # File doesn't exist, extract it
                    zip_ref.extract(member, extract_path)
                    #print(f"Extracted: {member}")
                else:
                    # Add the file to the list of duplicates
                    duplicates.append(member)
                    zip_ref.extract(member, duplicates_path) 
        #os.remove(file)
        print("Zip File: " + os.path.basename(file))

for duplicate in duplicates:
    print("Found this duplciate: " + duplicate)

    