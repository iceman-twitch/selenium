"""
Web Scraping Example with Selenium Stealth
Demonstrates extracting data from websites while avoiding detection
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def setup_stealth_driver(headless=False):
    """Setup Chrome driver with stealth settings"""
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
    # Disable logging
    options.add_argument('--log-level=3')
    options.add_argument('--disable-notifications')
    
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    
    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )
    
    return driver


def scrape_quotes():
    """Example: Scrape quotes from a demo website"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("http://quotes.toscrape.com/")
        
        # Wait for quotes to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
        )
        
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        
        scraped_data = []
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
            
            scraped_data.append({
                "quote": text,
                "author": author,
                "tags": tags
            })
        
        print(f"Scraped {len(scraped_data)} quotes")
        print(json.dumps(scraped_data[:3], indent=2))  # Print first 3 quotes
        
        return scraped_data
        
    finally:
        driver.quit()


def scrape_with_pagination():
    """Example: Scrape multiple pages with pagination"""
    driver = setup_stealth_driver()
    
    try:
        all_quotes = []
        page = 1
        max_pages = 3
        
        while page <= max_pages:
            url = f"http://quotes.toscrape.com/page/{page}/"
            driver.get(url)
            
            # Wait for quotes
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
            )
            
            quotes = driver.find_elements(By.CLASS_NAME, "quote")
            
            for quote in quotes:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                all_quotes.append({"text": text, "author": author})
            
            print(f"Scraped page {page}: {len(quotes)} quotes")
            page += 1
            time.sleep(1)  # Be polite
        
        print(f"\nTotal quotes scraped: {len(all_quotes)}")
        return all_quotes
        
    finally:
        driver.quit()


def check_bot_detection():
    """Test if the driver is detected as a bot"""
    driver = setup_stealth_driver()
    
    try:
        # Visit bot detection test sites
        test_sites = [
            "https://bot.sannysoft.com/",
            "https://arh.antoinevastel.com/bots/areyouheadless",
        ]
        
        for site in test_sites:
            print(f"\nTesting: {site}")
            driver.get(site)
            time.sleep(3)
            
            # Take screenshot for manual verification
            screenshot_name = f"bot_test_{test_sites.index(site)}.png"
            driver.save_screenshot(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")
        
    finally:
        driver.quit()


def extract_table_data():
    """Example: Extract data from HTML tables"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.scrapethissite.com/pages/simple/")
        
        # Wait for table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "country"))
        )
        
        countries = driver.find_elements(By.CLASS_NAME, "country")
        
        country_data = []
        for country in countries[:5]:  # First 5 countries
            name = country.find_element(By.CLASS_NAME, "country-name").text
            capital = country.find_element(By.CLASS_NAME, "country-capital").text
            population = country.find_element(By.CLASS_NAME, "country-population").text
            
            country_data.append({
                "name": name.strip(),
                "capital": capital.strip(),
                "population": population.strip()
            })
        
        print("\nCountry Data:")
        print(json.dumps(country_data, indent=2))
        return country_data
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("=== Web Scraping with Selenium Stealth ===\n")
    
    print("1. Basic Quote Scraping:")
    scrape_quotes()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Pagination Scraping:")
    scrape_with_pagination()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Table Data Extraction:")
    extract_table_data()
    
    print("\n" + "="*50 + "\n")
    
    print("4. Bot Detection Test:")
    check_bot_detection()
