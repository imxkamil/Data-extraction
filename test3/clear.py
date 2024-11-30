import os
import glob

def delete_files_in_temp(directory):
    # Create the full path with the wildcard to match all files in the directory
    files = glob.glob(os.path.join(directory, '*'))
    
    # Iterate through each file and delete it
    for file in files:
        try:
            os.remove(file)
            # print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print("Temp folder cleared")

# Path to the directory where files should be deleted
temp_directory = r'C:\Users\pdf\Desktop\monitor\test3\data\temp'

# Call the function
delete_files_in_temp(temp_directory)
