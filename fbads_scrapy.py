import concurrent.futures
import asyncio
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
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import sys

# Configuration
MAX_WORKERS = 5  # Number of parallel browsers
MAX_ADS_PER_PROXY = 20
SEARCH_TERM = ""  # Leave empty to scrape all recent ads
COUNTRY_CODE = ""  # Leave empty to search all countries
HEADLESS_MODE = True  # Set to False for debugging
SCROLL_ATTEMPTS = 10  # How many times to scroll for more ads
LOG_DIR = Path("logs")
OUTPUT_DIR = Path("output")

# Create directories
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Logging setup
log_filename = LOG_DIR / f"fbads_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# User-Agents (Modern browsers)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# Statistics tracker
class ScraperStats:
    def __init__(self):
        self.total_ads = 0
        self.successful_proxies = 0
        self.failed_proxies = 0
        self.cloudflare_blocks = 0
        self.start_time = time.time()
        self.proxy_results = {}
    
    def add_result(self, proxy: str, ads_count: int, status: str):
        self.proxy_results[proxy] = {'ads': ads_count, 'status': status}
        if status == 'success':
            self.successful_proxies += 1
            self.total_ads += ads_count
        elif status == 'cloudflare':
            self.cloudflare_blocks += 1
            self.failed_proxies += 1
        else:
            self.failed_proxies += 1
    
    def get_summary(self) -> str:
        duration = time.time() - self.start_time
        return f"""
╔═══════════════════════════════════════════════════════════╗
║              FACEBOOK ADS SCRAPER - SUMMARY               ║
╠═══════════════════════════════════════════════════════════╣
║ Total Ads Collected: {self.total_ads:>35} ║
║ Successful Proxies:  {self.successful_proxies:>35} ║
║ Failed Proxies:      {self.failed_proxies:>35} ║
║ Cloudflare Blocks:   {self.cloudflare_blocks:>35} ║
║ Duration:            {duration:>32.2f}s ║
╚═══════════════════════════════════════════════════════════╝
"""

stats = ScraperStats()


def get_proxies() -> List[str]:
    """Fetch free proxies from multiple sources."""
    all_proxies = []
    
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    
    for source in sources:
        try:
            logger.info(f"Fetching proxies from: {source}")
            response = requests.get(source, timeout=10)
            proxies = [p.strip() for p in response.text.split('\n') if p.strip() and ':' in p]
            all_proxies.extend(proxies)
            logger.info(f"Fetched {len(proxies)} proxies from source")
        except Exception as e:
            logger.warning(f"Failed to fetch from {source}: {e}")
    
    # Remove duplicates and limit
    unique_proxies = list(set(all_proxies))
    logger.info(f"Total unique proxies: {len(unique_proxies)}")
    return unique_proxies[:MAX_WORKERS * 2]  # Get extra in case some fail

def test_proxy(proxy: str) -> bool:
    """Test if proxy is working."""
    try:
        response = requests.get(
            "https://www.facebook.com",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=10
        )
        return response.status_code in [200, 301, 302, 403]
    except:
        return False



def init_driver(proxy: str) -> webdriver.Chrome:
    """Initialize Chrome driver with stealth settings."""
    chrome_options = Options()
    
    # Headless configuration
    if HEADLESS_MODE:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
    
    # Proxy settings
    if proxy:
        chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    
    # Random User-Agent
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Stealth settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Performance settings
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    
    # Memory optimization
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-web-security")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Apply stealth
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)
        
        logger.debug(f"Driver initialized with proxy: {proxy}")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize driver: {e}")
        raise



def human_interaction(driver: webdriver.Chrome):
    """Simulate human-like browsing behavior."""
    time.sleep(random.uniform(1.5, 3.5))
    
    # Random scroll
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_positions = [random.randint(200, min(1000, scroll_height)) for _ in range(3)]
    
    for pos in scroll_positions:
        driver.execute_script(f"window.scrollTo({{top: {pos}, behavior: 'smooth'}})")
        time.sleep(random.uniform(0.5, 1.2))
    
    # Random mouse movements (via JavaScript)
    driver.execute_script("""
        var event = new MouseEvent('mousemove', {
            'view': window,
            'bubbles': true,
            'cancelable': true,
            'clientX': Math.random() * window.innerWidth,
            'clientY': Math.random() * window.innerHeight
        });
        document.dispatchEvent(event);
    """)
    
    time.sleep(random.uniform(0.8, 2.0))

def extract_ad_data(ad_element, proxy: str) -> Optional[Dict]:
    """Extract data from a single ad element."""
    try:
        ad_data = {
            'advertiser': '',
            'text': '',
            'media': [],
            'cta_text': '',
            'sponsor_info': '',
            'date_scraped': datetime.now().isoformat(),
            'proxy': proxy,
            'timestamp': int(time.time())
        }
        
        # Advertiser name
        try:
            ad_data['advertiser'] = ad_element.find_element(
                By.XPATH, './/div[contains(@class, "_7jwu") or contains(@class, "x1lliihq")]'
            ).text
        except:
            pass
        
        # Ad text content
        try:
            ad_data['text'] = ad_element.find_element(
                By.XPATH, './/div[contains(@class, "_7jyu") or contains(@class, "x1iorvi4")]'
            ).text
        except:
            pass
        
        # Media (images/videos)
        try:
            media_elements = ad_element.find_elements(By.TAG_NAME, 'img')
            ad_data['media'] = [
                img.get_attribute('src') for img in media_elements 
                if img.get_attribute('src') and 'http' in img.get_attribute('src')
            ]
        except:
            pass
        
        # Call to action
        try:
            ad_data['cta_text'] = ad_element.find_element(
                By.XPATH, './/div[contains(@class, "_7jyr") or contains(@role, "button")]'
            ).text
        except:
            pass
        
        # Sponsor information
        try:
            ad_data['sponsor_info'] = ad_element.find_element(
                By.XPATH, './/div[contains(@class, "_7jys")]'
            ).text
        except:
            pass
        
        # Only return if we got meaningful data
        if ad_data['advertiser'] or ad_data['text']:
            return ad_data
        return None
        
    except Exception as e:
        logger.debug(f"Failed to extract ad data: {e}")
        return None



def scrape_with_proxy(proxy: str) -> List[Dict]:
    """Scrape Facebook ads using a single proxy."""
    driver = None
    ads_data = []
    
    try:
        logger.info(f"[{proxy}] Starting scrape session")
        driver = init_driver(proxy)
        
        # Build URL
        base_url = "https://www.facebook.com/ads/library/"
        params = []
        
        if SEARCH_TERM:
            params.append(f"q={SEARCH_TERM}")
            logger.info(f"[{proxy}] Searching for: {SEARCH_TERM}")
        
        if COUNTRY_CODE:
            params.append(f"country={COUNTRY_CODE}")
            logger.info(f"[{proxy}] Country filter: {COUNTRY_CODE}")
        
        params.append("active_status=active")
        params.append("ad_type=all")
        
        url = base_url + "?" + "&".join(params) if params else base_url
        
        driver.get(url)
        logger.info(f"[{proxy}] Page loaded")
        
        # Initial wait and human interaction
        time.sleep(random.uniform(3, 5))
        human_interaction(driver)
        
        scroll_count = 0
        no_new_ads_count = 0
        seen_ad_texts = set()
        
        while len(ads_data) < MAX_ADS_PER_PROXY and scroll_count < SCROLL_ATTEMPTS:
            try:
                # Check for Cloudflare or blocking
                page_source = driver.page_source.lower()
                if any(keyword in page_source for keyword in ['checking your browser', 'cloudflare', 'security check']):
                    logger.warning(f"[{proxy}] Detected bot protection")
                    stats.add_result(proxy, len(ads_data), 'cloudflare')
                    break
                
                # Wait for ads to load
                WebDriverWait(driver, 15).until(
                    lambda d: d.find_elements(By.XPATH, '//div[contains(@class, "_7jyr") or contains(@class, "x1yc453h")]')
                )
                
                # Find all ad cards
                ad_cards = driver.find_elements(
                    By.XPATH, 
                    '//div[contains(@class, "_7jyr") or contains(@class, "x1yc453h") or contains(@data-testid, "ad-card")]'
                )
                
                logger.info(f"[{proxy}] Found {len(ad_cards)} ad elements on page")
                
                initial_count = len(ads_data)
                
                # Extract data from each ad
                for ad in ad_cards:
                    if len(ads_data) >= MAX_ADS_PER_PROXY:
                        break
                    
                    ad_data = extract_ad_data(ad, proxy)
                    
                    if ad_data:
                        # Check for duplicates using text as identifier
                        ad_identifier = ad_data.get('text', '')[:100]
                        if ad_identifier and ad_identifier not in seen_ad_texts:
                            ads_data.append(ad_data)
                            seen_ad_texts.add(ad_identifier)
                            logger.debug(f"[{proxy}] Extracted ad from: {ad_data.get('advertiser', 'Unknown')}")
                
                # Check if we got new ads
                if len(ads_data) == initial_count:
                    no_new_ads_count += 1
                    logger.info(f"[{proxy}] No new ads found (attempt {no_new_ads_count})")
                    if no_new_ads_count >= 3:
                        logger.info(f"[{proxy}] No new ads after 3 attempts, stopping")
                        break
                else:
                    no_new_ads_count = 0
                    logger.info(f"[{proxy}] Total ads collected: {len(ads_data)}")
                
                # Scroll down for more ads
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
                
                # Human interaction
                if scroll_count % 2 == 0:
                    human_interaction(driver)
                
                scroll_count += 1
                
            except Exception as e:
                logger.error(f"[{proxy}] Error during scraping: {str(e)[:200]}")
                if HEADLESS_MODE:
                    try:
                        screenshot_path = OUTPUT_DIR / f"error_{proxy.replace(':', '_').replace('.', '_')}.png"
                        driver.save_screenshot(str(screenshot_path))
                        logger.info(f"[{proxy}] Screenshot saved: {screenshot_path}")
                    except:
                        pass
                break
        
        logger.info(f"[{proxy}] Completed: {len(ads_data)} ads collected")
        stats.add_result(proxy, len(ads_data), 'success' if ads_data else 'failed')
        return ads_data
    
    except Exception as e:
        logger.error(f"[{proxy}] Fatal error: {str(e)[:200]}")
        stats.add_result(proxy, 0, 'error')
        return []
    
    finally:
        if driver:
            try:
                driver.quit()
                logger.debug(f"[{proxy}] Driver closed")
            except:
                pass



def save_to_json(ads: List[Dict], filename: str):
    """Save ads data to JSON file."""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(ads, f, ensure_ascii=False, indent=2)
    logger.info(f"JSON saved: {filepath}")
    return filepath

def save_to_csv(ads: List[Dict], filename: str):
    """Save ads data to CSV file."""
    if not ads:
        logger.warning("No ads to save to CSV")
        return None
    
    filepath = OUTPUT_DIR / filename
    
    # Define CSV columns
    fieldnames = [
        'advertiser', 'text', 'cta_text', 'sponsor_info', 
        'media_count', 'media_urls', 'date_scraped', 'proxy', 'timestamp'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for ad in ads:
            row = {
                'advertiser': ad.get('advertiser', ''),
                'text': ad.get('text', '').replace('\n', ' '),
                'cta_text': ad.get('cta_text', ''),
                'sponsor_info': ad.get('sponsor_info', ''),
                'media_count': len(ad.get('media', [])),
                'media_urls': ' | '.join(ad.get('media', [])),
                'date_scraped': ad.get('date_scraped', ''),
                'proxy': ad.get('proxy', ''),
                'timestamp': ad.get('timestamp', '')
            }
            writer.writerow(row)
    
    logger.info(f"CSV saved: {filepath}")
    return filepath

async def async_scrape_wrapper(proxy: str) -> List[Dict]:
    """Async wrapper for scraping (runs in thread pool)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, scrape_with_proxy, proxy)

async def async_scrape_all(proxies: List[str]) -> List[List[Dict]]:
    """Run all scraping tasks concurrently."""
    tasks = [async_scrape_wrapper(proxy) for proxy in proxies]
    return await asyncio.gather(*tasks)

def main():
    """Main execution function."""
    logger.info("="*60)
    logger.info("FACEBOOK ADS SCRAPER - Starting")
    logger.info("="*60)
    logger.info(f"Configuration:")
    logger.info(f"  - Search Term: {SEARCH_TERM or 'ALL (no filter)'}")
    logger.info(f"  - Country Code: {COUNTRY_CODE or 'ALL (no filter)'}")
    logger.info(f"  - Max Workers: {MAX_WORKERS}")
    logger.info(f"  - Max Ads Per Proxy: {MAX_ADS_PER_PROXY}")
    logger.info(f"  - Headless Mode: {HEADLESS_MODE}")
    logger.info(f"  - Scroll Attempts: {SCROLL_ATTEMPTS}")
    logger.info("="*60)
    
    # Get proxies
    logger.info("Fetching proxies...")
    proxies = get_proxies()
    
    if not proxies:
        logger.error("No proxies available! Exiting...")
        return
    
    logger.info(f"Testing {len(proxies)} proxies...")
    
    # Test proxies in parallel (quick test)
    working_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(proxies))) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    working_proxies.append(proxy)
                    logger.info(f"✓ Proxy OK: {proxy}")
                    if len(working_proxies) >= MAX_WORKERS:
                        break
            except Exception as e:
                logger.debug(f"✗ Proxy failed: {proxy}")
    
    if not working_proxies:
        logger.error("No working proxies found! Exiting...")
        return
    
    logger.info(f"Using {len(working_proxies)} working proxies")
    logger.info("="*60)
    
    # Start scraping with asyncio
    logger.info("Starting parallel scraping...")
    
    try:
        # Run async scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(async_scrape_all(working_proxies))
        loop.close()
    except Exception as e:
        logger.error(f"Async scraping error: {e}")
        # Fallback to thread pool
        logger.info("Falling back to thread pool execution...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(scrape_with_proxy, working_proxies))
    
    # Combine results
    all_ads = []
    seen_texts = set()
    
    for proxy_ads in results:
        for ad in proxy_ads:
            # Deduplicate by text
            ad_text = ad.get('text', '')[:100]
            if ad_text and ad_text not in seen_texts:
                all_ads.append(ad)
                seen_texts.add(ad_text)
    
    logger.info("="*60)
    logger.info(stats.get_summary())
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    search_part = f"_{SEARCH_TERM}" if SEARCH_TERM else "_all"
    country_part = f"_{COUNTRY_CODE}" if COUNTRY_CODE else ""
    
    # Save JSON
    json_filename = f"fb_ads{search_part}{country_part}_{timestamp}.json"
    json_path = save_to_json(all_ads, json_filename)
    
    # Save CSV
    csv_filename = f"fb_ads{search_part}{country_part}_{timestamp}.csv"
    csv_path = save_to_csv(all_ads, csv_filename)
    
    # Save detailed log summary
    summary = {
        'scrape_date': datetime.now().isoformat(),
        'search_term': SEARCH_TERM or 'all',
        'country_code': COUNTRY_CODE or 'all',
        'total_ads': len(all_ads),
        'unique_advertisers': len(set(ad.get('advertiser', '') for ad in all_ads)),
        'proxies_used': len(working_proxies),
        'successful_proxies': stats.successful_proxies,
        'failed_proxies': stats.failed_proxies,
        'cloudflare_blocks': stats.cloudflare_blocks,
        'duration_seconds': time.time() - stats.start_time,
        'files_generated': {
            'json': str(json_path),
            'csv': str(csv_path),
            'log': str(log_filename)
        }
    }
    
    summary_filename = f"summary{search_part}{country_part}_{timestamp}.json"
    summary_path = OUTPUT_DIR / summary_filename
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Summary saved: {summary_path}")
    logger.info("="*60)
    logger.info(f"✓ Scraping complete!")
    logger.info(f"✓ Total unique ads: {len(all_ads)}")
    logger.info(f"✓ Unique advertisers: {summary['unique_advertisers']}")
    logger.info(f"✓ Files saved in: {OUTPUT_DIR}")
    logger.info("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠ Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
