import zipfile
import os

def extract_zip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            member_path = os.path.join(extract_path, member)

            # Check if the file already exists
            if not os.path.exists(member_path):
                # File doesn't exist, extract it
                zip_ref.extract(member, extract_path)
                print(f"Extracted: {member}")
            else:
                # File already exists, handle it according to your needs
                print(f"Skipped (File already exists): {member}")

# Example usage
zip_path = './input/archive2.zip'
extract_path = './output'

extract_zip(zip_path, extract_path)
