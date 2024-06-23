import os
import re
import sys
import tarfile

current_script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Directory containing compressed TAQ tick record
parent_directory = '/Users/chenjiaying/Desktop/TAQ_data' #replace by ur name

types_of_data = ['trades', 'quotes']

def extract_data(parent_directory, types_of_data):
    for type in types_of_data:
        # Directory to extract the contents of the .tar.gz files
        extract_directory = os.path.join('data', type)

        # Ensure the base extract directory exists
        if not os.path.exists(extract_directory):
            os.makedirs(extract_directory)

        # Iterate through all files in the directory
        for file_name in os.listdir(os.path.join(parent_directory, type)):
            # Check if the file ends with .tar.gz
            if file_name.endswith('.tar.gz'):
                # Extract the date from the file name
                date = file_name.split('.')[0]
                # Check if the file name matches the format YYYYMMDD.tar.gz
                if len(date) == 8 and date.isdigit():
                    # Construct the full path to the file
                    file_path = os.path.join(parent_directory, type, file_name)

                    # Extract the contents of the .tar.gz file
                    extract_tmp = os.path.join(extract_directory, file_name[:8])
                    if not os.path.exists(extract_tmp):
                        # If it doesn't exist, extract the contents of the .tar.gz file
                        with tarfile.open(file_path, 'r:gz') as tar:
                            tar.extractall(path=extract_directory)
                            print(f"Extracted {file_name} to {extract_directory}")
                    else:
                        print(f"Directory for {file_name} already exists, skipping extraction.")

    print("finish extracting data")

if __name__ == "__main__":
    extract_data(parent_directory, types_of_data)