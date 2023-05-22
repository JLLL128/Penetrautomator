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
        self.target_url = target_url
        self.timestamp=timestamp
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        #print(self.main_path)
        self.tool_path = os.path.join(self.script_path,'dirsearch-master', 'dirsearch.py')
        #print(self.tool_path)
        parsed_url = urlparse(self.target_url)
        file_name = f"{parsed_url.netloc}.txt"
        self.output_dir = os.path.join(self.main_path, 'output_file', f'{timestamp}')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file=os.path.join(self.output_dir, file_name)
        self.logfile = f"{self.main_path}\\result\\{timestamp}\\log.json"
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)
        self.logfile = f"{self.main_path}\\result\\{timestamp}\\log.json"
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def progress_record(self, module=None, finished=False):
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

            # 创建一个新的文件来保存处理过的输出
            processed_output_file = os.path.splitext(self.output_file)[0] + '_directory.txt'
            with open(processed_output_file, 'w') as f:
                for line in lines:
                    if line.startswith(('200', '301', '302', '404', '500')):
                        parts = line.split()
                        status_code = parts[0]
                        url = parts[2]  # parts[2] is the URL
                        f.write(f"{status_code} {url}\n")

            # 删除原始输出文件
            os.remove(self.output_file)
            self.progress_record(module='dirsearch', finished=True)

def get_directory(target_url,timestamp):
    tool = Directory_Enumeration(target_url,timestamp)
    tool.run_dirsearch()

if __name__ == '__main__':
    try:
        TARGET_URL = input("请输入目标网站url：")
    except MissingSchema:
        print("无效的URL，请确保输入正确的网址，例如www.example.com")
        exit(1)
    TIMESTAMP=datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 添加全局变量 TIME
    get_directory(TARGET_URL,TIMESTAMP)
