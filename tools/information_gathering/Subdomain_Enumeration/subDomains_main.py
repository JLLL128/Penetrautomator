import os
import subprocess
from urllib.parse import urlparse
from requests.exceptions import MissingSchema
from pathlib import Path
from datetime import datetime

class SubDomain_Enumeration:
    def __init__(self, target_url, timestamp):
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

    def run_subdomainsbrute(self):
        cmd = f'python {self.tool_path} {self.parsed_url.netloc} -p 10 -o {self.output_file}'
        print("SubDomainsBrute is running, please wait...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error occurred: {stderr.decode('utf-8', 'ignore')}")
        else:
            print("SubDomainsBrute has completed its work")

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
