import os
import json
import shutil
import requests
import datetime
from urllib.parse import urlparse
from pathlib import Path
from requests.exceptions import MissingSchema

class Company_Identification:
    def __init__(self, target_url, timestamp):
        # Initialize the Company_Identification object with target_url and timestamp
        self.timestamp = timestamp
        self.target_url = target_url
        self.api_key = 'at_NK3eunVE0bILETCjizlVX668XoNM5'  # Replace this with your actual Whois API key
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path = Path(self.script_path).parent.parent.parent
        parsed_url = urlparse(self.target_url)
        file_name = f"{parsed_url.netloc}_company.json"
        self.output_dir = os.path.join(self.main_path, 'output_file', f'{timestamp}')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file = os.path.join(self.output_dir, file_name)
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

    def query_company(self):
        # Query the company of the target_url
        api_url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={self.api_key}&domainName={self.target_url}&outputFormat=JSON"
        response = requests.get(api_url)
        return response.json()

    def run_company_identification(self):
        # Run the company identification and record its progress
        print("Company Query is running, please wait...")
        result = self.query_company()
        company_name = result.get("WhoisRecord", {}).get("registrant", {}).get("organization")
        final_result = {"url": self.target_url, "company": company_name}
        with open(self.output_file, 'w') as f:
            json.dump(final_result, f, indent=4)
        print("Company Query has completed its work")
        self.progress_record(module='company_identification', finished=True)

def get_company(target_url, timestamp):
    # Create a Company_Identification object and run company identification
    tool = Company_Identification(target_url, timestamp)
    tool.run_company_identification()

if __name__ == "__main__":
    # Main function: get the target URL from user input and run get_company
    try:
        TARGET_URL = input("Please enter the target website url：")
    except MissingSchema:
        print("Invalid URL, please make sure to enter the correct address, such as www.example.com")
        exit(1)
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    get_company(TARGET_URL, TIMESTAMP)