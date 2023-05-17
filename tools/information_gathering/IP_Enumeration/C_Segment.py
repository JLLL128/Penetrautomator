import socket
from urllib.parse import urlparse
import shodan
import datetime

class C_Segment_Shodan:
    def __init__(self, target_url,timestamp, api_key):
        self.target_url = target_url
        self.timestamp = timestamp
        self.api_key = api_key

    def run_c_segment_scan(self):
        try:
            api = shodan.Shodan(self.api_key)

            # Resolve URL to an IP address
            ip = socket.gethostbyname(urlparse(self.target_url).netloc)
            print(ip)

            # Calculate C segment
            c_net = ".".join(ip.split('.')[:-1]) + '.0/24'

            # Search Shodan for hosts in the C segment
            results = api.search(c_net)

            # Process the results
            for result in results['matches']:
                print(f'IP: {result["ip_str"]}')
                print(f'Data: {result["data"]}')
                print('---')
        except shodan.APIError as e:
            print(f'Error: {e}')

def get_c_segment(target_url,timestamp, api_key):
    tool = C_Segment_Shodan(target_url,timestamp, api_key)
    tool.run_c_segment_scan()

if __name__ == '__main__':
    TARGET_URL = input("请输入目标网站url：")
    API_KEY = input("请输入Shodan API key：")
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 添加全局变量 TIME
    get_c_segment(TARGET_URL, TIMESTAMP, API_KEY)
