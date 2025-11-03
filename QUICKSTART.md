# Quick Start Guide - Enhanced Twitch Bot

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

```powershell
pip install selenium selenium-stealth webdriver-manager random-user-agent requests
```

### Step 2: Create Your Config File

```powershell
python twitch_bot.py YOUR_USERNAME --create-config
```

This creates `twitch_YOUR_USERNAME.json`. Edit it:

```json
{
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "email": {
        "address": "your_email@example.com",
        "password": "your_email_password",
        "cookies": []
    }
}
```

### Step 3: Run the Bot

```powershell
# Watch a specific channel
python twitch_bot.py YOUR_USERNAME --channel https://twitch.tv/shroud

# That's it! The bot will:
# ✅ Login automatically
# ✅ Save cookies for next time
# ✅ Watch the stream
# ✅ Read chat messages
```

## 📝 Common Commands

```powershell
# Watch for 30 minutes
python twitch_bot.py myuser -c https://twitch.tv/ninja -w 30

# Read chat for 5 minutes (300 seconds)
python twitch_bot.py myuser -c https://twitch.tv/pokimane --chat 300

# Use with proxy
python twitch_bot.py myuser -c https://twitch.tv/xqc --proxy 1
```

## 🎯 What the Bot Does

1. **First Run**:
   - Logs in with your credentials
   - Saves cookies to config file
   - Watches stream
   - Monitors chat

2. **Next Runs**:
   - Uses saved cookies (no login needed!)
   - Faster startup
   - Same functionality

## 💡 Tips

- **Keep Config Safe**: Never share your `twitch_*.json` files
- **First Login**: May require manual 2FA verification
- **Cookie Expiry**: Bot auto re-authenticates if cookies expire
- **Multiple Accounts**: Create multiple config files for different accounts

## 🔧 Troubleshooting

**Bot won't start?**
```powershell
# Update Chrome
# Then run:
pip install --upgrade selenium webdriver-manager
```

**Can't login?**
- Check username/password in config file
- Complete 2FA in the browser when it appears
- Cookies will be saved after successful login

**Need help?**
- See full documentation: `TWITCH_BOT_README.md`
- Check example config: `twitch_example_user.json`

## 📚 More Examples

See the other example scripts:
- `web_scraping_stealth.py` - Web scraping examples
- `form_automation_stealth.py` - Form filling examples
- `advanced_interactions_stealth.py` - Mouse/keyboard examples
- `wait_strategies_stealth.py` - Handling dynamic content
- `screenshot_pdf_stealth.py` - Taking screenshots/PDFs

## ⚠️ Important

Use responsibly! This is for educational purposes. Respect Twitch's Terms of Service.

---

**Ready to go?** Run your first bot:
```powershell
python twitch_bot.py myusername --create-config
# Edit the config file, then:
python twitch_bot.py myusername --channel https://twitch.tv/yourfavoritestreamer
```
