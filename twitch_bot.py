import time
import requests
import random 
import string
import re
import sys
import os, platform
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

global twitch_url
global proxy_mode
twitch_url = 'https://twitch.tv/'
proxy_mode = 0

def get_useragent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()
def check_proxy(proxy):
    """Test if proxy is working by making a request to Twitch"""
    try:
        proxydict = {
            'https': proxy.strip(),
            'http': proxy.strip()
        }
        
        # Test proxy with a simple request to Twitch homepage
        r = requests.get(
            "https://www.twitch.tv",
            proxies=proxydict,
            timeout=10
        )
        
        # Consider proxy working if we get any successful response
        if r.status_code in [200, 301, 302, 403]:
            print(f"✓ Proxy working: {proxy.strip()} (Status: {r.status_code})")
            return True
        else:
            print(f"✗ Proxy failed: {proxy.strip()} (Status: {r.status_code})")
            return False
            
    except requests.exceptions.ProxyError:
        print(f"✗ Proxy error: {proxy.strip()} (Connection failed)")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Proxy timeout: {proxy.strip()} (Too slow)")
        return False
    except Exception as e:
        print(f"✗ Proxy error: {proxy.strip()} - {str(e)}")
        return False

def get_proxy():
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + r"\proxy.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    while True:
        proxy = lines[random.randint(0,len(lines)-2)]
        if check_proxy(proxy):
            return proxy


    # return lines[random.randint(0,len(lines)-2)]

class TwitchAccount:
    """Handle Twitch account data including cookies and credentials"""
    
    def __init__(self, username):
        self.username = username
        self.config_file = f"twitch_{username}.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Load account configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    print(f"✓ Loaded config for {self.username}")
                    return config
            except Exception as e:
                print(f"✗ Error loading config: {e}")
                return self.create_default_config()
        else:
            print(f"✗ Config file not found: {self.config_file}")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration structure"""
        return {
            "username": self.username,
            "password": "",
            "email": {
                "address": "",
                "password": "",
                "cookies": []
            },
            "twitch_cookies": [],
            "last_login": None,
            "settings": {
                "auto_login": True,
                "chat_enabled": True,
                "read_chat": True
            }
        }
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"✓ Config saved for {self.username}")
            return True
        except Exception as e:
            print(f"✗ Error saving config: {e}")
            return False
    
    def get_credentials(self):
        """Get username and password"""
        return self.config.get('username'), self.config.get('password')
    
    def get_email_credentials(self):
        """Get email credentials"""
        email_data = self.config.get('email', {})
        return email_data.get('address'), email_data.get('password')
    
    def get_twitch_cookies(self):
        """Get Twitch cookies"""
        return self.config.get('twitch_cookies', [])
    
    def get_email_cookies(self):
        """Get email cookies"""
        return self.config.get('email', {}).get('cookies', [])
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.config['last_login'] = datetime.now().isoformat()
        self.save_config()


def chrome(use_proxy=False):
    """Setup Chrome driver with stealth mode"""
    options = Options()
    
    # User agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    options.add_argument("user-agent=" + ua)
    
    # Proxy setup
    if use_proxy and proxy_mode:
        proxy = get_proxy()
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
            print(f"Using proxy: {proxy}")
    
    # Stealth options
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument('--log-level=3')
    
    # Optional: headless mode
    # options.add_argument('--headless')
    options.add_argument("--mute-audio")
    
    # Download preferences (for email attachments if needed)
    prefs = {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    # Try to use webdriver_manager or fallback to local chromedriver
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        try:
            chromepath = 'chromedriver.exe'
            service = Service(chromepath)
            driver = webdriver.Chrome(service=service, options=options)
        except:
            # Last resort: try without service
            driver = webdriver.Chrome(options=options)
    
    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )
    
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)
    
    return driver

class TwitchBot:
    """Enhanced Twitch bot with authentication and chat functionality"""
    
    def __init__(self, username, channel_url=None):
        self.username = username
        self.account = TwitchAccount(username)
        self.driver = None
        self.channel_url = channel_url or twitch_url
        self.logged_in = False
        self.chat_messages = []
    
    def start_driver(self):
        """Initialize Chrome driver"""
        self.driver = chrome(use_proxy=bool(proxy_mode))
        print(f"✓ Driver initialized for {self.username}")
    
    def load_cookies(self):
        """Load cookies into the browser"""
        if not self.driver:
            print("✗ Driver not initialized")
            return False
        
        cookies = self.account.get_twitch_cookies()
        
        if not cookies:
            print("✗ No cookies found")
            return False
        
        try:
            # Need to visit Twitch first before adding cookies
            self.driver.get("https://www.twitch.tv")
            time.sleep(2)
            
            for cookie in cookies:
                try:
                    # Remove fields that Selenium doesn't accept
                    clean_cookie = {
                        'name': cookie.get('name'),
                        'value': cookie.get('value'),
                        'domain': cookie.get('domain', '.twitch.tv'),
                        'path': cookie.get('path', '/'),
                    }
                    
                    # Optional fields
                    if 'expiry' in cookie:
                        clean_cookie['expiry'] = cookie['expiry']
                    if 'secure' in cookie:
                        clean_cookie['secure'] = cookie['secure']
                    if 'httpOnly' in cookie:
                        clean_cookie['httpOnly'] = cookie['httpOnly']
                    
                    self.driver.add_cookie(clean_cookie)
                except Exception as e:
                    print(f"Warning: Could not add cookie {cookie.get('name')}: {e}")
            
            print(f"✓ Loaded {len(cookies)} cookies")
            
            # Refresh to apply cookies
            self.driver.refresh()
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading cookies: {e}")
            return False
    
    def save_cookies(self):
        """Save current browser cookies"""
        if not self.driver:
            return False
        
        try:
            cookies = self.driver.get_cookies()
            self.account.config['twitch_cookies'] = cookies
            self.account.save_config()
            print(f"✓ Saved {len(cookies)} cookies")
            return True
        except Exception as e:
            print(f"✗ Error saving cookies: {e}")
            return False
    
    def check_if_logged_in(self):
        """Check if already logged in"""
        try:
            # Look for user menu button (appears when logged in)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-a-target='user-menu-toggle']"))
            )
            self.logged_in = True
            print("✓ Already logged in!")
            return True
        except TimeoutException:
            self.logged_in = False
            print("✗ Not logged in")
            return False
    
    def login(self):
        """Login to Twitch using credentials"""
        if not self.driver:
            print("✗ Driver not initialized")
            return False
        
        username, password = self.account.get_credentials()
        
        if not username or not password:
            print("✗ Missing credentials in config file")
            return False
        
        try:
            print("Attempting login...")
            
            # Go to login page
            self.driver.get("https://www.twitch.tv/login")
            time.sleep(random.uniform(2, 3))
            
            # Enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )
            
            # Human-like typing
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password-input")
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-a-target='passport-login-button']")
            login_button.click()
            
            print("Login button clicked, waiting for response...")
            time.sleep(5)
            
            # Check if login successful
            if self.check_if_logged_in():
                self.save_cookies()
                self.account.update_last_login()
                return True
            else:
                print("✗ Login may have failed or requires verification")
                return False
                
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def authenticate(self):
        """Authenticate user (try cookies first, then login)"""
        if not self.driver:
            self.start_driver()
        
        # Try loading cookies first
        if self.load_cookies():
            self.driver.get(self.channel_url)
            time.sleep(3)
            
            if self.check_if_logged_in():
                print("✓ Authenticated via cookies")
                return True
        
        # If cookies didn't work, try login
        print("Cookies didn't work, attempting login...")
        return self.login()
    
    def human_like_scroll(self, direction="down", distance=None):
        """Simulate human-like scrolling with mouse wheel"""
        if not distance:
            distance = random.randint(100, 400)
        
        if direction == "down":
            distance = abs(distance)
        else:
            distance = -abs(distance)
        
        # Smooth scroll with easing (like real mouse wheel)
        scroll_script = f"""
            var start = window.pageYOffset;
            var distance = {distance};
            var duration = {random.randint(300, 800)};
            var startTime = null;
            
            function easeInOutQuad(t) {{
                return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
            }}
            
            function scroll(currentTime) {{
                if (startTime === null) startTime = currentTime;
                var timeElapsed = currentTime - startTime;
                var progress = Math.min(timeElapsed / duration, 1);
                var ease = easeInOutQuad(progress);
                window.scrollTo(0, start + (distance * ease));
                
                if (timeElapsed < duration) {{
                    requestAnimationFrame(scroll);
                }}
            }}
            
            requestAnimationFrame(scroll);
        """
        
        self.driver.execute_script(scroll_script)
        time.sleep(random.uniform(0.5, 1.5))
    
    def human_like_mouse_movement(self):
        """Simulate random mouse movements using JavaScript"""
        # Move mouse cursor to random position (simulated via page interactions)
        move_script = """
            // Create invisible overlay to track 'mouse movement'
            var moveEvent = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': Math.random() * window.innerWidth,
                'clientY': Math.random() * window.innerHeight
            });
            document.dispatchEvent(moveEvent);
        """
        self.driver.execute_script(move_script)
    
    def random_human_action(self):
        """Perform a random human-like action"""
        actions = [
            self.human_like_scroll_chat,
            self.hover_over_stream,
            self.check_stream_title,
            self.random_pause,
            lambda: self.human_like_scroll("down", random.randint(50, 200)),
            lambda: self.human_like_scroll("up", random.randint(50, 150)),
        ]
        
        action = random.choice(actions)
        try:
            action()
        except:
            pass
    
    def human_like_scroll_chat(self):
        """Scroll the chat area like a human"""
        scroll_chat_script = """
            var chatScroll = document.querySelector('.chat-scrollable-area__message-container');
            if (chatScroll) {
                var scrollAmount = Math.random() * 100 + 50;
                chatScroll.scrollTop += (Math.random() > 0.5 ? scrollAmount : -scrollAmount);
            }
        """
        self.driver.execute_script(scroll_chat_script)
        time.sleep(random.uniform(0.3, 0.8))
    
    def hover_over_stream(self):
        """Hover over the stream player"""
        try:
            player = self.driver.find_element(By.CSS_SELECTOR, "video")
            ActionChains(self.driver).move_to_element(player).perform()
            time.sleep(random.uniform(0.5, 2))
        except:
            pass
    
    def check_stream_title(self):
        """Look at stream title (scroll to top briefly)"""
        self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
        time.sleep(random.uniform(1, 2))
        self.driver.execute_script("window.scrollTo({top: 200, behavior: 'smooth'});")
        time.sleep(random.uniform(0.5, 1))
    
    def random_pause(self):
        """Random pause like user is reading or watching"""
        time.sleep(random.uniform(3, 8))
    
    def watch_stream(self, duration_minutes=60):
        """Watch stream for specified duration with human-like behavior"""
        if not self.driver:
            print("✗ Driver not initialized")
            return
        
        try:
            self.driver.get(self.channel_url)
            time.sleep(random.uniform(3, 6))
            
            # Random initial scroll to see page
            self.human_like_scroll("down", random.randint(100, 300))
            time.sleep(random.uniform(1, 2))
            self.human_like_scroll("up", random.randint(50, 150))
            time.sleep(random.uniform(1, 2))
            
            # Unmute if needed
            try:
                mute_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-a-target='player-mute-unmute-button']")
                aria_label = mute_button.get_attribute('aria-label')
                if aria_label and 'Unmute' in aria_label:
                    # Move to button before clicking (human-like)
                    ActionChains(self.driver).move_to_element(mute_button).pause(random.uniform(0.3, 0.8)).click().perform()
                    print("✓ Stream unmuted")
                    time.sleep(random.uniform(0.5, 1.5))
            except:
                pass
            
            # Set quality to lowest for bandwidth
            try:
                settings_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-a-target='player-settings-button']")
                ActionChains(self.driver).move_to_element(settings_button).pause(random.uniform(0.2, 0.5)).click().perform()
                time.sleep(random.uniform(0.8, 1.5))
                
                quality_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-a-target='player-settings-menu-item-quality']")
                ActionChains(self.driver).move_to_element(quality_button).pause(random.uniform(0.2, 0.5)).click().perform()
                time.sleep(random.uniform(0.8, 1.5))
                
                # Select 160p if available
                quality_options = self.driver.find_elements(By.CSS_SELECTOR, "input[data-a-target='tw-radio']")
                if quality_options:
                    ActionChains(self.driver).move_to_element(quality_options[-1]).pause(random.uniform(0.2, 0.5)).click().perform()
                    print("✓ Quality set to lowest")
                    time.sleep(random.uniform(0.5, 1))
            except:
                print("Could not change quality")
            
            # Click somewhere on page to dismiss any popups
            try:
                self.driver.execute_script("document.body.click();")
                time.sleep(0.5)
            except:
                pass
            
            print(f"Watching stream for {duration_minutes} minutes with human-like behavior...")
            
            # Watch and interact periodically with realistic behavior
            intervals = duration_minutes * 6  # Check every 10 seconds
            action_counter = 0
            
            for i in range(intervals):
                # Random wait time between actions (8-15 seconds)
                wait_time = random.uniform(8, 15)
                time.sleep(wait_time)
                
                action_counter += 1
                
                # Perform random human-like actions
                # More frequent actions early on (first 20% of watch time)
                if i < intervals * 0.2:
                    action_frequency = 2  # Every 2 intervals
                else:
                    action_frequency = random.randint(4, 8)  # Every 4-8 intervals
                
                if action_counter >= action_frequency:
                    self.random_human_action()
                    action_counter = 0
                
                # Occasionally move mouse
                if random.random() < 0.3:  # 30% chance
                    self.human_like_mouse_movement()
                
                # Check if still on page
                if "twitch.tv" not in self.driver.current_url:
                    print("✗ Page navigated away")
                    break
                
                # Occasional longer pause (like user is afk briefly)
                if random.random() < 0.05:  # 5% chance
                    afk_time = random.uniform(30, 90)
                    print(f"  [Human behavior: Brief pause for {int(afk_time)}s]")
                    time.sleep(afk_time)
            
            print("✓ Watch session completed")
            
        except Exception as e:
            print(f"✗ Error watching stream: {e}")
    
    def read_chat(self, duration_seconds=60):
        """Read chat messages for specified duration"""
        if not self.driver:
            print("✗ Driver not initialized")
            return []
        
        print(f"Reading chat for {duration_seconds} seconds...")
        
        start_time = time.time()
        messages = []
        
        try:
            while time.time() - start_time < duration_seconds:
                try:
                    # Find chat messages
                    chat_lines = self.driver.find_elements(By.CSS_SELECTOR, ".chat-line__message")
                    
                    for line in chat_lines[-10:]:  # Get last 10 messages
                        try:
                            username_elem = line.find_element(By.CSS_SELECTOR, ".chat-author__display-name")
                            message_elem = line.find_element(By.CSS_SELECTOR, ".text-fragment")
                            
                            username = username_elem.text
                            message = message_elem.text
                            
                            msg_data = {
                                "username": username,
                                "message": message,
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            if msg_data not in messages:
                                messages.append(msg_data)
                                print(f"[{username}]: {message}")
                        except:
                            pass
                    
                    time.sleep(2)
                    
                except Exception as e:
                    pass
            
            self.chat_messages = messages
            return messages
            
        except Exception as e:
            print(f"✗ Error reading chat: {e}")
            return messages
    
    def send_chat_message(self, message):
        """Send a message in chat"""
        if not self.logged_in:
            print("✗ Must be logged in to send chat messages")
            return False
        
        try:
            # Find chat input
            chat_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-a-target='chat-input']"))
            )
            
            # Type message with human-like timing
            for char in message:
                chat_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.3, 0.7))
            
            # Send message
            chat_input.send_keys(Keys.RETURN)
            print(f"✓ Sent message: {message}")
            
            time.sleep(random.uniform(1, 2))
            return True
            
        except Exception as e:
            print(f"✗ Error sending chat message: {e}")
            return False
    
    def run(self, watch_duration=60, read_chat_enabled=True, chat_duration=60):
        """Run the bot with all features"""
        try:
            print(f"\n{'='*50}")
            print(f"Starting Twitch Bot for {self.username}")
            print(f"Channel: {self.channel_url}")
            print(f"{'='*50}\n")
            
            # Start driver and authenticate
            self.start_driver()
            
            if not self.authenticate():
                print("✗ Authentication failed")
                return
            
            # Watch stream
            if watch_duration > 0:
                self.watch_stream(duration_minutes=watch_duration)
            
            # Read chat
            if read_chat_enabled and self.account.config['settings'].get('read_chat', True):
                messages = self.read_chat(duration_seconds=chat_duration)
                print(f"\n✓ Captured {len(messages)} chat messages")
            
            # Keep alive option
            keep_alive = input("\nKeep browser open? (y/n): ").lower().strip()
            if keep_alive == 'y':
                print("Browser will stay open. Press Ctrl+C to exit.")
                while True:
                    time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n✓ Bot stopped by user")
        except Exception as e:
            print(f"✗ Bot error: {e}")
        finally:
            if self.driver:
                print("Closing browser...")
                self.driver.quit()


def create_sample_config(username):
    """Create a sample configuration file"""
    sample_config = {
        "username": username,
        "password": "YOUR_TWITCH_PASSWORD",
        "email": {
            "address": "your_email@example.com",
            "password": "YOUR_EMAIL_PASSWORD",
            "cookies": []
        },
        "twitch_cookies": [],
        "last_login": None,
        "settings": {
            "auto_login": True,
            "chat_enabled": True,
            "read_chat": True
        }
    }
    
    filename = f"twitch_{username}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(sample_config, f, indent=4)
        print(f"✓ Sample config created: {filename}")
        print("Please edit the file and add your credentials!")
        return True
    except Exception as e:
        print(f"✗ Error creating config: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Twitch Bot')
    parser.add_argument('username', help='Twitch username for the bot')
    parser.add_argument('--channel', '-c', help='Channel URL to watch', default='https://twitch.tv/')
    parser.add_argument('--watch', '-w', type=int, help='Watch duration in minutes', default=60)
    parser.add_argument('--chat', type=int, help='Chat reading duration in seconds', default=60)
    parser.add_argument('--proxy', '-p', type=int, help='Use proxy (1=yes, 0=no)', default=0)
    parser.add_argument('--create-config', action='store_true', help='Create sample config file')
    
    args = parser.parse_args()
    
    # Set global proxy mode
    proxy_mode = args.proxy
    
    # Create config if requested
    if args.create_config:
        create_sample_config(args.username)
        sys.exit(0)
    
    # Run bot
    bot = TwitchBot(username=args.username, channel_url=args.channel)
    bot.run(watch_duration=args.watch, chat_duration=args.chat)