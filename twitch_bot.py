import time
import requests
import random 
import string
import re
import sys
import os, platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
global twitch_url
global proxy_mode
twitch_url = 'https://twitch.tv/'
proxy_mode = 0

def get_useragent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()
def check_proxy(proxy):
    code=404
    try:
        proxydict = {
            'https': proxy,
            'http': proxy
        }
        r =requests.get("https://twitch.tv/theicyman",proxies=proxydict)
        
        print(r.status_code)
        code=r.status_code
    except Exception as e:
        print("ERROR:" + str(e))
        if code == 404:
            return False
        else:
            return True
    
    if code == 404:
        return False
    else:
        return True

def get_proxy():
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open( cwd + "\proxy.txt" ) as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    while True:
        proxy = lines[random.randint(0,len(lines)-2)]
        if check_proxy(proxy):
            return proxy


    # return lines[random.randint(0,len(lines)-2)]

def chrome():
    options = Options()
    # proxy = get_proxy()
    # ua = get_useragent()
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
    # print(proxy)
    options.add_argument( "user-agent=" + ua )
    # options.add_argument( f'--proxy-server={ proxy }' )

    # options = {'proxy':{'http':proxy, 'https':proxy, 'no_proxy':'localhost,127.0.0.1,dev_server:8080'}}
    chromepath = 'chromedriver.exe'
    # chromepath = chromepath.replace("\\","/")
    # options.add_argument('--headless') 
    options.add_argument("--mute-audio")    
    driver = webdriver.Chrome(executable_path = chromepath, options = options)
    # driver = webdriver.Chrome(executable_path = chromepath)
    driver.implicitly_wait(55)
    driver.set_page_load_timeout(55)
    return driver

def twitchbot():
    driver = chrome()
    while True:
        time.sleep(random.randint(1,3))
        reached = False
        try:
            driver.get( twitch_url )
            reached = True
        except:
            reached = False
        if reached:
            time.sleep(random.randint(55,60))



if sys.argv[1:]:
    twitch_url = str( sys.argv[1:][0] )
    if sys.argv[1:][1]:
        proxy_mode = int( sys.argv[1:][1] )
        
    twitchbot()

# twitchbot()