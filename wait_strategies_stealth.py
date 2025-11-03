"""
Wait Strategies with Selenium Stealth
Demonstrates different waiting techniques for handling dynamic content
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time


def setup_stealth_driver():
    """Setup Chrome driver with stealth settings"""
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--log-level=3')
    
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )
    
    return driver


def explicit_wait_examples():
    """Demonstrate explicit waits with different conditions"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        wait = WebDriverWait(driver, 10)
        
        # Wait for element to be present
        print("1. Waiting for element presence...")
        try:
            element = wait.until(
                EC.presence_of_element_located((By.ID, "adder"))
            )
            print("✓ Element found")
        except TimeoutException:
            print("✗ Element not found within timeout")
        
        time.sleep(1)
        
        # Wait for element to be clickable
        print("\n2. Waiting for element to be clickable...")
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.ID, "reveal"))
            )
            print("✓ Element is clickable")
            button.click()
        except TimeoutException:
            print("✗ Element not clickable within timeout")
        
        # Wait for element to be visible after click
        print("\n3. Waiting for revealed element...")
        try:
            revealed = wait.until(
                EC.visibility_of_element_located((By.ID, "revealed"))
            )
            print("✓ Revealed element is visible")
            print(f"   Text: {revealed.text}")
        except TimeoutException:
            print("✗ Revealed element not visible within timeout")
        
    finally:
        time.sleep(2)
        driver.quit()


def wait_for_text_conditions():
    """Wait for specific text conditions"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        wait = WebDriverWait(driver, 10)
        
        # Wait for specific text to be present in element
        print("1. Waiting for text in element...")
        try:
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.ID, "adder"),
                    "Add"
                )
            )
            print("✓ Expected text found in element")
        except TimeoutException:
            print("✗ Expected text not found")
        
        # Wait for title to contain text
        print("\n2. Waiting for title...")
        try:
            wait.until(EC.title_contains("Dynamic"))
            print(f"✓ Title contains expected text: {driver.title}")
        except TimeoutException:
            print("✗ Title doesn't contain expected text")
        
    finally:
        time.sleep(2)
        driver.quit()


def wait_for_element_state_changes():
    """Wait for element state changes"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        wait = WebDriverWait(driver, 10)
        
        # Click to reveal element
        reveal_button = wait.until(
            EC.element_to_be_clickable((By.ID, "reveal"))
        )
        
        print("Clicking reveal button...")
        reveal_button.click()
        
        # Wait for element to be visible
        print("1. Waiting for element to become visible...")
        try:
            wait.until(
                EC.visibility_of_element_located((By.ID, "revealed"))
            )
            print("✓ Element is now visible")
        except TimeoutException:
            print("✗ Element didn't become visible")
        
        # Wait for element to be selected (for checkboxes/radio buttons)
        print("\n2. Checking element selection state...")
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        checkbox = driver.find_element(By.ID, "my-check-1")
        checkbox.click()
        
        try:
            wait.until(
                EC.element_to_be_selected(checkbox)
            )
            print("✓ Checkbox is selected")
        except TimeoutException:
            print("✗ Checkbox not selected")
        
    finally:
        time.sleep(2)
        driver.quit()


def implicit_wait_example():
    """Demonstrate implicit waits"""
    driver = setup_stealth_driver()
    
    try:
        # Set implicit wait - applies to all element searches
        driver.implicitly_wait(10)
        
        print("Implicit wait set to 10 seconds")
        
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        # Element searches will automatically wait up to 10 seconds
        try:
            element = driver.find_element(By.ID, "adder")
            print(f"✓ Element found: {element.text}")
        except NoSuchElementException:
            print("✗ Element not found")
        
        # Note: Implicit waits are generally not recommended
        # Explicit waits are more flexible and predictable
        
    finally:
        time.sleep(2)
        driver.quit()


def custom_wait_condition():
    """Create and use custom wait condition"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("http://quotes.toscrape.com")
        
        # Custom condition: wait until minimum number of quotes loaded
        class minimum_elements_present:
            def __init__(self, locator, minimum):
                self.locator = locator
                self.minimum = minimum
            
            def __call__(self, driver):
                elements = driver.find_elements(*self.locator)
                if len(elements) >= self.minimum:
                    return elements
                return False
        
        wait = WebDriverWait(driver, 10)
        
        print("Waiting for at least 5 quotes to load...")
        try:
            quotes = wait.until(
                minimum_elements_present((By.CLASS_NAME, "quote"), 5)
            )
            print(f"✓ Found {len(quotes)} quotes (minimum 5)")
        except TimeoutException:
            print("✗ Minimum quotes not found")
        
    finally:
        time.sleep(2)
        driver.quit()


def wait_with_polling():
    """Wait with custom polling interval"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        # Custom wait with 0.5 second polling interval
        wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        
        print("Waiting with custom polling (0.5s interval)...")
        
        reveal_button = wait.until(
            EC.element_to_be_clickable((By.ID, "reveal"))
        )
        reveal_button.click()
        
        revealed = wait.until(
            EC.visibility_of_element_located((By.ID, "revealed"))
        )
        print(f"✓ Element revealed: {revealed.text}")
        
    finally:
        time.sleep(2)
        driver.quit()


def wait_for_ajax_completion():
    """Wait for AJAX/JavaScript operations to complete"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("http://quotes.toscrape.com")
        
        wait = WebDriverWait(driver, 10)
        
        # Wait for jQuery to load (if page uses jQuery)
        print("1. Waiting for page to be ready...")
        wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✓ Page is ready")
        
        # Wait for specific number of AJAX requests to complete (example)
        print("\n2. Checking for active AJAX requests...")
        
        # Custom wait for jQuery AJAX to complete
        def jquery_inactive(driver):
            try:
                return driver.execute_script("return jQuery.active == 0")
            except:
                return True  # jQuery not present
        
        try:
            wait.until(jquery_inactive)
            print("✓ No active AJAX requests")
        except:
            print("✓ jQuery not present or AJAX complete")
        
    finally:
        time.sleep(2)
        driver.quit()


def wait_for_element_to_disappear():
    """Wait for element to become invisible or removed"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        wait = WebDriverWait(driver, 10)
        
        # Find and click remove button
        try:
            remove_button = wait.until(
                EC.element_to_be_clickable((By.ID, "reveal"))
            )
            
            print("Element present initially")
            
            # In a real scenario, you'd click something that removes an element
            # Here we'll just demonstrate the wait condition
            
            # Wait for element to be invisible
            # wait.until(EC.invisibility_of_element_located((By.ID, "some-element")))
            print("(This would wait for element to disappear)")
            
        except TimeoutException:
            print("Element operation timed out")
        
    finally:
        time.sleep(2)
        driver.quit()


def fluent_wait_example():
    """Demonstrate fluent wait pattern"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        # Fluent wait with custom configuration
        wait = WebDriverWait(
            driver,
            timeout=15,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                TimeoutException
            ]
        )
        
        print("Using fluent wait pattern...")
        
        element = wait.until(
            EC.presence_of_element_located((By.ID, "adder")),
            message="Element was not found within the timeout period"
        )
        
        print(f"✓ Element found: {element.get_attribute('id')}")
        
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    print("=== Wait Strategies with Selenium Stealth ===\n")
    
    print("1. Explicit Wait Examples:")
    explicit_wait_examples()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Wait for Text Conditions:")
    wait_for_text_conditions()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Wait for Element State Changes:")
    wait_for_element_state_changes()
    
    print("\n" + "="*50 + "\n")
    
    print("4. Implicit Wait:")
    implicit_wait_example()
    
    print("\n" + "="*50 + "\n")
    
    print("5. Custom Wait Condition:")
    custom_wait_condition()
    
    print("\n" + "="*50 + "\n")
    
    print("6. Wait with Polling:")
    wait_with_polling()
    
    print("\n" + "="*50 + "\n")
    
    print("7. Wait for AJAX:")
    wait_for_ajax_completion()
    
    print("\n" + "="*50 + "\n")
    
    print("8. Fluent Wait:")
    fluent_wait_example()
