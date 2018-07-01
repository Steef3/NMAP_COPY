#NOTE: DO NOT TRUST SIMPLE HTTP SERVER

'''
#TO DO
Cleanup code
Add function to the end of every task to ask, whether the user wants to do anything else
Make directory responses show up cleaner in the terminal/independent of how long the directory name is
Input via text file/list of IPs.
Input cleaning for website entries (DNS), e.g. google.co is not possible
Test mode for any website and directory
RangePorts not working, when inputting 443-443, for example.
RangePorts not working and taking forever in any case.
s.connect not working, if put into a function.
Control+C not immediately exiting.
Web requests will be sent to every port. Needs to be fixed.
FIXED: Fix timeout default for webrequests.
Program closes out, if no valid response from a web request.
Open port but NO web server leads to exception of web server AND ports... (should only be for web)
'''

import socket, ipaddress, requests, sys, bs4

def WebServer(ip,ports):
    WebSocket = "http://{}:{}".format(str(j),str(i))
    timeout_web = input("What would you like the timeout to be for this web request in seconds? (Please choose a whole number between 1 and 100. Default: 5) ")
    if timeout_web == '':
        timeout_web = '5'
    else:
        timeout_web = timeout_web

    print("Sending WebRequest to " + WebSocket + " with a timeout of {}.".format(timeout_web))

    try:
        response = requests.get(WebSocket,timeout=int(timeout_web))

        print("There is a WebServer at {} on port {}.".format(str(ip),str(ports)))

        headers = response.headers

        print("This is a(n) {}".format(headers['Server']),"server.")

        if response.status_code == 200:
            print("Code: 200, Ok.")
            html = bs4.BeautifulSoup(response.text, "html.parser")
            print("This is the title of the page: ", html.title )
        elif response.status_code == 201:
            print("Code: 201, Created.")
        elif response.status_code == 204:
            print("Code: 204, No Content.")
        elif response.status_code == 304:
            print("Code: 304, Not Modified.")
        elif response.status_code == 400:
            print("Code: 400, Bad Request.")
        elif response.status_code == 401:
            print("Code: 401, Unauthorized.")
        elif response.status_code == 403:
            print("Code: 403, Forbidden.")
        elif response.status_code == 404:
            print("Code: 404, Not Found.")
        elif response.status_code == 409:
            print("Code: 409, Conflict.")
        elif response.status_code == 418:
            print("Code: 418, I'm a teapot.")
        elif response.status_code == 500:
            print("Code: 500, Internal Server Error.")
        print("\n")

    except:
        print("There is probably no WebServer running here or it only accepts http requests with SSL/TLS.")
        print("\n")
        # This would run the exception of the port scan "Port is closed".
        # raise Exception ("There probably is no WebServer running here.")
        pass
    # For more info on status codes, please see http://www.restapitutorial.com/httpstatuscodes.html.


scan = input("Would you like scan via inputting an IP (ip), via inputting a website name (name) or would you like to go into webs server test mode (test)? ")
# FOR TESTING
# scan = 'ip'
# scan = 'name'
scan = 'test'
print(scan)

# Website testing
if scan == "test":
    # Multi-website and single directory testing
    website = input("Please input the website that you would like to scan! (e.g. google.com) ")
    website = "depaul.edu"
    directories = input("Please input the directories for the first level that you would like to scan divided by commas! (.e.g about,/,support,test) ")
    directories = "about,/,support,test"
    print(directories)
    directories = directories.split(",")
    print(directories)
    level_2 = input("Would you like to scan a second layer of directories? (yes/no) ")
    # level_2 = 'YeS'
    level_2 = 'nO'
    level_2 = level_2.lower()
    print(level_2)
    if level_2 == 'yes':
        directories2 = input("Please input the directories for the second level that you would like to scan divided by commas! (.e.g about,/,support,test) ")
        directories2 = 'about,/,support,test'
        print(directories2)
        directories2 = directories2.split(",")
        print(directories2)

    else:
        directories2 = ''
        print("No second-level directories specified.")

    for directory in directories:
        for directory2 in directories2:
            TestSocket = "https://" + website + "/" + directory + "/" + directory2
            response = requests.get(TestSocket, timeout=5)
            print("Testing {}/{}/{}!\t".format(website,directory,directory2),response)

    print("Testing complete. Exiting.")
    sys.exit()


elif scan == 'name':
    name = input("What is the name of the website that you would like to scan? (e.g. google.com) ")
    # name = 'brackets.io'
    name = 'secdaemons.org'
    # This is dangerous...
    global ip
    ip = socket.gethostbyname(name)
    ip = ip.split()
    print(ip)



elif scan == 'ip':
    # ip = input("Input IP: ")
    ipinput = input("Would you like to input an ip/network to scan via inputting into the terminal (terminal) or via a list in a text file (text)? ")
    # FOR TESTING
    ipinput = 'terminal'
    # ipinput = 'text'
    if ipinput == 'terminal':
        ip = input("Please input the ip address/network that you would like to scan (e.g. 140.192.40.120/32) ")
        # FOR TESTING
        # ip = '10.11.2.110'
        # ip = '127.0.0.1/32'
        # ip = '140.192.40.120/32'
        # ip = '140.192.40.120/30'
        # ip = '146.55.65.186/32' # DePaul iD Lab
        # NOT WORKING: ip = '62.116.130.8' # theuselessweb.com 80, "Sorry, no host found"
    else:
        pass
'''
NOTE: Needs to be fixed
    elif ipinput == 'text':
        list = input('Please input the name of the list that you would like to submit (e.g. "iplist.txt"): ')
        list = open('iplist.txt', 'r')
        ip = list.read().split("\n")
        print(ip)
        # ip = '140.192.40.120/32'
        # print("File Test")
'''



ans1 = input("Would you like to scan single ports (single) or a range of ports (range)? ")
# FOR TESTING
# ans1 = 'single'
ans1 = 'range'
# ans1 = 'file'

ans1 = ans1.lower()

if ans1 == 'single':
    ports_single = input("Please enter single ports separated by a comma (e.g. 80,443,3389) ")
    ports = ports_single.split(',')
    # FOR TESTING
    # ports = ['80']
    # ports = ['890']
    # ports = ['443']
    # ports = ['80', '443', '8000']
    # ports = ['80', '443', '8001', '8080', '9000']

    f = 's'
    print("SinglePorts: {}\n".format(ports))

elif ans1 == 'range':
    ports_range = input("Please enter a range of ports (e.g. 100-500) ")
    # FOR TESTING
    # ports_range = '442-444'
    ports_range = '0-65536'
    ports = ports_range.split('-')

    f = 'r'
    # print(type(ports[0]))
    print("RangePorts: {}\n".format(ports))

'''
# MAYBE: Port list from a file
elif ans1 == 'file':
    ports_file = open('portlist.txt', 'r')
    print(ports_file)
    ports = ports_file.split('\n')
    f = 'f'
    # print("FilePorts:{}".format(type(ports)))
    print("FilePorts: {}\n".format(ports))
'''

timeout_ports = input("What would you like the timeout be for the port scan in seconds? (Please choose a whole number between 1 and 100. Default: 5) ")
if timeout_ports == '':
    # timeout_ports = '5'
    # FOR TESTING
    timeout_ports = '1'
else:
    timeout_ports = timeout_ports

print(ip)
ip = '10.11.2.110'
# ip = '127.0.0.1'
for j in ipaddress.ip_network(ip):
    j = str(j)
    # print(j)
    print("\nScanning IP: {}\n".format(j))
    open_ports = []

    # TCP SCAN - Single Ports
    if f == 's':

        for i in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(float(timeout_ports))
            # print(s)
            print("Trying port number",i,".")
            try:
                s.connect((j,int(i)))
                print("Port Connection Test Single successful.")
                open_ports.append(i)
                # print("Open_Ports Appending Test Single successful.")

                print("Test 2")

                try:
                    banner = s.recv(1024)
                    print(banner)
                    print("Test 3a")
                except:
                    print("Test 3b")
                    pass


                # FOR TESTING
                # print("SingleTest 1")

                print("Test 4")
                WebServer(j,i)

            except:
                print("This port is closed.\n")
                pass

    # TCP SCAN - Range Ports/File Ports
    elif f == 'r':
        for i in range(int(ports[0]),int(ports[1])):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(float(timeout_ports))
            # print(s)
            print("Trying port number",i,".")
            # WORKS UP UNTIL HERE
            # print(s)
            try:
                s.connect((j,int(i)))
                print("Port Connection Test Range successful.")
                open_ports.append(i)
                # print("Open_Ports Appending Test Range.")

                print("Test 2")

                try:
                    banner = s.recv(1024)
                    print(banner)
                    print("Test 3a")
                except:
                    print("Test 3b")
                    pass

                # FOR TESTING
                # print("RangeTest 1")
                WebServer(j,i)

            except:
                print("This port is closed.\n")
                pass

    print("Summary/These ports are all open:")
    if len(open_ports) == 0:
        print("NONE.\n")
    else:
        for i in open_ports:
            print(i)
            # print("\n")
