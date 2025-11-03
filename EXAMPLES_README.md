# Selenium Stealth Examples Collection

Comprehensive examples demonstrating Selenium with Selenium Stealth for web automation and scraping while avoiding bot detection.

## 📦 Installation

```powershell
pip install selenium selenium-stealth webdriver-manager
```

## 🚀 New Examples

### 1. **web_scraping_stealth.py** - Web Scraping
Demonstrates data extraction from websites while avoiding detection.

**Features:**
- ✅ Basic quote scraping
- ✅ Pagination handling
- ✅ Bot detection testing
- ✅ Table data extraction
- ✅ Stealth driver setup

**Run:**
```powershell
python web_scraping_stealth.py
```

---

### 2. **form_automation_stealth.py** - Form Automation
Shows how to fill forms, handle dropdowns, checkboxes, and simulate human-like interactions.

**Features:**
- ✅ Basic form filling
- ✅ Human-like typing with delays
- ✅ Multi-step forms
- ✅ Dynamic form elements
- ✅ Form validation handling
- ✅ Dropdowns, checkboxes, radio buttons

**Run:**
```powershell
python form_automation_stealth.py
```

---

### 3. **screenshot_pdf_stealth.py** - Screenshots & PDFs
Demonstrates capturing screenshots at various resolutions and generating PDFs.

**Features:**
- ✅ Full page screenshots
- ✅ Element-specific screenshots
- ✅ Multi-resolution captures (desktop/tablet/mobile)
- ✅ PDF generation from webpages
- ✅ HTML and text content extraction
- ✅ Scroll-based screenshots
- ✅ Before/after action captures

**Run:**
```powershell
python screenshot_pdf_stealth.py
```

---

### 4. **advanced_interactions_stealth.py** - Advanced Interactions
Shows complex user interactions like drag & drop, mouse movements, and keyboard shortcuts.

**Features:**
- ✅ Mouse hover interactions
- ✅ Drag and drop (two methods)
- ✅ Keyboard shortcuts (Ctrl+A, Ctrl+C, etc.)
- ✅ Double-click actions
- ✅ Right-click context menu
- ✅ Scroll into view
- ✅ Chained action sequences
- ✅ Human-like typing simulation
- ✅ Frame and window handling

**Run:**
```powershell
python advanced_interactions_stealth.py
```

---

### 5. **wait_strategies_stealth.py** - Wait Strategies
Comprehensive guide to handling dynamic content with various wait strategies.

**Features:**
- ✅ Explicit waits with multiple conditions
- ✅ Wait for text conditions
- ✅ Element state change detection
- ✅ Implicit waits
- ✅ Custom wait conditions
- ✅ Polling intervals
- ✅ AJAX completion detection
- ✅ Fluent wait patterns

**Run:**
```powershell
python wait_strategies_stealth.py
```

---

## 🎯 Existing Examples

- `test_stealth.py` - Basic stealth test
- `twitch_signin.py` - Twitch sign-in automation
- `amazon_login.py` - Amazon login example
- `python_selenium_example.py` - CAPTCHA solving example
- And more...

## 🔧 Common Stealth Configuration

All examples use the following stealth configuration:

```python
from selenium_stealth import stealth

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
```

## 📝 Key Features Across Examples

### Stealth Techniques
- ✅ Remove automation flags
- ✅ Custom user agents
- ✅ Human-like timing delays
- ✅ WebGL and canvas fingerprinting protection
- ✅ Disable automation extensions

### Chrome Options
```python
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
```

## 🎓 Learning Path

1. Start with `web_scraping_stealth.py` - Learn basic scraping
2. Move to `form_automation_stealth.py` - Practice form interactions
3. Try `wait_strategies_stealth.py` - Master dynamic content
4. Explore `advanced_interactions_stealth.py` - Complex actions
5. Use `screenshot_pdf_stealth.py` - Capture and document

## 🧪 Testing Bot Detection

Run the bot detection test:
```python
python web_scraping_stealth.py
```

Check these sites manually:
- https://bot.sannysoft.com/
- https://arh.antoinevastel.com/bots/areyouheadless

## ⚠️ Best Practices

1. **Use Appropriate Delays** - Don't scrape too fast
2. **Respect robots.txt** - Check website policies
3. **Rotate User Agents** - Vary your fingerprint
4. **Handle Errors Gracefully** - Implement try-except blocks
5. **Use Explicit Waits** - More reliable than implicit waits
6. **Close Drivers Properly** - Use try-finally blocks

## 🛠️ Troubleshooting

### ChromeDriver Issues
If ChromeDriver fails to install automatically:
```powershell
# Manual download and specify path
from selenium.webdriver.chrome.service import Service
s = Service("path/to/chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)
```

### Stealth Not Working
1. Update to latest versions
2. Test on bot detection sites
3. Disable headless mode for debugging
4. Check Chrome version compatibility

## 📚 Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium Stealth GitHub](https://github.com/diprajpatra/selenium-stealth)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

## 🤝 Contributing

Feel free to add more examples or improve existing ones!

## 📄 License

See LICENSE file for details.
