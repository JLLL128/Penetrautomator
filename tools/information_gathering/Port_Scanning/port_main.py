import os
import shutil
import json
import subprocess
import datetime
from urllib.parse import urlparse
from pathlib import Path

class Port_Scanning:
    def __init__(self, target_url,timestamp):
        # Initialize the Port_Scanning object with target_url and timestamp
        self.timestamp = timestamp
        self.target_url = target_url
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        self.parsed_url = urlparse(self.target_url)
        file_name = f"{self.parsed_url.netloc}_port.txt"
        self.tool_path = os.path.join(self.script_path, 'nmap', 'nmap.exe')
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

    def run_port_scan(self):
        # Run the port scan and record its progress
        cmd = f'{self.tool_path} {self.parsed_url.netloc} -sT -Pn --unprivileged'
        print("Nmap Port Scanning is running, please wait...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,bufsize=0)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error occurred: {stderr.decode('utf-8', 'ignore')}")
        else:
            print("Nmap Port Scanning has completed its work")
            with open(self.output_file, 'w',encoding='utf-8') as f:
                f.write(stdout.decode('utf-8', 'ignore'))
                self.progress_record(module='port_scan', finished=True)

def get_port(target_url,timestamp):
    # Create a Port_Scanning object and run port scan
    tool = Port_Scanning(target_url,timestamp)
    tool.run_port_scan()

if __name__ == '__main__':
    # Main function: get the target URL from user input and run get_port
    TARGET_URL = input("Please enter the target website url：")
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # Add global variable TIME
    get_port(TARGET_URL,TIMESTAMP)
