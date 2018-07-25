import os

os_type = input("Please choose your OS for more information on what to install (w for Windows and m for MAC OS)!")

if os_type == 'w':
    print("You need winpcap and miktex.")
elif os_type == 'm':
    print("You need miktex.")

print("Upgrading pip...")
os.system("pip3 install --upgrade pip")

modules = "ipaddress, requests, beautifulsoup4, termcolor, scapy, pyx"
modules_split = modules.split(", ")

for i in modules_split:
    print("\n Installing module named \'" + i + "\'")
    os.system("pip3 install " + i)