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
    tool = SubDomain_Enumeration(target_url, timestamp)
    tool.run_subdomainsbrute()

if __name__ == '__main__':
    try:
        TARGET_URL = input("请输入目标网站url：")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    except MissingSchema:
        print("无效的URL，请确保输入正确的网址，例如www.example.com")
        exit(1)
    get_subdomains(TARGET_URL, timestamp)
