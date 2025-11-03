# Facebook Ads Scraper - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install selenium selenium-stealth webdriver-manager requests
```

### Step 2: Configure Your Scrape

Open `fbads_scrapy.py` and edit these lines (around line 21-26):

```python
MAX_WORKERS = 5              # Number of parallel browsers (5-10 recommended)
MAX_ADS_PER_PROXY = 20       # Ads per proxy before stopping
SEARCH_TERM = "nike"         # What to search for (empty = all ads)
COUNTRY_CODE = "US"          # 2-letter code (empty = all countries)
HEADLESS_MODE = True         # True = hidden browser, False = visible
SCROLL_ATTEMPTS = 10         # How many times to scroll
```

### Step 3: Run!
```bash
python fbads_scrapy.py
```

That's it! The scraper will:
- ✅ Fetch and test proxies automatically
- ✅ Start parallel scraping
- ✅ Show progress in real-time
- ✅ Save results to `output/` folder
- ✅ Create detailed logs in `logs/` folder

---

## 📊 Example Configurations

### Scrape Everything (No Filters)
```python
SEARCH_TERM = ""
COUNTRY_CODE = ""
```
Gets all recent ads from all countries.

### Specific Brand in USA
```python
SEARCH_TERM = "nike"
COUNTRY_CODE = "US"
```

### Industry Research (Global)
```python
SEARCH_TERM = "cryptocurrency"
COUNTRY_CODE = ""
MAX_ADS_PER_PROXY = 50
```

### Fast Scrape (Many Workers)
```python
MAX_WORKERS = 10
SCROLL_ATTEMPTS = 5
```

### Thorough Scrape (More Scrolling)
```python
MAX_WORKERS = 3
SCROLL_ATTEMPTS = 20
MAX_ADS_PER_PROXY = 50
```

---

## 📁 Output Files

After running, check the `output/` folder:

### 1. JSON File
`fb_ads_nike_US_20250103_143022.json`
- Full ad data with all fields
- Easy to process programmatically

### 2. CSV File  
`fb_ads_nike_US_20250103_143022.csv`
- Spreadsheet format
- Open in Excel/Google Sheets

### 3. Summary File
`summary_nike_US_20250103_143022.json`
- Statistics and metadata
- Performance metrics

---

## 🔍 Common Search Terms

**Fashion & Apparel:**
- `nike`, `adidas`, `fashion`, `clothing`, `shoes`

**Technology:**
- `iphone`, `laptop`, `software`, `app`, `saas`

**Finance:**
- `crypto`, `bitcoin`, `trading`, `investment`, `insurance`

**E-commerce:**
- `shopify`, `ecommerce`, `dropshipping`, `amazon`

**Services:**
- `fitness`, `education`, `real estate`, `travel`

**Seasonal:**
- `black friday`, `christmas`, `summer sale`

---

## 🌍 Country Codes

| Code | Country        | Code | Country       |
|------|---------------|------|---------------|
| US   | United States | GB   | United Kingdom|
| CA   | Canada        | AU   | Australia     |
| DE   | Germany       | FR   | France        |
| JP   | Japan         | BR   | Brazil        |
| IN   | India         | IT   | Italy         |
| ES   | Spain         | MX   | Mexico        |
| NL   | Netherlands   | SE   | Sweden        |
| NO   | Norway        | DK   | Denmark       |

---

## 🐛 Debugging

### See What's Happening
```python
HEADLESS_MODE = False  # Shows browser windows
```

### Check Logs
```bash
# View the latest log file
cd logs
# Open the most recent .log file
```

### View Error Screenshots
```bash
cd output
# Look for error_*.png files
```

---

## ⚡ Performance Tips

1. **Start Small** - Test with 1-2 workers first
2. **Good Proxies** - Use quality proxies for better results
3. **Respect Rate Limits** - Don't go too aggressive
4. **Monitor Logs** - Watch for Cloudflare blocks
5. **Adjust Workers** - Find the sweet spot for your system

---

## 📋 What Gets Scraped

Each ad includes:
- ✅ Advertiser name
- ✅ Ad text/copy
- ✅ Call-to-action button text
- ✅ Media URLs (images/videos)
- ✅ Sponsor information
- ✅ Timestamp
- ✅ Proxy used

---

## 🔥 Pro Tips

### Scrape Competitor Ads
```python
SEARCH_TERM = "your_competitor_name"
COUNTRY_CODE = "US"
```

### Find Ad Trends
```python
SEARCH_TERM = ""  # All ads
MAX_ADS_PER_PROXY = 100  # Get lots of data
```

### Monitor Specific Country
```python
SEARCH_TERM = ""
COUNTRY_CODE = "DE"  # Germany only
```

### Quick Test Run
```python
MAX_WORKERS = 2
MAX_ADS_PER_PROXY = 10
SCROLL_ATTEMPTS = 3
```

---

## ❓ Troubleshooting

### "No proxies available"
- Check internet connection
- Script will retry with backup sources

### "Cloudflare blocks"
- Reduce MAX_WORKERS
- Use better quality proxies
- Add more delays

### "No ads found"
- Try different search term
- Remove filters (empty strings)
- Check if Facebook changed layout

### Script crashes
- Check logs/ folder for details
- Look at error screenshots
- Try with HEADLESS_MODE = False

---

## 🎯 Next Steps

1. ✅ Run your first scrape
2. ✅ Check output files
3. ✅ Analyze the CSV in Excel
4. ✅ Try different search terms
5. ✅ Experiment with configurations

---

## 📚 More Information

See `FBADS_SCRAPER_README.md` for complete documentation.

See `fb_ads_config.json` for detailed configuration options.

See `fb_ads_example.json` for sample output format.

---

**Happy Scraping! 🎉**
