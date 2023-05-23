import os
import shutil
import json
import subprocess
from urllib.parse import urlparse
from requests.exceptions import MissingSchema
from pathlib import Path
from datetime import datetime

class SubDomain_Enumeration:
    def __init__(self, target_url, timestamp):
        # Initialize the SubDomain_Enumeration object with target_url and timestamp
        self.timestamp = timestamp
        self.target_url = target_url
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        self.tool_path = os.path.join(self.script_path,'subDomainsBrute-master', 'subDomainsBrute.py')
        self.parsed_url = urlparse(self.target_url)
        file_name = f"{self.parsed_url.netloc}_subDomains.txt"
        self.output_dir = os.path.join(self.main_path, 'output_file', f'{timestamp}')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file=os.path.join(self.output_dir, file_name)
        self.logfile = f"{self.main_path}\\result\\{timestamp}\\log.json"
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def progress_record(self, module=None, finished=False):
        # Record the progress of a module
        if os.path.exists(self.logfile) is False:
            shutil.copy(f"{self.main_path}\\config\\log_template.json", f"{self.main_path}\\result\\{self.timestamp}\\log.json")
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

    def run_subdomainsbrute(self):
        # Run the subdomains brute force tool and record its progress
        cmd = f'python {self.tool_path} {self.parsed_url.netloc} -p 10 -o {self.output_file}'
        print("SubDomainsBrute is running, please wait...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error occurred: {stderr.decode('utf-8', 'ignore')}")
        else:
            print("SubDomainsBrute has completed its work")
            self.progress_record(module='subdomainbrute', finished=True)

def get_subdomains(target_url, timestamp):
    # Create a SubDomain_Enumeration object and run subdomains brute force
    tool = SubDomain_Enumeration(target_url, timestamp)
    tool.run_subdomainsbrute()

if __name__ == '__main__':
    # Main function: get the target URL from user input and run get_subdomains
    try:
        TARGET_URL = input("Please enter the target website url：")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    except MissingSchema:
        print("Invalid URL, please make sure to enter the correct address, such as www.example.com")
        exit(1)
    get_subdomains(TARGET_URL, timestamp)
