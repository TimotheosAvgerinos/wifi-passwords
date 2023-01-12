#  This program shows all the passwond of the Wifi network that this PC is conected with. The operation system must be Windows 


import subprocess

import re

# we use system commands using the subprocess module

# we specify that we want to capture the output (capture_output = True) 
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()  

# we find all the wifi names which are listed after the "All User Profile     :.
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#Empty list where dictionaries containing all the wifi usernames and passwords
wifi_list = []

# we check if there are wifi conections with networks
if len(profile_names) != 0 :
    
    for name in profile_names:
        # we append every wifi conection to the wifi_list as a dictionary 
        wifi_profile = {}

        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()

        # we look for the absent cases so we can ignore them
        if re.search("Key Content            : (.*)\r", profile_info):

            continue

        else:
            # assign the ssid of the wifi profile to the dictionary
            wifi_profile["ssid"] = name

            # we run the "key=clear" command part to get the passwor
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()

            # we capture the group after the :(which is the password)
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            # some wifi connections may not have passwords
            if password == None:

                wifi_profile["password"] = None

            else:

                wifi_profile["password"] = password[1]
            
            wifi_list.append(wifi_profile)

for i in range(len(wifi_list)):
    print(wifi_list[i])

