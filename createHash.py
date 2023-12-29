import hashlib
import os
import time
import logging

# Configure the logging system
logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger('my_logger')

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        
        # Try to create a hash object
        try:
            hash_object = hashlib.md5(f.read()).hexdigest()
            logger.debug("File hashed successfully: %s", file_path)
        except ValueError:
            hash_object = None
            logger.error("There was an error hashing the file: %s", file_path)

    return hash_object

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