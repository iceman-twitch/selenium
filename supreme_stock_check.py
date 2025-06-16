from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from windows_toasts import WindowsToaster, ToastText1

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument("--disable-infobars")
# options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument('log-level=3')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

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

driver.get("https://eu.supreme.com/products/evtprddlyebvjmqy?variant=42719354028236")
# print(driver.find_element(By.XPATH, "/html/body").text)

def Check_Stock( driver ):
    
    while driver.title != "":
        a = driver.find_element(By.XPATH, "/html/body").text
        
        if "Please try again in a couple minutes by refreshing the page" in a:
            print( "Temporary Disabled" )
        else:
            if "sold out" in a:
                print( "STOCK OUT :(" )
            else:
                wintoaster = WindowsToaster('Supreme STOCK IN GO BUY IT')
                newToast = ToastText1()
                newToast.SetBody('Supreme STOCK IN GO BUY IT')
                newToast.on_activated = lambda _: print('GO SUPREME NOW')
                wintoaster.show_toast(newToast)
            
        time.sleep(39)
        driver.refresh()
        
Check_Stock( driver )
driver.close()
time.sleep(10)