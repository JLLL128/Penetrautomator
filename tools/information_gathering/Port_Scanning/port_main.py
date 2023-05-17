import os
import subprocess
import datetime
from urllib.parse import urlparse
from pathlib import Path

class Port_Scanning:
    def __init__(self, target_url,timestamp):
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

    def run_port_scan(self):
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

def get_port(target_url,timestamp):
    tool = Port_Scanning(target_url,timestamp)
    tool.run_port_scan()

if __name__ == '__main__':
    TARGET_URL = input("请输入目标网站url：")
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 添加全局变量 TIME
    get_port(TARGET_URL,TIMESTAMP)
