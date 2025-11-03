"""
Screenshot and PDF Generation with Selenium Stealth
Demonstrates taking screenshots, generating PDFs, and saving page content
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import base64
import json


def setup_stealth_driver(headless=False):
    """Setup Chrome driver with stealth settings"""
    options = webdriver.ChromeOptions()
    
    if not headless:
        options.add_argument("start-maximized")
    else:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--log-level=3')
    
    # Enable downloads in headless mode
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True
    })
    
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


def take_full_page_screenshot():
    """Take a full-page screenshot"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://example.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)
        
        # Get page dimensions
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        print(f"Page height: {total_height}px")
        print(f"Viewport height: {viewport_height}px")
        
        # Take full page screenshot
        screenshot_path = "full_page_screenshot.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"Screenshot saved: {screenshot_path}")
        
        return screenshot_path
        
    finally:
        driver.quit()


def take_element_screenshot():
    """Take screenshot of specific element"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://example.com")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Find specific element
        element = driver.find_element(By.TAG_NAME, "h1")
        
        # Take screenshot of element only
        screenshot_path = "element_screenshot.png"
        element.screenshot(screenshot_path)
        
        print(f"Element screenshot saved: {screenshot_path}")
        
        return screenshot_path
        
    finally:
        driver.quit()


def take_screenshots_at_different_resolutions():
    """Take screenshots at various screen sizes"""
    driver = setup_stealth_driver(headless=True)
    
    resolutions = [
        (1920, 1080, "desktop"),
        (768, 1024, "tablet"),
        (375, 667, "mobile")
    ]
    
    try:
        driver.get("https://example.com")
        
        for width, height, device in resolutions:
            driver.set_window_size(width, height)
            time.sleep(1)
            
            screenshot_path = f"screenshot_{device}_{width}x{height}.png"
            driver.save_screenshot(screenshot_path)
            
            print(f"Screenshot saved for {device}: {screenshot_path}")
        
    finally:
        driver.quit()


def generate_pdf_from_page():
    """Generate PDF from webpage"""
    driver = setup_stealth_driver(headless=True)
    
    try:
        driver.get("https://example.com")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)
        
        # Use Chrome's print to PDF feature
        pdf_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        
        result = driver.execute_cdp_cmd("Page.printToPDF", pdf_options)
        
        # Save PDF
        pdf_path = "webpage.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(base64.b64decode(result['data']))
        
        print(f"PDF saved: {pdf_path}")
        
        return pdf_path
        
    finally:
        driver.quit()


def capture_page_content():
    """Capture and save page HTML and text content"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://example.com")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get page source (HTML)
        page_source = driver.page_source
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("HTML saved: page_source.html")
        
        # Get visible text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        with open("page_text.txt", "w", encoding="utf-8") as f:
            f.write(body_text)
        print("Text content saved: page_text.txt")
        
        # Get page title and URL
        metadata = {
            "title": driver.title,
            "url": driver.current_url,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("page_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print("Metadata saved: page_metadata.json")
        
    finally:
        driver.quit()


def take_screenshot_after_scroll():
    """Take screenshots while scrolling through page"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("http://quotes.toscrape.com")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get total height
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        scroll_position = 0
        screenshot_count = 0
        
        while scroll_position < total_height:
            # Take screenshot at current position
            screenshot_path = f"scroll_screenshot_{screenshot_count}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot taken at scroll position {scroll_position}: {screenshot_path}")
            
            # Scroll down
            scroll_position += viewport_height
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(1)
            
            screenshot_count += 1
            
            # Safety limit
            if screenshot_count > 10:
                break
        
        print(f"Total screenshots taken: {screenshot_count}")
        
    finally:
        driver.quit()


def capture_before_after_action():
    """Take screenshots before and after an action"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        
        time.sleep(2)
        
        # Take 'before' screenshot
        driver.save_screenshot("before_action.png")
        print("Before screenshot saved")
        
        # Perform action (click button)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "reveal"))
            )
            button.click()
            
            # Wait for change
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "revealed"))
            )
            
            time.sleep(1)
            
            # Take 'after' screenshot
            driver.save_screenshot("after_action.png")
            print("After screenshot saved")
            
        except Exception as e:
            print(f"Action failed: {e}")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("=== Screenshot and PDF Generation with Selenium Stealth ===\n")
    
    print("1. Full Page Screenshot:")
    take_full_page_screenshot()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Element Screenshot:")
    take_element_screenshot()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Multiple Resolutions:")
    take_screenshots_at_different_resolutions()
    
    print("\n" + "="*50 + "\n")
    
    print("4. PDF Generation:")
    generate_pdf_from_page()
    
    print("\n" + "="*50 + "\n")
    
    print("5. Page Content Capture:")
    capture_page_content()
    
    print("\n" + "="*50 + "\n")
    
    print("6. Scroll Screenshots:")
    take_screenshot_after_scroll()
    
    print("\n" + "="*50 + "\n")
    
    print("7. Before/After Screenshots:")
    capture_before_after_action()
