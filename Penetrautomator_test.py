from requests.exceptions import MissingSchema
from tools.information_gathering.Directory_Enumeration import Directory_main
from tools.information_gathering.CMS_Identification import CMS_main
from tools.information_gathering.Subdomain_Enumeration import subDomains_main
from tools.information_gathering.Port_Scanning import port_main
import requests
from requests.exceptions import MissingSchema
from urllib.parse import urlparse
import datetime
import os
import threading

TARGET_URL = None
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 添加全局变量 TIME

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
    try:
        input_url = input("请输入目标网站url：")
        TARGET_URL = get_url_with_scheme(input_url)
    except MissingSchema:
        print("无效的URL，请确保输入正确的网址，例如www.example.com")
        exit(1)

    # 创建一个新的文件夹来存储输出
    output_dir = os.path.join('output_file', f'{TIMESTAMP}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 创建线程
    t1 = threading.Thread(target=CMS_main.get_CMS, args=(TARGET_URL,TIMESTAMP))
    t2 = threading.Thread(target=Directory_main.get_directory, args=(TARGET_URL,TIMESTAMP))
    t3 = threading.Thread(target=subDomains_main.get_subdomains, args=(TARGET_URL,TIMESTAMP))
    t4 = threading.Thread(target=port_main.get_port, args=(TARGET_URL,TIMESTAMP))

    # 开始线程
    t1.start()
    t1.join()  # 等待 t1 线程完成

    t2.start()
    t2.join()  # 等待 t2 线程完成

    t3.start()
    t3.join()  # 等待 t3 线程完成

    t4.start()
    t4.join()  # 等待 t4 线程完成

if __name__ == "__main__":
    main()
