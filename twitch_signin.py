from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth
from amazoncaptcha import AmazonCaptcha
from python3_anticaptcha import ImageToTextTask
import time


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless")
options.add_argument("--disable-infobars")
# options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument('log-level=3')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0')

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)

driver.get("https://ident.me")
# print(driver.find_element(By.XPATH, "/html/body").text)


def check_exists_by_xpath( driver, xpath ):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    
def SelectByValue( self, xpath, value ):
    if check_exists_by_xpath( driver, xpath ):
        click = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        click = Select( click )
        click.select_by_value( value )
        print( 'Selected value to: ' + value )
    time.sleep( 1 )
    
def SendKeys( driver, xpath, value ):
    if check_exists_by_xpath( driver, xpath ):
        click = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        click.click()
        time.sleep(0.1) # wait because human not a robot
        click.send_keys( value ) # send keys to simulate keyboard
        print( 'Sent keys to: ' + value )
    time.sleep( 1 )
        
def Click( driver, xpath ):
    if check_exists_by_xpath( driver, xpath ):
        click = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        time.sleep(0.1) # wait because human not a robot
        click.click()
        print( 'Clicked element' )
    time.sleep( 1 )

def CheckCaptcha( driver ):
    captcha_image = '//*[@id="auth-captcha-image"]'
    input_auth = '//*[@id="auth-captcha-guess"]'
    if "Enter the characters you see" in driver.find_element(By.XPATH, "/html/body").text:
        link = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, captcha_image))).get_attribute("src")
        captcha = AmazonCaptcha.fromlink(link)
        solution = captcha.solve()
        print(link)
        SendKeys( driver, input_auth, solution )
        return True
    return False

def SignIn( driver ):
    driver.get( "https://www.twitch.tv/login" )
    click = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div[3]/button')))
    click.send_keys(Keys.RETURN)
    Click( driver, '/html/body/div[1]/div/div[1]/div/div/div/div[3]/button' )
    Click( driver, '/html/body/div[1]/div/div[1]/div/div/div/div[3]/button' )
    
    SendKeys( driver, '//*[@id="login-username"]', 'username' )
    SendKeys( driver, '//*[@id="password-input"]', 'password' )
    Click( driver, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[3]/form/div/div[3]/div/button' )
    
time.sleep(2)
SignIn( driver )
time.sleep( 300 )

driver.close()
