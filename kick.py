from selenium import webdriver
from selenium_stealth import stealth
import time

options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor = "Intel Inc.",
        renderer = "Intel Iris OpenGL Engine",
        fix_hairline = False,
        run_on_insecure_origins = False,
)

# url = "https://bot.sannysoft.com/"
url = "https://kick.com/theicyman"
driver.get(url)
while True:
    a = 1