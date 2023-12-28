import hashlib
import os
import time

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Record start time
start_time = time.time()

file = '/Volumes/Video/Go Pro Working/Christmas Choir 2016/MVI_4721.MOV'
print(hash_file(file))

# Record end time
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed Time: {elapsed_time} seconds")