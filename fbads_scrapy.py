import concurrent.futures
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import random
import time
import json

# Configuration
MAX_WORKERS = 3  # Number of parallel browsers
MAX_ADS_PER_PROXY = 15
SEARCH_TERM = ""
COUNTRY_CODE = ""
HEADLESS_MODE = True  # Set to False for debugging

# User-Agents (Modern browsers)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

def get_proxies():
    proxy_url = "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=500&anonymity=elite"
    try:
        response = requests.get(proxy_url, timeout=10)
        proxies = [p.strip() for p in response.text.split('\r\n') if p.strip()]
        return list(set(proxies))[:MAX_WORKERS]  # Unique proxies only
    except Exception as e:
        print(f"Proxy fetch error: {e}")
        return []

def init_driver(proxy):
    chrome_options = Options()
    
    # Headless configuration
    if HEADLESS_MODE:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
    
    # Proxy settings
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    
    # Random User-Agent
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Stealth settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Additional headless precautions
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    
    # Apply stealth (even in headless)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    
    return driver

def human_interaction(driver):
    time.sleep(random.uniform(1.0, 3.0))
    # Scroll in headless needs different handling
    if HEADLESS_MODE:
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_pos = random.randint(300, min(800, scroll_height))
        driver.execute_script(f"window.scrollTo(0, {scroll_pos})")
    else:
        driver.execute_script(f"window.scrollBy(0, {random.randint(200, 500)})")
    time.sleep(random.uniform(0.5, 1.5))

def scrape_with_proxy(proxy):
    driver = None
    try:
        driver = init_driver(proxy)
        print(f"Started scraping with {proxy} (Headless: {HEADLESS_MODE})")
        
        url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={COUNTRY_CODE}&q={SEARCH_TERM}"
        driver.get(url)
        human_interaction(driver)
        
        ads_data = []
        scroll_attempts = 0
        
        while len(ads_data) < MAX_ADS_PER_PROXY and scroll_attempts < 5:
            try:
                # Wait for either ads or timeout
                WebDriverWait(driver, 15).until(
                    lambda d: d.find_elements(By.XPATH, '//div[contains(@class, "_7jyr")]') or 
                    "Checking your browser" in d.page_source
                )
                
                # Check for Cloudflare challenge
                if "Checking your browser" in driver.page_source:
                    print(f"Proxy {proxy} triggered Cloudflare")
                    break
                
                ad_cards = driver.find_elements(By.XPATH, '//div[contains(@class, "_7jyr")]')
                
                for ad in ad_cards[len(ads_data):]:
                    try:
                        ad_data = {
                            'advertiser': ad.find_element(By.XPATH, './/div[contains(@class, "_7jwu")]').text,
                            'text': ad.find_element(By.XPATH, './/div[contains(@class, "_7jyu")]').text,
                            'media': [img.get_attribute('src') for img in ad.find_elements(By.TAG_NAME, 'img')],
                            'sponsor': ad.find_element(By.XPATH, './/div[contains(@class, "_7jys")]').text,
                            'proxy': proxy,
                            'timestamp': int(time.time())
                        }
                        ads_data.append(ad_data)
                    except Exception as e:
                        continue
                
                human_interaction(driver)
                scroll_attempts += 1
                
            except Exception as e:
                print(f"Proxy {proxy} error: {str(e)[:100]}")
                if HEADLESS_MODE:
                    # Save screenshot for debugging
                    driver.save_screenshot(f"error_{proxy.replace(':', '_')}.png")
                break
        
        return ads_data[:MAX_ADS_PER_PROXY]
    
    except Exception as e:
        print(f"Proxy {proxy} failed: {str(e)[:100]}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    proxies = get_proxies()
    if not proxies:
        print("No proxies available")
        exit()
    
    print(f"Starting parallel scraping (Headless: {HEADLESS_MODE}) with {len(proxies)} proxies...")
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(scrape_with_proxy, proxies))
    
    # Combine results
    all_ads = [ad for proxy_ads in results for ad in proxy_ads]
    print(f"Total ads collected: {len(all_ads)} in {time.time()-start_time:.2f} seconds")
    
    # Save with timestamp
    filename = f'fb_ads_{SEARCH_TERM}_{int(time.time())}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {filename}")
