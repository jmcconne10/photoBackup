# Image/Video Management

photoBackup

This is used to identify duplicates based on checking file names and then comparing hashes.
Duplicates are moved to a folder

### Easy adjustments

root_directory is the folder we're looking through
duplicates_path is where the duplicates will go (they keep their folder structure)
exclude_files has files that should be excluded
exclude_extensions is for extensions that should be excluded
log_Level can be changed to info or debug

### Output goes to the relative path
output/combined_duplicate_file_hashes.csv

