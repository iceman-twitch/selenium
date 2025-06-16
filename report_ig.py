import os
import time
from colorama import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth
import random
init()

logo = """
                      _____ _____   _____                       _     _______          _ 
                     |_   _/ ____| |  __ \                     | |   |__   __|        | |
                       | || |  __  | |__) |___ _ __   ___  _ __| |_     | | ___   ___ | |
                       | || | |_ | |  _  // _ \ '_ \ / _ \| '__| __|    | |/ _ \ / _ \| |
                      _| || |__| | | | \ \  __/ |_) | (_) | |  | |_     | | (_) | (_) | |
                     |_____\_____| |_|  \_\___| .__/ \___/|_|   \__|    |_|\___/ \___/|_|
                                              | |                                        
                                              |_|                                        

"""
# Decline All Option Cookies
# //*[@id="u_0_n_vZ"] 
# /html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]
# Username
# //*[@id="258021274378282"]
# Fullname
# //*[@id="735407019826414"]
# Year
# //*[@id="js_mj"]
# Month
# /html/body/div[1]/div/div[3]/div/div[2]/div/form/div[3]/div[2]/div/div[2]/div/a
# Day
# /html/body/div[1]/div/div[3]/div/div[2]/div/form/div[3]/div[2]/div/div[3]/div/a
# Relationship to person
# //*[@id="294540267362199"]
# Your Email Address
# //*[@id="843437906537050"]
# Send
# //*[@id="u_0_8_H4"]
def dosleep():
    time.sleep(min(random.expovariate(0.6), 3.0))
def exist(x,driver):
    value = False
    try:
        driver.find_element(By.XPATH,x)
        value = True
    except NoSuchElementException:
        print("Element not found")
    return value
def sendkey(x,driver,txt):
    value = False
def main(username, full_name, wait_):
    times_reported = 0
    while True:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument("--headless")
        options.add_argument("--disable-infobars")
        # options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument('log-level=3')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )
        dosleep()
        
        driver.get('https://help.instagram.com/contact/723586364339719')
        dosleep()
        if exist('/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]',driver):
            a = 0
        else:
            dosleep()
            driver.close()
            continue
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]').click()
        print('Click Decline All Optional Cookies')
        dosleep()
        driver.find_element(By.XPATH,'//input[@name="Field258021274378282"]').send_keys(username)
        print('Typing Username: ' + username)
        dosleep()
        driver.find_element(By.XPATH,'//input[@name="Field735407019826414"]').send_keys(full_name)
        print('Typing FullName: ' +full_name)
        dosleep()
        # Year
        driver.find_element(By.XPATH,'//span[@class="_55pe"]').click()
        dosleep()
        driver.find_element(By.XPATH,'//ul[@class="_54nf"]//a[@title="2013"]').click()
        dosleep()
        # Month
        driver.find_element(By.XPATH,'//a[@class="_p _55pi _5vto _55_p _2agf _4o_4 _4jy0 _4jy3 _517h _51sy _42ft"]//span[@class="_55pe"]').click()
        dosleep()
        driver.find_element(By.XPATH,'//a[@title="February"]//span[@class="_54nh"]').click()
        dosleep()
        # Day
        driver.find_element(By.XPATH,'//a[@class="_p _55pi _5vto _55_p _2agf _4o_4 _4jy0 _4jy3 _517h _51sy _42ft"]//span[@class="_55pe"]').click()
        dosleep()
        driver.find_element(By.XPATH,'//a[@title="9"]//span[@class="_54nh"]').click()
        dosleep()
        # Relation ship to Person
        driver.find_element(By.XPATH,'//select[@id="294540267362199"]//option[@value="Other"]').click()
        dosleep()
        # Your Email Address
        email = str(times_reported) 
        driver.find_element(By.XPATH,'//*[@id="843437906537050"]').send_keys(email)
        dosleep()
        # Send
        driver.find_element(By.XPATH,'//button[@class="_42ft _4jy0 _4jy4 _4jy1 selected _51sy"]').click()
        time.sleep(4)
        driver.close()
        times_reported += 1
        print(Fore.LIGHTBLUE_EX + f'Reported {Fore.LIGHTGREEN_EX}{times_reported}{Fore.LIGHTBLUE_EX} Time/s' + Fore.RESET)
        time.sleep(wait_)
        

def info():
    os.system('cls')
    print(Fore.LIGHTGREEN_EX + logo + Fore.RESET)
    username = input(Fore.LIGHTBLUE_EX + 'Username: @' + Fore.LIGHTGREEN_EX)
    full_name = input(Fore.LIGHTBLUE_EX + 'Full Name: ' + Fore.LIGHTGREEN_EX)
    wait_ = int(input(Fore.LIGHTBLUE_EX + 'Time to wait before the next report: ' + Fore.LIGHTGREEN_EX))
    main(username, full_name, wait_)
    

print(Fore.LIGHTGREEN_EX + logo + Fore.RESET)
info()