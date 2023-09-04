import requests
import tkinter as tk
from tkinter import messagebox
import zipfile
import os
import shutil
import io
import subprocess


# Define your GitHub repository URL and the version tracking file URL
repo = 'Main'
authors = "IcyDiamond"

repository_url = f'https://github.com/{authors}/PythonDesktop-Files'
version_file_url = f'https://raw.githubusercontent.com/{authors}/PythonDesktop-Files/{repo}/PythonDesktop.py'

# Get the current version of the script
try:
    with open('PythonDesktop.py', 'r') as f:
        current_version = f.read().split("\n")
        for line in current_version:
            if "update_version =" in line:
                value = line.split("update_version = ")[1]
                value = value.replace("\r","")
                ver1 = float(value)
                current_version = ver1
                break
except FileNotFoundError:
    current_version='Null'

# Check the latest version on GitHub
response = requests.get(version_file_url)
if response.status_code == 200:
    for line in response.text.split("\n"):
        if "update_version =" in line:
            value = line.split("update_version = ")[1]
            value = value.replace("\r","")
            ver1 = float(value)
            latest_version = ver1
            break

    if current_version != latest_version:
        i = messagebox.askquestion('Update', 'Update Available\nDo you wish to Update?')
        if i == 'yes':
            i = messagebox.askquestion('Confirm', 'Are you Sure?')
            if i == 'no':
                pass
            else:
                print(f'Updating from version {current_version} to {latest_version}...')
                for i in os.listdir():
                    if i == 'Users' or i =='update.py':
                        pass
                    else:
                        try:
                            os.remove(i)
                        except PermissionError:
                            shutil.rmtree(i)

                        # Replace with the repository URL
                        repo_url = 'https://github.com/IcyDiamond/PythonDesktop-Files/archive/main.zip'

                        # Make a request to download the ZIP archive
                        response = requests.get(repo_url)

                        if response.status_code == 200:
                            # Extract the ZIP archive
                            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                                zip_file.extractall()
                            
                            print('Downloaded and extracted files successfully.')
                        else:
                            print(f'Failed to download files. Status code: {response.status_code}')

                print('Update complete. Please restart the script.')
        # Define the content of the new Python script
        new_script_content = """
import os
import shutil
os.remove('update.py')
for i in os.listdir('PythonDesktop-Files-Main'):
    shutil.move(f"PythonDesktop-Files-Main/{i}", os.getcwd())
    print(f'moving {i}')
shutil.rmtree('PythonDesktop-Files-Main')

def delete_self():
    try:
        # Get the absolute path of the current script
        script_path = os.path.abspath(__file__)

        # Attempt to delete the script file
        os.remove(script_path)

        # If successful, print a message and exit
        print(f"Script '{script_path}' deleted successfully.")
    except Exception as e:
        # If there's an error, print an error message
        print(f"Error deleting the script: {str(e)}")

if __name__ == "__main__":
    print("This script will delete itself after it's done.")
    
    # Your script logic goes here
    
    # Call the delete_self() function to delete the script
    delete_self()
"""

        # Specify the file name for the new script
        new_script_file = "temp_move_files.py"

        # Write the content to the new script file
        print('writing file to move Files')
        with open(new_script_file, "w") as file:
            file.write(new_script_content)

        # Import the necessary module to run the new script

        # Run the new script using the Python interpreter
        print('Moving Files')
        subprocess.Popen(["python", new_script_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    else:
        print('You are already using the latest version.')
else:
    print('Failed to check for updates.')

    
