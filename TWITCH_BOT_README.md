# Enhanced Twitch Bot

A sophisticated Twitch bot with authentication, cookie management, stream watching, and chat functionality.

## 🚀 Features

- ✅ **Cookie Management** - Save and load cookies for persistent login
- ✅ **Auto Authentication** - Login with credentials or cookies
- ✅ **Stream Watching** - Watch streams with configurable duration
- ✅ **Chat Reading** - Monitor and log chat messages
- ✅ **Chat Sending** - Send messages in chat (when logged in)
- ✅ **Email Support** - Store email credentials for account recovery
- ✅ **Stealth Mode** - Avoid bot detection with selenium-stealth
- ✅ **Proxy Support** - Optional proxy configuration
- ✅ **Human-like Behavior** - Random delays and interactions

## 📦 Installation

```powershell
pip install selenium selenium-stealth webdriver-manager random-user-agent requests
```

## 🔧 Configuration

### 1. Create Configuration File

Create a JSON file named `twitch_[USERNAME].json` with your credentials:

```powershell
python twitch_bot.py your_username --create-config
```

This creates `twitch_your_username.json`. Edit it and add your credentials:

```json
{
    "username": "your_twitch_username",
    "password": "your_twitch_password",
    "email": {
        "address": "your_email@example.com",
        "password": "your_email_password",
        "cookies": []
    },
    "twitch_cookies": [],
    "last_login": null,
    "settings": {
        "auto_login": true,
        "chat_enabled": true,
        "read_chat": true
    }
}
```

### 2. Configuration Fields

| Field | Description |
|-------|-------------|
| `username` | Your Twitch username |
| `password` | Your Twitch password |
| `email.address` | Your email address |
| `email.password` | Your email password (for recovery) |
| `email.cookies` | Email provider cookies (optional) |
| `twitch_cookies` | Twitch session cookies (auto-saved) |
| `last_login` | Timestamp of last login (auto-updated) |
| `settings.auto_login` | Auto-login on start |
| `settings.chat_enabled` | Enable chat functionality |
| `settings.read_chat` | Enable chat reading |

## 🎮 Usage

### Basic Usage

```powershell
# Watch a stream for 60 minutes (default)
python twitch_bot.py your_username --channel https://twitch.tv/channelname

# Watch for 30 minutes
python twitch_bot.py your_username --channel https://twitch.tv/channelname --watch 30

# Watch and read chat for 120 seconds
python twitch_bot.py your_username --channel https://twitch.tv/channelname --chat 120

# Use proxy
python twitch_bot.py your_username --channel https://twitch.tv/channelname --proxy 1
```

### Command Line Arguments

```
python twitch_bot.py [OPTIONS]

Required:
  username              Twitch username for the bot

Optional:
  --channel, -c URL     Channel URL to watch (default: https://twitch.tv/)
  --watch, -w MINUTES   Watch duration in minutes (default: 60)
  --chat SECONDS        Chat reading duration in seconds (default: 60)
  --proxy, -p 0|1       Use proxy: 1=yes, 0=no (default: 0)
  --create-config       Create sample config file and exit
```

### Examples

#### 1. Create Config
```powershell
python twitch_bot.py myusername --create-config
```

#### 2. Watch Stream
```powershell
python twitch_bot.py myusername --channel https://twitch.tv/shroud --watch 120
```

#### 3. Watch and Monitor Chat
```powershell
python twitch_bot.py myusername -c https://twitch.tv/xqc -w 60 --chat 300
```

#### 4. Use with Proxy
```powershell
python twitch_bot.py myusername -c https://twitch.tv/tfue --proxy 1
```

## 🔑 Cookie Management

### How Cookies Work

1. **First Run**: Bot logs in with credentials and saves cookies
2. **Subsequent Runs**: Bot uses saved cookies (faster, no login needed)
3. **Cookie Expiry**: If cookies expire, bot automatically re-authenticates

### Cookie Storage

Cookies are automatically saved to your config file after successful login:
- Location: `twitch_[username].json`
- Field: `twitch_cookies`
- Format: JSON array of cookie objects

### Manual Cookie Export (Optional)

You can manually export cookies from your browser:

1. Login to Twitch in Chrome
2. Open DevTools (F12) → Application → Cookies
3. Copy all cookies to your config file's `twitch_cookies` array

Example cookie format:
```json
{
    "name": "auth-token",
    "value": "your_token_here",
    "domain": ".twitch.tv",
    "path": "/",
    "expiry": 1234567890,
    "secure": true,
    "httpOnly": true
}
```

## 💬 Chat Features

### Reading Chat

The bot can monitor and log chat messages:

```python
# Read chat for 60 seconds
bot = TwitchBot(username="myuser", channel_url="https://twitch.tv/channel")
bot.start_driver()
bot.authenticate()
messages = bot.read_chat(duration_seconds=60)

# Messages are saved in bot.chat_messages
for msg in messages:
    print(f"[{msg['username']}]: {msg['message']}")
```

### Sending Chat Messages

```python
# Must be logged in
bot.authenticate()
bot.send_chat_message("Hello from bot!")
```

## 🛡️ Stealth Features

The bot uses multiple techniques to avoid detection:

- **Selenium Stealth** - Patches WebDriver to avoid detection
- **Human-like Timing** - Random delays between actions
- **User Agent Spoofing** - Uses realistic browser user agents
- **Automation Flag Removal** - Removes WebDriver automation indicators
- **Natural Scrolling** - Random scroll movements
- **Quality Adjustment** - Changes stream quality naturally

## 🌐 Proxy Support

### Setup Proxy

1. Create `proxy.txt` in the same directory
2. Add proxies (one per line):
   ```
   http://proxy1.com:8080
   http://proxy2.com:8080
   socks5://proxy3.com:1080
   ```

3. Run with proxy flag:
   ```powershell
   python twitch_bot.py username --proxy 1
   ```

The bot will:
- Test each proxy for connectivity
- Use a working proxy for the session
- Rotate to different proxy on next run

## 📊 Bot Workflow

```
1. Load Configuration
   ↓
2. Initialize Chrome Driver (with stealth)
   ↓
3. Attempt Cookie Authentication
   ↓
4. If cookies fail → Login with credentials
   ↓
5. Save new cookies
   ↓
6. Navigate to channel
   ↓
7. Watch stream (with random interactions)
   ↓
8. Read chat (if enabled)
   ↓
9. Keep alive (optional)
   ↓
10. Save session & quit
```

## 🔒 Security Best Practices

1. **Never commit config files** - Add `twitch_*.json` to `.gitignore`
2. **Use environment variables** - For sensitive credentials
3. **Rotate passwords** - Change passwords regularly
4. **2FA consideration** - Bot may require manual 2FA verification
5. **Proxy privacy** - Use trusted proxy providers

## 🐛 Troubleshooting

### Bot can't login
- Check credentials in config file
- Twitch may require 2FA (manual verification needed)
- Check if IP is rate-limited

### Cookies not working
- Cookies may have expired (bot will auto re-login)
- Check cookie domain is `.twitch.tv`
- Delete `twitch_cookies` array and re-authenticate

### Chat not reading
- Ensure you're logged in
- Some channels restrict chat to followers
- Chat selector may have changed (update CSS selectors)

### ChromeDriver errors
- Update Chrome browser
- Run: `pip install --upgrade webdriver-manager`
- Or manually download chromedriver.exe

### Proxy not working
- Test proxy manually
- Check proxy format in proxy.txt
- Ensure proxy supports HTTPS

## 📝 Example Session

```powershell
PS> python twitch_bot.py iceman --channel https://twitch.tv/shroud -w 30

==================================================
Starting Twitch Bot for iceman
Channel: https://twitch.tv/shroud
==================================================

✓ Loaded config for iceman
✓ Driver initialized for iceman
✓ Loaded 15 cookies
✓ Already logged in!
✓ Authenticated via cookies
✓ Stream unmuted
✓ Quality set to lowest
Watching stream for 30 minutes...
✓ Watch session completed

Reading chat for 60 seconds...
[viewer123]: nice play!
[viewer456]: gg
[viewer789]: PogChamp
✓ Captured 3 chat messages

Keep browser open? (y/n): n
Closing browser...
✓ Bot stopped
```

## 🔄 Advanced Usage

### Use as Python Module

```python
from twitch_bot import TwitchBot

# Create bot instance
bot = TwitchBot(username="myuser", channel_url="https://twitch.tv/channel")

# Custom workflow
bot.start_driver()
bot.authenticate()
bot.watch_stream(duration_minutes=120)
messages = bot.read_chat(duration_seconds=300)

# Send chat message
bot.send_chat_message("Great stream!")

# Manual control
input("Press Enter to close...")
bot.driver.quit()
```

### Multiple Bots

Run multiple bots with different configs:

```powershell
# Terminal 1
python twitch_bot.py user1 -c https://twitch.tv/channel1

# Terminal 2  
python twitch_bot.py user2 -c https://twitch.tv/channel2

# Terminal 3
python twitch_bot.py user3 -c https://twitch.tv/channel3
```

## 📚 Dependencies

- `selenium` - Browser automation
- `selenium-stealth` - Bot detection avoidance
- `webdriver-manager` - Automatic ChromeDriver management
- `random-user-agent` - User agent rotation
- `requests` - HTTP requests for proxy testing

## ⚖️ Legal Disclaimer

This bot is for educational purposes. Use responsibly and in accordance with Twitch Terms of Service. Automated interactions may violate platform policies.

## 🤝 Contributing

Improvements welcome! Consider adding:
- Firefox support
- Twitch drops farming
- Channel points farming
- Multi-account management
- Better CAPTCHA handling
- Stream quality analytics

## 📄 License

See LICENSE file for details.
