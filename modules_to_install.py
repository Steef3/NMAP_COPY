import os

modules = "ipaddress, requests, beautifulsoup4, termcolor, scapy"
modules_split = modules.split(", ")

for i in modules_split:
    print("\n Installing module named \'" + i + "\'")
    os.system("pip3 install " + i)