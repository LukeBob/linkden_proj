# Author: Luke
#
# Written for python 3+

import os
import re
from selenium import webdriver 
import selenium
import time
import parsel
from bs4 import BeautifulSoup
import subprocess
import sys

v = False

target_dict = {}

healp = """
usage: linkdeen [options]

example: linkdeen -v   -- this will run linkdeen in verbose mode
example: linkdeen -h   -- print this help screen
"""

try:
    if sys.argv[1] == "-v":
        v = True

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(healp)
        exit()
except:
    pass

banner = """
$$\      $$\         $$\             $$$$$$$\                        
$$ |     \__|        $$ |            $$  __$$\                       
$$ |     $$\$$$$$$$\ $$ |  $$\       $$ |  $$ $$\  $$\  $$\$$$$$$$\  
$$ |     $$ $$  __$$\$$ | $$  |      $$$$$$$  $$ | $$ | $$ $$  __$$\ 
$$ |     $$ $$ |  $$ $$$$$$  /       $$  ____/$$ | $$ | $$ $$ |  $$ |
$$ |     $$ $$ |  $$ $$  _$$<        $$ |     $$ | $$ | $$ $$ |  $$ |
$$$$$$$$\$$ $$ |  $$ $$ | \$$\       $$ |     \$$$$$\$$$$  $$ |  $$ |
\________\__\__|  \__\__|  \__|      \__|      \_____\____/\__|  \__| Author: Luke_bob
                                                                      Github: https://github.com/LukeBob


"""

print(banner)

# Name of csv file to write to. (name it anything)
file_name = 'link.csv'

#linkedin username
user = input('Email/Username: ')

#linkedin password
passwd = input('Pass: ')

# define writer object for writing data to csv
#writer = csv.writer(open(file_name, 'w'))

#writer.writerow(['Name', 'Job Title', 'Company', 'Collage', 'Location', 'Url'])
if v:
    print('[v]Creating new webdriver...')
# specifies the path to the chromedriver.exe

if os.name == 'nt':
    try:
        driver = webdriver.Chrome()
    except selenium.common.exceptions.WebDriverException:
        print("\n[#] Error: Make sure Chrome is installed and up to date!\n")
        

# makes request to linkenin through selenium
if v:
    print('[v] Connecting to linkden.com...')
driver.get('https://www.linkedin.com') 

#define username element
username = driver.find_element_by_name('session_key')

#define password element 
password = driver.find_element_by_name('session_password')

#define log-in button
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

#send username through selenium
username.send_keys(str(user))

#send password through selenium
password.send_keys(str(passwd))

#try to log-in
if v:
    print('[v] Trying login with details {0} -- {1}'.format(user, passwd))
    time.sleep(2)
log_in_button.click()

data = input("Press Enter To Continue...")
#navigate to connections page 

if v:
    print('[v] Navigating to MEMBER_PROFILE_CANNED_SEARCH...')
    time.sleep(2)

driver.get('https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH')

connection_list = driver.find_elements_by_class_name('search-result__result-link.ember-view')

link_list = []
new_l_list = []

for i in connection_list:
    link_list.append(i.get_attribute('href'))

link_list = list(dict.fromkeys(link_list))   


for i in link_list:
    i = i.replace("\n", "")
    i = i.replace(" ", "")
    if v:
        print("[v] Found contact -- {}".format(i))
    time.sleep(1)
    driver.get('{}detail/contact-info/'.format(i))
    details = driver.find_elements_by_class_name("pv-contact-info__contact-link")
    for a in details:
        if a.get_attribute('href') != i[:-1]:
            x = re.search("mailto", a.get_attribute('href'))
            if not x:
                if v:
                    print('[v] Found company site -- '+a.get_attribute('href'))
                #print("Scanning host "+a.get_attribute('href'))
                
                target_dict[i] = a.get_attribute('href')
                #new_l_list.append(a.get_attribute('href'))
                #subprocess.run(["wpscan", "--url", a.get_attribute('href')])
                print("\n[#] Processing Results...\n")
                time.sleep(3)
                
driver.close()
                      
for i in target_dict:
    print("[#]Found Company Site: {} -- {}".format(i, target_dict[i]))
    #subprocess.run(["wpscan", "--url", i])