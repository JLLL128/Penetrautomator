from requests.exceptions import MissingSchema
from tools.information_gathering.Directory_Enumeration import Directory_main
from tools.information_gathering.CMS_Identification import CMS_main
from tools.information_gathering.Subdomain_Enumeration import subDomains_main
from tools.information_gathering.Port_Scanning import port_main
from tools.vulnerability_scanning import poc_main
from tools.information_gathering.Company_Identification import Company_main
from tools.vulnerability_scanning import poc_main
import requests
from requests.exceptions import MissingSchema
from urllib.parse import urlparse
import datetime
import os
import argparse  # 引入argparse库

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

TARGET_URL = None
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 添加全局变量 TIME

banner = f"""
{red}PeneAuto is a tool for automatically penetration{yellow}
  ___                _       _       
 | _ \___ _ _  ___  /_\ _  _| |_ ___ 
 |  _/ -_) ' \/ -_)/ _ \ || |  _/ _ \\
 |_| \___|_||_\___/_/ \_\_,_|\__\___/ {white}By JL
{end}"""

def get_url_with_scheme(url):
    if not url.startswith(('http://', 'https://')):
        try:
            response = requests.head('https://' + url, timeout=5)
            return 'https://' + url
        except requests.exceptions.RequestException:
            return 'http://' + url
    else:
        return url

def main():
    global TARGET_URL

    # 创建argparse对象
    parser = argparse.ArgumentParser(description="An Automated Penetration Testing Tool")
    parser.add_argument("-u", "--url", dest="url", required=True, help="TARGET_URL")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a","--all",action="store_true",help="full scan")
    group.add_argument("-c","--cms",action="store_true",help="cms identification only")
    args = parser.parse_args()

    try:
        input_url = args.url
        TARGET_URL = get_url_with_scheme(input_url)
    except MissingSchema:
        print("无效的URL，请确保输入正确的网址，例如www.example.com")
        exit(1)

    # 创建一个新的文件夹来存储输出
    output_dir = os.path.join('output_file', f'{TIMESTAMP}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(banner)
    if args.cms:
        CMS_main.get_CMS(TARGET_URL, TIMESTAMP)
        print("-cms success")
    else:

        # Running CMS_main
        CMS_main.get_CMS(TARGET_URL,TIMESTAMP)

        # Running Directory_main
        Directory_main.get_directory(TARGET_URL,TIMESTAMP)

        # Running subDomains_main
        subDomains_main.get_subdomains(TARGET_URL,TIMESTAMP)

        # Running port_main
        port_main.get_port(TARGET_URL,TIMESTAMP)

        # Running Company_main
        Company_main.get_company(TARGET_URL, TIMESTAMP)

        #Running poc_main
        poc_main.poc_scan(TARGET_URL,TIMESTAMP)

        # Running Xray
        poc_main.poc_scan(TARGET_URL, TIMESTAMP)

        print("defult sucess")

if __name__ == "__main__":
    main()
