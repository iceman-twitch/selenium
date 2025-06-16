import json
import deathbycaptcha
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


USERNAME = 'DBC_USERNAME'   # Your DBC username here
PASSWORD = 'DBC_PASSWORD'   # Your DBC password here
CAPTCHA_URL = 'https://www.google.com/recaptcha/api2/demo'


def solve_captcha(captcha: dict):
    json_captcha = json.dumps(captcha)
    client = deathbycaptcha.SocketClient(USERNAME, PASSWORD)

    try:
        # First let's check our balance (not needed though)
        balance = client.get_balance()
        print('Balance: %s' % balance)

        print('Solving captcha...')
        client.is_verbose = True
        result = client.decode(type=4, token_params=json_captcha)

        return result.get('text')

    except Exception as e:
        print(e)
        return None


def main():
    with webdriver.Firefox() as driver:  #using firefox
    # with webdriver.Chrome() as driver:  #using Chrome
        driver.get(CAPTCHA_URL)

        try:
            element: WebElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "recaptcha-demo"))
            )
        except:
            print('Not found')
            return

        googlekey = element.get_dom_attribute('data-sitekey')
        print('GoogleKey: %s' % googlekey)

        captcha = {     # not using proxy in this example
            'googlekey': googlekey,
            'pageurl': CAPTCHA_URL}

        solution = solve_captcha(captcha)
        if not solution:
            print('No captcha solution (maybe implement retry)...closing')
            return

        print('Solution: %s' % solution)
        driver.execute_script(
            "document.getElementById('g-recaptcha-response').value='%s'" % solution
        )

        # Click on Check button
        check_button = driver.find_element(By.ID, 'recaptcha-demo-submit')
        check_button.click()

        # Check if success
        try:
            success_element = driver.find_element(By.CLASS_NAME, "recaptcha-success")
            print(success_element.text)
        except NoSuchElementException as e:
            print("Success message not found: %s" % str(e))


if __name__ == '__main__':
    main()
