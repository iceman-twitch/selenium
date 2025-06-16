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
import json

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

# Perform some actions that set cookies (e.g., login)
dosleep()

if exist('/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]',driver):
    a = 0
else:
    dosleep()
    driver.close()
    exit(0)

driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]').click()
dosleep()
driver.get('https://help.instagram.com/contact/723586364339719')
dosleep()

# Get the cookies
cookies = driver.get_cookies()


# Save the cookies to a file
with open("cookies.json", "w") as f:
    json.dump(cookies, f)

dosleep()
driver.close()
dosleep()
driver = webdriver.Chrome(options=options)
dosleep()
# Load the cookies from the file
with open("cookies.json", "r") as f:
    cookies = json.load(f)
dosleep()
driver.get('https://help.instagram.com/contact/723586364339719')
dosleep()
# Add the cookies to the driver
for cookie in cookies:
    # print(cookie)
    # if cookie['domain'] != 'instagram.com':
        # cookie['domain'] = 'www.instagram.com'
    driver.add_cookie(cookie)
dosleep()
driver.get('https://help.instagram.com/contact/723586364339719')
dosleep()
# Save the cookies to a file
with open("cookies.json", "w") as f:
    json.dump(cookies, f)

dosleep()
driver.close()
dosleep()