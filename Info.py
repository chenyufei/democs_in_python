import ctypes
import re
import random

def get_ip():
    while True:
        ip = input("input the ip:")
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
            return ip
        else:
            print("input ip is error,please input the correct ip")

def get_port():
    while True:
        port = input("input the port:")
        if re.match(r"^[0-9]*[1-9][0-9]*$", port):
            return int(port)
        else:
            print("input port is error,please input the correct port")

def get_appeui():
    while True:
        appeui = input("input the appeui:")
        if re.match(r"^[a-fA-F0-9]+$", appeui):
            if len(appeui) == 16:
                return  appeui
            else:
                input("the length of appeui is error,input the correct legnth appeui")
        else:
            print("input appeui is error,please input the correct appeui")

def get_appkey():
    while True:
        appkey = input("input the appkey:")
        if re.match(r"^[a-fA-F0-9]+$", appkey):
            if len(appkey) == 32:
                return  appkey
            else:
                input("the length of appkey is error,input the correct legnth appkey")
        else:
            print("input appkey is error,please input the correct appkey")

def get_appnonce():
    return random.randint(130000000, 139999999)

