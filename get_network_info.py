''' get_known_wifi_passwords.py - prints out known Wifi networks and corresponding passwords '''

import subprocess
import re
import platform

print("-------------------- Stored Network Info --------------------\r")

# identify OS
currentOS = platform.system()

# Windows detected
if (currentOS == 'Windows'):

    # retrieve network names
    show_profiles_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

    network_names = []

    for i in show_profiles_output:
        if ('All User Profile' in i):
            network_names.append(i.split(":")[1][1:-1])

    # retrieve corresponding passwords
    for i in network_names:
        key_content_present = False

        network_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')

        for j in network_info:
            if ('Key Content' in j):
                key_content_present = True
                print("{:} -> {:}".format(i, j.split(":")[1][1:-1]))

        if (not key_content_present):
            print("{:} -> {:}".format(i, "FAILED TO RETRIEVE PASSWORD"))

# Mac OS detected
elif(currentOS == 'Darwin'):

    # retrieve network names
    list_networks_output = subprocess.check_output(["networksetup", "-listpreferredwirelessnetworks", "en0"]).decode("utf-8").split('\n')[1:]
    known_networks = [i[1:] for i in list_networks_output][:-1]

    # retrieve corresponding passwords
    for network_name in known_networks:
        try:
            password = subprocess.check_output("security find-generic-password -wa" + network_name, shell=True).decode("utf-8")[:-1]
            print("{:} -> {:}".format(network_name, password))
        except (subprocess.CalledProcessError, IndexError):
            print("{:} -> {:}".format(network_name, "FAILED TO RETRIEVE PASSWORD"))

# Linux detected
elif(currentOS == 'Linux'):

    # retrieve network names
    system_connections = subprocess.check_output("sudo grep -r '^psk=' /etc/NetworkManager/system-connections/", shell=True).split('\n')

    # retrieve corresponding passwords
    for data in system_connections:
        try:
            data = re.findall('/etc/NetworkManager/system-connections/(.*)', data)[0].split(':')
            print("{:} -> {:}".format(data[0], data[1].split('=')[1]))
        except:
            print("UNABLE TO RETRIEVE NETWORK DATA")


# Invalid OS or unable to identify
else:
    print("UNABLE TO IDENTIFY RUNNING OPERATING SYSTEM...")


print("------------------------------------------------------------\r")

# string to hold user's input for program exit
quit_input = ''
while(quit_input != 'q'):
    quit_input = input("Enter q to quit \n")
