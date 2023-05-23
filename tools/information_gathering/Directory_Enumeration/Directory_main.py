import os
import shutil
import json
import requests
import subprocess
from urllib.parse import urlparse
from requests.exceptions import MissingSchema
from pathlib import Path
import datetime

class Directory_Enumeration:
    def __init__(self, target_url,timestamp):
        # Initialize the Directory_Enumeration object with target_url and timestamp
        self.target_url = target_url
        self.timestamp=timestamp
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        self.tool_path = os.path.join(self.script_path,'dirsearch-master', 'dirsearch.py')
        parsed_url = urlparse(self.target_url)
        file_name = f"{parsed_url.netloc}.txt"
        self.output_dir = os.path.join(self.main_path, 'output_file', f'{timestamp}')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file=os.path.join(self.output_dir, file_name)
        self.logfile = f"{self.main_path}\\result\\{timestamp}\\log.json"
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def progress_record(self, module=None, finished=False):
        # Record the progress of a module
        if os.path.exists(self.logfile) is False:
            shutil.copy(f"{self.main_path}/config/log_template.json", f"{self.main_path}/result/{self.timestamp}/log.json")
        with open(self.logfile, "r", encoding="utf-8") as f1:
            log_json = json.loads(f1.read())
        if finished is False:
            if log_json[module] is False:
                return False
            elif log_json[module] is True:
                return True
        elif finished is True:
            log_json[module] = True
            with open(self.logfile, "w", encoding="utf-8") as f:
                f.write(json.dumps(log_json))
            return True

    def run_dirsearch(self):
        # Run the dirsearch tool and record its progress
        cmd = f'python {self.tool_path} -u {self.target_url} -o {self.output_file}'
        print("Dirsearch is running, please wait...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error occurred: {stderr.decode('utf-8', 'ignore')}")
        else:
            print("Dirsearch has completed its work")
            with open(self.output_file, 'r') as f:
                lines = f.readlines()

            # Create a new file to save the processed output
            processed_output_file = os.path.splitext(self.output_file)[0] + '_directory.txt'
            with open(processed_output_file, 'w') as f:
                for line in lines:
                    if line.startswith(('200', '301', '302', '404', '500')):
                        parts = line.split()
                        status_code = parts[0]
                        url = parts[2]  # parts[2] is the URL
                        f.write(f"{status_code} {url}\n")

            # Delete the original output file
            os.remove(self.output_file)
            self.progress_record(module='dirsearch', finished=True)

def get_directory(target_url,timestamp):
    # Create a Directory_Enumeration object and run dirsearch
    tool = Directory_Enumeration(target_url,timestamp)
    tool.run_dirsearch()

if __name__ == '__main__':
    # Main function: get the target URL from user input and runget_directory
    try:
        TARGET_URL = input("Please enter the target website url：")
    except MissingSchema:
        print("Invalid URL, please make sure to enter the correct address, such as www.example.com")
        exit(1)
    TIMESTAMP=datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # Add global variable TIME
    get_directory(TARGET_URL,TIMESTAMP)
