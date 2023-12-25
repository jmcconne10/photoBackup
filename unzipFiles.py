## TODO
# Figure out what happens when files share the same name. 

#get a list of files in a folder
import os
import zipfile

#set the directory you want to unzip files from
#os.chdir("/Volumes/Video/Google Takeout2023")

#set the directory to current
os.chdir("./input")


for file in os.listdir():
    if file.endswith(".zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()
        #os.remove(file)
        print(os.path.basename(file))

    