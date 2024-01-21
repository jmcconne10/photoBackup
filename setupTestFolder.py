import shutil
import os

def delete_and_copy(source_folder, destination_folder):
    try:
        # Delete the existing googleTest folder
        shutil.rmtree(destination_folder)
        print(f"Deleted: {destination_folder}")

    except shutil.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Copy the contents of googleTestBackup to googleTest
        shutil.copytree(source_folder, destination_folder)
        print(f"Copied: {source_folder} to {destination_folder}")

    except shutil.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage:
source_folder = "googleTestBackup"
destination_folder = "googleTest"

delete_and_copy(source_folder, destination_folder)
