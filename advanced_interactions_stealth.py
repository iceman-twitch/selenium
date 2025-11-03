"""
Advanced Interactions with Selenium Stealth
Demonstrates mouse movements, drag & drop, keyboard shortcuts, and complex actions
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def mouse_hover_example():
    """Demonstrate mouse hover interactions"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/mouse_interaction.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)
        
        # Find hoverable element
        try:
            hoverable = driver.find_element(By.ID, "hover")
            
            # Create ActionChains object
            actions = ActionChains(driver)
            
            # Perform hover
            actions.move_to_element(hoverable).perform()
            print("Hovered over element")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Hover demo: {e}")
        
    finally:
        time.sleep(2)
        driver.quit()


def drag_and_drop_example():
    """Demonstrate drag and drop"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/dragAndDropTest.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)
        
        try:
            # Find draggable and droppable elements
            draggable = driver.find_element(By.ID, "draggable")
            droppable = driver.find_element(By.ID, "droppable")
            
            # Method 1: Using drag_and_drop
            actions = ActionChains(driver)
            actions.drag_and_drop(draggable, droppable).perform()
            
            print("Drag and drop completed")
            time.sleep(2)
            
            # Refresh for another demo
            driver.refresh()
            time.sleep(2)
            
            # Method 2: Using click_and_hold, move, release
            draggable = driver.find_element(By.ID, "draggable")
            droppable = driver.find_element(By.ID, "droppable")
            
            actions = ActionChains(driver)
            actions.click_and_hold(draggable)\
                   .move_to_element(droppable)\
                   .release()\
                   .perform()
            
            print("Alternative drag and drop completed")
            
        except Exception as e:
            print(f"Drag and drop demo: {e}")
        
    finally:
        time.sleep(2)
        driver.quit()


def keyboard_shortcuts_example():
    """Demonstrate keyboard shortcuts and key combinations"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/single_text_input.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textInput"))
        )
        
        text_input = driver.find_element(By.ID, "textInput")
        
        # Type text
        text_input.send_keys("Hello Selenium World")
        time.sleep(1)
        
        # Select all (Ctrl+A)
        text_input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.5)
        
        # Copy (Ctrl+C)
        text_input.send_keys(Keys.CONTROL + "c")
        time.sleep(0.5)
        
        # Clear field
        text_input.clear()
        
        # Paste (Ctrl+V)
        text_input.send_keys(Keys.CONTROL + "v")
        print("Text copied and pasted")
        
        time.sleep(1)
        
        # Use ActionChains for more complex key combinations
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL)\
               .send_keys("a")\
               .key_up(Keys.CONTROL)\
               .send_keys(Keys.DELETE)\
               .perform()
        
        print("Text deleted using ActionChains")
        
    finally:
        time.sleep(2)
        driver.quit()


def double_click_example():
    """Demonstrate double-click action"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/mouse_interaction.html")
        
        time.sleep(2)
        
        try:
            # Find element that responds to double-click
            element = driver.find_element(By.ID, "clickable")
            
            # Perform double-click
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            
            print("Double-click performed")
            
        except Exception as e:
            print(f"Double-click demo: {e}")
        
    finally:
        time.sleep(2)
        driver.quit()


def right_click_context_menu():
    """Demonstrate right-click (context menu)"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/mouse_interaction.html")
        
        time.sleep(2)
        
        try:
            element = driver.find_element(By.ID, "clickable")
            
            # Perform right-click
            actions = ActionChains(driver)
            actions.context_click(element).perform()
            
            print("Right-click (context menu) performed")
            
        except Exception as e:
            print(f"Right-click demo: {e}")
        
    finally:
        time.sleep(2)
        driver.quit()


def scroll_into_view_example():
    """Scroll element into view"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("http://quotes.toscrape.com")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
        )
        
        # Find an element at the bottom
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        last_quote = quotes[-1]
        
        # Scroll to element using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", last_quote)
        print("Scrolled to last quote")
        
        time.sleep(1)
        
        # Highlight the element
        driver.execute_script("arguments[0].style.border='3px solid red'", last_quote)
        
        time.sleep(2)
        
        # Scroll to top
        driver.execute_script("window.scrollTo(0, 0);")
        print("Scrolled to top")
        
    finally:
        time.sleep(2)
        driver.quit()


def chain_multiple_actions():
    """Chain multiple actions together"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/single_text_input.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textInput"))
        )
        
        text_input = driver.find_element(By.ID, "textInput")
        
        # Chain multiple actions
        actions = ActionChains(driver)
        actions.click(text_input)\
               .send_keys("First text")\
               .pause(0.5)\
               .send_keys(Keys.ENTER)\
               .send_keys("Second line")\
               .pause(0.5)\
               .key_down(Keys.CONTROL)\
               .send_keys("a")\
               .key_up(Keys.CONTROL)\
               .send_keys("Replaced all text")\
               .perform()
        
        print("Chained actions completed")
        
    finally:
        time.sleep(2)
        driver.quit()


def simulate_human_typing():
    """Simulate human-like typing with random delays"""
    import random
    
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/single_text_input.html")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textInput"))
        )
        
        text_input = driver.find_element(By.ID, "textInput")
        
        message = "This is typed like a human would type it"
        
        actions = ActionChains(driver)
        actions.click(text_input)
        
        for char in message:
            actions.send_keys(char)
            actions.pause(random.uniform(0.05, 0.2))  # Random delay
        
        actions.perform()
        
        print("Human-like typing completed")
        
    finally:
        time.sleep(2)
        driver.quit()


def handle_frames_and_windows():
    """Switch between frames and windows"""
    driver = setup_stealth_driver()
    
    try:
        driver.get("https://www.selenium.dev/selenium/web/frameset.html")
        
        time.sleep(2)
        
        # Get current window handle
        main_window = driver.current_window_handle
        print(f"Main window handle: {main_window}")
        
        # Switch to frame by index
        driver.switch_to.frame(0)
        print("Switched to first frame")
        
        # Do something in frame
        time.sleep(1)
        
        # Switch back to main content
        driver.switch_to.default_content()
        print("Switched back to main content")
        
        # Switch to frame by name/id (if available)
        try:
            driver.switch_to.frame("frame1")
            driver.switch_to.default_content()
        except:
            pass
        
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    print("=== Advanced Interactions with Selenium Stealth ===\n")
    
    print("1. Mouse Hover:")
    mouse_hover_example()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Drag and Drop:")
    drag_and_drop_example()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Keyboard Shortcuts:")
    keyboard_shortcuts_example()
    
    print("\n" + "="*50 + "\n")
    
    print("4. Double Click:")
    double_click_example()
    
    print("\n" + "="*50 + "\n")
    
    print("5. Right Click:")
    right_click_context_menu()
    
    print("\n" + "="*50 + "\n")
    
    print("6. Scroll Into View:")
    scroll_into_view_example()
    
    print("\n" + "="*50 + "\n")
    
    print("7. Chain Multiple Actions:")
    chain_multiple_actions()
    
    print("\n" + "="*50 + "\n")
    
    print("8. Human-like Typing:")
    simulate_human_typing()
    
    print("\n" + "="*50 + "\n")
    
    print("9. Frames and Windows:")
    handle_frames_and_windows()
