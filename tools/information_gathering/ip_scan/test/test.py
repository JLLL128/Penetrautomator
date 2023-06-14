import collections
import concurrent.futures
import os
import platform
import queue
import socket
import struct
import subprocess
import threading
import time
from pathlib import Path
import re
import random
import ipaddress

alivehosts = []


def run_ip_scan(target_ip):
    if target_ip == "":
        print("IP is none")
        return
    allip = parse_ip(target_ip)
    if allip == None or len(allip) == 0:
        return

    if len(allip) > 0:
        alivehosts = checkalive(allip)
        print("[*] Ping alive hosts len is: {0}".format(len(alivehosts)))


def parse_ip(target_ip):
    hosts = parse_ip_part(target_ip)
    return hosts


def parse_ip_part(target_ip):
    reg = re.compile("[a-zA-Z]+")
    allip = []
    # 扫描/8字段
    if target_ip.endswith("/8"):
        return parseIP8(target_ip)
    # /24 /16 /8 /xxx等字段
    elif target_ip.find("/") != -1:
        return parseIP2(target_ip)
    # 域名判断
    elif reg.match(target_ip):
        allip.append(target_ip)
        return allip
    # 192.168.1.1-192.168.1.100
    elif target_ip.find("-") != -1:
        # print(target_ip)
        return parseIP1(target_ip)
    # only one ip
    else:
        testip = check_ip(target_ip)
        if testip == None or testip == "":
            return None
        allip.append(target_ip)
        return allip


def parseIP8(ip):
    allip = []
    realip = ip[:len(ip) - 2]
    testip = check_ip(realip)
    if testip == None or testip == "":
        return None

    iprange = ip.split(".")[0]
    for i in range(0, 256):
        for j in range(0, 256):
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, 1))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, 2))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, 4))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, 5))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, random.randint(6, 55)))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, random.randint(56, 100)))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, random.randint(101, 150)))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, random.randint(151, 200)))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, random.randint(201, 253)))
            allip.append("{0}.{1}.{2}.{3}".format(iprange, i, j, 254))

    return allip


def parseIP2(ip):
    allip = parseIP1(get_ip_range(ip))
    return allip


def get_ip_range(ip):
    interface = ipaddress.ip_interface(ip)
    network = interface.network

    start = network.network_address
    end = network.broadcast_address

    ip_range = "{0}-{1}".format(start, end)
    return ip_range


def parseIP1(ip):
    IPRange = ip.split("-")
    testIP = check_ip(IPRange[0])
    AllIP = []
    if len(IPRange[1]) < 4:
        Range = int(IPRange[1])
        if testIP == None or Range > 255:
            return None
        SplitIP = IPRange[0].split(".")
        ip1 = int(SplitIP[3])
        ip2 = int(IPRange[1])
        PrefixIP = ".".join(SplitIP[0:3])
        if ip1 > ip2:
            return None
        for i in range(ip1, ip2 + 1):
            AllIP.append(PrefixIP + "." + str(i))
    else:
        SplitIP1 = IPRange[0].split(".")
        SplitIP2 = IPRange[1].split(".")
        if len(SplitIP1) != 4 or len(SplitIP2) != 4:
            return None
        start, end = [0] * 4, [0] * 4
        for i in range(4):
            ip1 = int(SplitIP1[i])
            ip2 = int(SplitIP2[i])
            if ip1 > ip2:
                return None
            start[i], end[i] = ip1, ip2
        startNum = start[0] << 24 | start[1] << 16 | start[2] << 8 | start[3]
        endNum = end[0] << 24 | end[1] << 16 | end[2] << 8 | end[3]
        for num in range(startNum, endNum + 1):
            ip = socket.inet_ntoa(struct.pack(">I", num))
            AllIP.append(ip)
    return AllIP


def check_ip(ip):
    # invalid ip address will return None
    try:
        if ip.find("/") != -1:
            testip = ipaddress.ip_network(ip)
        else:
            testip = ipaddress.ip_address(ip)
        return testip
    # except ValueError
    except:
        return None


def checkalive(hosts):
    alivehosts = run_ping(hosts)
    if len(hosts) > 1000:
        arrTop, arrLen = arraycountvaluetop(alivehosts, 10, True)
        for i in range(len(arrTop)):
            output = "[*] LiveTop {0} 段存活数量为: {1}".format(arrTop[i] + ".0.0/16", arrLen[i])
            print(output)

    if len(hosts) > 256:
        arrTop, arrLen = arraycountvaluetop(alivehosts, 10, False)
        for i in range(len(arrTop)):
            output = "[*] LiveTop {0} 段存活数量为: {1}".format(arrTop[i] + ".0/24", arrLen[i])
            print(output)

    return alivehosts


def run_ping(hosts):
    osenv = ""
    if platform.system() != "Windows":
        osenv = "/bin/bash"

    for host in hosts:
        thread = threading.Thread(target=ping_host, args=(host, osenv, alivehosts))
        thread.start()
    return alivehosts


def ping_host(host, osenv, alivehosts):
    if exec_command_ping(host, osenv):
        print("(ping) Target {0} is alive".format(host))
        alivehosts.append(host)
    return alivehosts


def exec_command_ping(host, osenv):
    if platform.system() == "Windows":
        command = subprocess.run(["cmd", "/c", "ping -n 1 -w 1 " + host + " && echo true || echo false"],
                                 stdout=subprocess.PIPE)
        output = command.stdout.decode("utf-8").split("\n")
        if "true" in output:
            return True
        else:
            return False

    elif platform.system() == "Linux":
        command = subprocess.run([osenv, "-c", "ping -c 1 -w 1 " + host + " >/dev/null && echo true || echo false"],
                                 stdout=subprocess.PIPE)
        output = command.stdout.decode("utf-8").split("\n")
        if "true" in output:
            return True
        else:
            return False

    elif platform.system() == "Darwin":
        command = subprocess.run([osenv, "-c", "ping -c 1 -W 1 " + host + " >/dev/null && echo true || echo false"],
                                 stdout=subprocess.PIPE)
        output = command.stdout.decode("utf-8").split("\n")
        if "true" in output:
            return True
        else:
            return False


def arraycountvaluetop(self, alivehosts, livetop, flag):
    if len(alivehosts) == 0 or alivehosts == None:
        return [], []
    arrMap1 = collections.defaultdict(int)
    arrMap2 = {}
    for value in alivehosts:
        line = value.split(".")
        if len(line) == 4:
            if flag:
                value = f"{line[0]}.{line[1]}"
            else:
                value = f"{line[0]}.{line[1]}.{line[2]}"
            arrMap1[value] += 1
    arrMap2 = dict(arrMap1)
    arrTop, arrLen = [], []
    for _ in range(len(arrMap1)):
        maxCountKey, maxCountVal = '', 0
        for key, val in arrMap2.items():
            if val > maxCountVal:
                maxCountVal = val
                maxCountKey = key
        arrTop.append(maxCountKey)
        arrLen.append(maxCountVal)
        if len(arrTop) >= livetop:
            return arrTop, arrLen
        del arrMap2[maxCountKey]
    return arrTop, arrLen


if __name__ == "__main__":
    ip = "36.152.44.0/24"
    run_ip_scan(ip)
