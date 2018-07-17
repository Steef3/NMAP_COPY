#NOTE: DO NOT TRUST SIMPLE HTTP SERVER

'''
# TO DO
Add a more thorough summary and make it outputable as .txt or something
Add graphs for open ports on various IPs
Add an info for what flags for the customized packet scan are possible
Add a way to have multiple ranges at once, e.g. 79-81 and 440-445
If no input is given for the time to wait, the default-waiting-time is 10 seconds
Create a way to test all possible options with a single click (make whole program a function and provide a loop with different variables?)
Read up on threading and timers to get rid of the KeyboardInterrupt for auto_continue
Since no one wants a slow program, consider speed more as soon as you become a pro (will that ever happen? Lol)
Since this is a security program, consider security more (i.e. global ip removed, importing only stuff that is necessay, etc.)
Make code more modular (for a reason... Also, find that reason)
Make directory-scanning scalable
Better commenting needed throughout the code
Make code super-clean (haha)
Show default pathway at some point (e.g. ip -> single -> text and so on)
Add function to the end of every task to ask, whether the user wants to do anything else
Make directory responses show up cleaner in the terminal/independent of how long the directory name is
Input cleaning for website entries (DNS), e.g. google.co is not possible
Bypassed: RangePorts not working, when auto_continueting 443-443, for example.
s.connect not working, if put into a function.
Control+C not immediately exiting during trying of ports.
Web requests will be sent to every port. Needs to be fixed. Problem: trying for banner times out, higher timeout (100) leads to b'' (without try statement)
Program closes out, if no valid response from a web request.
Open port but NO web server leads to exception of web server AND ports... (should only be for web)
Fix global ip in if-statement
'''

'''
# Fun websites to test
http://httpbin.org/status/418
http://httpstat.us/418?sleep=5
'''

import socket, ipaddress, requests, sys, bs4, time
# _thread, threading
from termcolor import colored
from scapy.all import *
from random import randint

if __name__ == "__main__":

    ###########################################
    # Display values that will be used in red #
    ###########################################
    def chosen_value(value):
        chosen_value = colored("Value(s) used: {}.".format(value), "red")
        return(chosen_value)

    # Read up on threading and timer to get rid of the KeyboardInterrupt
    ##############################################################################################
    # Use a default value after a certain time, unless the user hits CTRL + C and inputs a value #
    ##############################################################################################
    def auto_continue(prompt, time_to_wait):
        print(prompt)

        print("You have {} second(s) before the default value kicks in.".format(waitingtime))

        try:
            for i in range(0, 10):
                time.sleep(waitingtime/10)
                # FOR TESTING
                # print(i)
                if i == 9:
                    print("Using default values.........")
                    # FOR TESTING
                    # prompt = 'The time has outed.'
                else:
                    print('.', end='', flush=True)
                    pass
        except KeyboardInterrupt:
            prompt = input("\nInput: ")
            print(colored("You input:{}.".format(prompt)), "red")
            return(prompt)

    ###############################################
    # If no value is input, use the default value #
    ###############################################
    def default(default_name, default_value):
        if default_name == None:
            default_name = default_value
            return(default_name)
        else:
            default_name = default_name
            return(default_name)

    #########################################################
    # Send a web request to root and interpret the response #
    #########################################################
    def web_server(ip,ports):
        web_socket = "http://{}:{}".format(str(j),str(i))
        timeout_web = auto_continue("What would you like the timeout to be for this web request in seconds? (Please choose a whole number between 1 and 100. Default: 5) ", None)
        timeout_web = default(timeout_web, '5')
        print(chosen_value(timeout_web))

        print("Sending WebRequest to " + web_socket + " with a timeout of {}.".format(timeout_web))

        try:
            response = requests.get(web_socket,timeout=int(timeout_web))
            print("There is a web_server at {} on port {}.".format(str(ip),str(ports)))
            headers = response.headers
            print("This is a(n) {}".format(headers['Server']),"server.")

            if response.status_code == 200:
                print("Code: 200, Ok.")
                html = bs4.BeautifulSoup(response.text, "html.parser")
                print("Page Title: ", html.title )
            # The following lines can probably be improved by using a dictionairy or so
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
            print("There is probably no web_server running here or it only accepts http requests with SSL/TLS.")
            print("\n")
            # This would run the exception of the port scan "Port is closed".
            # raise Exception ("There probably is no web_server running here.")
            pass
        # For more info on status codes, please see http://www.restapitutorial.com/httpstatuscodes.html.

    #########################################################################
    # Send a web request to a specific directory and interpret the response #
    #########################################################################
    def directory_scan():
        # Multi-website and 2-level directory testing
        website = auto_continue("Please input the website that you would like to scan! (e.g. google.com) ", None)
        website = default(website, "secdaemons.org")
        print(chosen_value(website))
        directories = auto_continue("Please auto_continue the directories for the first level that you would like to scan divided by commas! (.e.g about,/,support,test) ", None)
        directories = default(directories, 'about,/,support,test,dokuwiki')
        directories = directories.split(",")
        print(chosen_value(directories))
        level_2 = auto_continue("Would you like to scan a second layer of directories? (yes/no) ", None)
        # level_2 = 'YeS'
        level_2 = 'nO'
        level_2 = level_2.lower()
        print(chosen_value(level_2))
        if level_2 == 'yes':
            directories2 = auto_continue("Please auto_continue the directories for the second level that you would like to scan divided by commas! (.e.g about,/,support,test) ", None)
            directories2 = default(directories2, 'about,/,support,test,dokuwiki')
            directories2 = directories2.split(",")
            print(chosen_value(directories2))

        else:
            directories2 = ''
            print("No second-level directories specified.")

        ssl = auto_continue("Do you trust this website? Requests will check for a certificate but might not find one. Inputting \'yes\' for this will NOT verify the certificate of the website. (Default: yes) ", None)
        ssl = default(ssl, 'yes')
        print(chosen_value(ssl))

        if ssl == 'yes':
            verify = False
        else:
            verify = True

        if directories2 == '':
            for directory in directories:
                TestSocket = "https://" + website + "/" + directory
                print("Testing {}/{}!".format(website,directory))
                response = requests.get(TestSocket, timeout=5, verify=verify)
                print("Response:{}!\n".format(response))
        else:
            for directory in directories:
                for directory2 in directories2:
                    TestSocket = "https://" + website + "/" + directory + "/" + directory2
                    print("Testing {}/{}/{}!".format(website,directory,directory2))
                    response = requests.get(TestSocket, timeout=5, verify=verify)
                    print("Response:{}!\n".format(response))

        print(colored("Testing complete. Exiting.", "yellow"))
        sys.exit()

    #######################################
    # Send customized packets using Scapy #
    #######################################
    # https://scapy.readthedocs.io/en/latest/installation.html
    def hardcore_scan():
        print("This mode will let you craft customized packets to send! At the moment, only IP packets are supported.")

        src = auto_continue("Please input the destination ip (Default: 192.168.5.100). ", None)
        src = default(src, '192.168.5.100')
        print(chosen_value(src))

        dst = auto_continue("Please input the destination ip (Default: 192.168.1.1). ", None)
        dst = default(dst, '192.168.1.1')
        print(chosen_value(dst))

        ptype = auto_continue("Please specify what type of packet to scan (Default: TCP). ", None)
        ptype = default(ptype, 'TCP')
        print(chosen_value(ptype))

        flags = auto_continue("Please input the flags that you would like to set without any commas (Default: S (for SYN)). ", None)
        flags = default(flags, 'S')
        print(chosen_value(flags))

        sport = auto_continue("Please input the destination port (Default: 80). ", None)
        sport = default(sport, randint(1, 65535))
        print(chosen_value(sport))

        dport = auto_continue("Please input the destination port (Default: 80). ", None)
        dport = default(dport, 80)
        print(chosen_value(dport))

        if ptype == 'TCP':
            send(IP(src=src,dst=dst)/TCP(dport=dport,flags=flags))
        elif ptype == 'UDP':
            send(IP(src=src,dst=dst)/UDP(dport=dport,flags=flags))
        else:
            print("Nope.")

        sys.exit()

    #######################################################################################
    # Get the ip address form a text file or terminal input and use that ip to do the scan #
    ########################################################################################
    def ip_scan():
        ip_in = auto_continue("Would you like to input an ip/network to scan via inputting into the terminal (terminal) or via a list in a text file (text)? ", None)
        ip_in = default(ip_in, 'text')
        print(chosen_value(ip_in))
        # Dangerous dangerous dangerous..... FIX NEEDED
        global ip
        if ip_in == 'terminal':
            ip = auto_continue("Please input the ip address/network that you would like to scan (e.g. 140.192.40.120/32) ", None)
            ip = default(ip, '140.192.40.120/32') # secdaemons.org
            print(chosen_value(ip))

        elif ip_in == 'text':
            ipfile = auto_continue("Please input the name of the list that you would like to submit (e.g. \"iplist.txt\"): ", None)
            ipfile = default(ipfile, 'ips.txt')
            ipfile = open(ipfile, 'r')
            ip = ipfile.read()
            ipfile.close()
            ip = ip.split('\n')
            print(chosen_value(ip))

    ########################################################################
    # Get the ip address from a domain name and use that ip to do the scan #
    ########################################################################
    def name_scan():
        name = auto_continue("What is the name of the website that you would like to scan? (e.g. google.com) ", None)
        name = default(name, 'secdaemons.org')
        # This is dangerous...
        global ip
        ip = socket.gethostbyname(name)
        ip = ip + '/32'
        print(chosen_value(ip))

    '''
    ###########################
    # THE PROGRAM STARTS HERE #
    ###########################
    '''

    info = 'At the current state of the program, you need to press Ctrl + C to input stuff, except for the time to wait value right after this line.'
    print(colored(info, "yellow"))

    waitingtime = float(input(colored("Please input the time in second(s) that the program should wait for inputs until going on with default values: ", "yellow")))
    print(chosen_value(waitingtime))

    scan = auto_continue("Would you like scan ports (ports), test a website for directories (directory) or go into hardcore mode (hardcore) (Default: )? ", None)
    scan = default(scan, 'directory')
    print(chosen_value(scan))

    if scan == 'ports':
        port_scan = auto_continue("Would you like to input an ip (ip) or a domain name (name)? ", None)
        port_scan = default(port_scan, 'ip')
        print(chosen_value(port_scan))

        if port_scan == 'name':
            name_scan()

        # IP address port testing
        elif port_scan == 'ip':
            ip_scan()

    # Website directory testing
    elif scan == "directory":
        directory_scan()

    elif scan == "hardcore":
        hardcore_scan()

    ans1 = auto_continue("Would you like to input single ports (single) or a range of ports (range) or single ports via a file (file)? ", None)
    ans1 = default(ans1, 'file')
    ans1 = ans1.lower()
    print(chosen_value(ans1))

    if ans1 == 'single':
        ports_single = auto_continue("Please enter single ports separated by a comma (e.g. 80,443,3389) ", None)
        ports_single = default(ports_single, '80,443,8000')

        ports = ports_single.split(',')
        f = 's'

        print(chosen_value(ports))

    elif ans1 == 'range':
        ports_range = auto_continue("Please enter a range of ports (e.g. 100-500). If you want to only scan one port, please auto_continue like 443-444 to scan 443. ", None)
        ports_range = default(ports_range, '441-444')

        ports = ports_range.split('-')
        f = 'r'

        print(chosen_value(ports))

    elif ans1 == 'file':
        ports_file = auto_continue("What file would you like to use? (e.g. ports.txt) ", None)
        ports_file = default(ports_file, 'ports.txt')

        ports_file = open(ports_file, 'r')
        ports = ports_file.read()
        ports_file.close()
        ports = ports.split('\n')
        f = 's'

        print(chosen_value(ports))

    timeout_ports = auto_continue("What would you like the timeout be for the port scan in seconds? (Please choose a whole number between 1 and 100. Default: 5) ", None)
    timeout_ports = default(timeout_ports, '5')
    print(chosen_value(timeout_ports))

    # FOR TESTING
    # print(ip)
    for k in ip:
        ip = k
        for j in ipaddress.ip_network(ip):
            j = str(j)
            open_ports = []

            # TCP SCAN - Single Ports
            if f == 's':
                for i in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(float(timeout_ports))
                    print("Trying {}:{}.".format(j,i))
                    try:
                        s.connect((j,int(i)))
                        print("Port Connection Test Single successful.")
                        open_ports.append(i)

                        try:
                            banner = s.recv(1024)
                            print(banner)
                        except:
                            pass

                        web_server(j,i)

                    except:
                        print("This port is closed.\n")
                        pass

            # TCP SCAN - Range Ports/File Ports
            elif f == 'r':
                for i in range(int(ports[0]),int(ports[1])):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(float(timeout_ports))
                    print("Trying {}:{}.".format(j,i))

                    try:
                        s.connect((j,int(i)))
                        print("Port Connection Test Range successful.")
                        open_ports.append(i)

                        try:
                            banner = s.recv(1024)
                            print(banner)
                        except:
                            pass

                        web_server(j,i)

                    except:
                        print("This port is closed.\n")
                        pass

            print(colored("Summary/These ports are all open for {}:".format(j), "white"))
            if len(open_ports) == 0:
                print("NONE.\n---------------------------------------\n")
            else:
                for i in open_ports:
                    print(i)
                print("----------------------------------------\n")
