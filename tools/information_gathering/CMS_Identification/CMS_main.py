import os
import json
import shutil
import requests
import json
import datetime
from urllib.parse import urlparse
from pathlib import Path
from requests.exceptions import MissingSchema

class CMS_Identification:
    def __init__(self, target_url,timestamp):
        # Initialize the CMS_Identification object with target_url and timestamp
        self.timestamp=timestamp
        self.target_url = target_url
        self.api_key = 'w9vllsvks6tk4ynmhwicwaxth2c9kmuokb9rnrih4qdgvuo8nak1a26ggee7jou4j2n2es'  # Replace this with your actual API key
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        parsed_url = urlparse(self.target_url)
        file_name = f"{parsed_url.netloc}_cms.json"
        self.output_dir = os.path.join(self.main_path, 'output_file',f'{timestamp}')
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

    def query_cms(self):
        # Query the CMS of the target_url
        api_url = 'https://whatcms.org/API/Tech'
        params = {
            'key': self.api_key,
            'url': self.target_url,
        }
        response = requests.get(api_url, params=params)
        return response.json()

    def run_cms_identification(self):
        # Run the CMS identification and record its progress
        print("CMS Query is running, please wait...")
        result = self.query_cms()
        final_result = {"url": self.target_url, "code": result["result"]["code"], "msg": result["result"]["msg"]}
        if result["result"]["code"] == 200:
            final_result["results"] = result["results"]
        with open(self.output_file, 'w') as f:
            json.dump(final_result, f,indent=4)
        print("CMS Query has completed its work")
        self.progress_record(module='cms_identification', finished=True)

def get_CMS(target_url,timestamp):
    # Create a CMS_Identification object and run CMS identification
    tool = CMS_Identification(target_url,timestamp)
    tool.run_cms_identification()

if __name__ == "__main__":
    # Main function: get the target URL from user input and run get_CMS
    try:
        TARGET_URL = input("Please enter the target website url：")
    except MissingSchema:
        print("Invalid URL, please make sure to enter the correct address, such as www.example.com")
        exit(1)
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    get_CMS(TARGET_URL,TIMESTAMP)
