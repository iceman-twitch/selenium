"""
Form Automation Example with Selenium Stealth
Demonstrates filling forms, handling dropdowns, checkboxes, and file uploads
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


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


def fill_basic_form():
    """Example: Fill a basic contact form"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        # Wait for form to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "my-text-id"))
        )
        
        # Fill text input
        text_input = driver.find_element(By.ID, "my-text-id")
        text_input.send_keys("John Doe")
        
        # Fill password
        password_input = driver.find_element(By.NAME, "my-password")
        password_input.send_keys("SecurePassword123")
        
        # Fill textarea
        textarea = driver.find_element(By.NAME, "my-textarea")
        textarea.send_keys("This is a test message for the form automation.")
        
        # Select dropdown option
        dropdown = Select(driver.find_element(By.NAME, "my-select"))
        dropdown.select_by_visible_text("Two")
        
        # Click checkbox
        checkbox = driver.find_element(By.ID, "my-check-2")
        if not checkbox.is_selected():
            checkbox.click()
        
        # Click radio button
        radio = driver.find_element(By.ID, "my-radio-2")
        radio.click()
        
        time.sleep(1)
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for success message or redirect
        time.sleep(2)
        
        print("Form submitted successfully!")
        print(f"Current URL: {driver.current_url}")
        
    finally:
        time.sleep(2)
        driver.quit()


def fill_form_with_delays():
    """Example: Fill form with human-like delays"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "my-text-id"))
        )
        
        # Simulate human typing with delays
        text_input = driver.find_element(By.ID, "my-text-id")
        name = "Jane Smith"
        
        for char in name:
            text_input.send_keys(char)
            time.sleep(0.1)  # Delay between keystrokes
        
        time.sleep(0.5)
        
        # Fill other fields with pauses
        password_input = driver.find_element(By.NAME, "my-password")
        password_input.send_keys("MyPassword")
        
        time.sleep(0.8)
        
        # Select from dropdown
        dropdown = Select(driver.find_element(By.NAME, "my-select"))
        dropdown.select_by_index(2)
        
        time.sleep(0.5)
        
        print("Form filled with human-like timing")
        
    finally:
        time.sleep(2)
        driver.quit()


def handle_multi_step_form():
    """Example: Handle multi-step form with navigation"""
    driver = setup_stealth_driver()
    
    try:
        # Using a demo multi-step form site
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "my-text-id"))
        )
        
        # Step 1: Personal Information
        print("Step 1: Filling personal information...")
        text_input = driver.find_element(By.ID, "my-text-id")
        text_input.send_keys("Alice Johnson")
        
        password = driver.find_element(By.NAME, "my-password")
        password.send_keys("StrongPass123")
        
        time.sleep(1)
        
        # Step 2: Additional details
        print("Step 2: Filling additional details...")
        textarea = driver.find_element(By.NAME, "my-textarea")
        textarea.send_keys("Additional information goes here.")
        
        dropdown = Select(driver.find_element(By.NAME, "my-select"))
        dropdown.select_by_value("2")
        
        time.sleep(1)
        
        # Step 3: Preferences
        print("Step 3: Setting preferences...")
        checkbox = driver.find_element(By.ID, "my-check-1")
        checkbox.click()
        
        radio = driver.find_element(By.ID, "my-radio-1")
        radio.click()
        
        print("Multi-step form completed!")
        
    finally:
        time.sleep(2)
        driver.quit()


def handle_dynamic_form():
    """Example: Handle forms with dynamic elements"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        # Wait for page to load
        time.sleep(2)
        
        # Click button to reveal new elements
        try:
            reveal_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "reveal"))
            )
            reveal_button.click()
            
            # Wait for revealed input to appear
            revealed_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "revealed"))
            )
            
            revealed_input.send_keys("Dynamic content loaded!")
            print("Successfully interacted with dynamic element")
            
        except Exception as e:
            print(f"Dynamic element handling: {e}")
        
    finally:
        time.sleep(2)
        driver.quit()


def fill_form_with_validation():
    """Example: Fill form with validation checking"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "my-text-id"))
        )
        
        # Test required field validation
        text_input = driver.find_element(By.ID, "my-text-id")
        
        # Clear and check if required
        text_input.clear()
        is_required = text_input.get_attribute("required")
        print(f"Field is required: {is_required is not None}")
        
        # Fill with valid data
        text_input.send_keys("Valid Name")
        
        # Validate password strength (example)
        password_input = driver.find_element(By.NAME, "my-password")
        test_password = "Weak"
        password_input.send_keys(test_password)
        
        print(f"Password length: {len(test_password)}")
        
        if len(test_password) < 8:
            print("Warning: Password too short")
            password_input.clear()
            password_input.send_keys("StrongPassword123")
        
        print("Form validation completed")
        
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    print("=== Form Automation with Selenium Stealth ===\n")
    
    print("1. Basic Form Fill:")
    fill_basic_form()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Human-like Form Fill:")
    fill_form_with_delays()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Multi-step Form:")
    handle_multi_step_form()
    
    print("\n" + "="*50 + "\n")
    
    print("4. Dynamic Form:")
    handle_dynamic_form()
    
    print("\n" + "="*50 + "\n")
    
    print("5. Form with Validation:")
    fill_form_with_validation()
