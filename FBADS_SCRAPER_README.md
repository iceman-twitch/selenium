# Facebook Ads Library Scraper

Advanced multi-threaded web scraper for Facebook Ads Library with async support, proxy rotation, comprehensive logging, and multiple export formats.

## Features

✅ **Multi-threaded Scraping** - Parallel browser instances for maximum speed  
✅ **Async Support** - Asyncio integration for efficient concurrent operations  
✅ **Headless Mode** - Run without visible browser windows  
✅ **Proxy Rotation** - Automatic proxy fetching and testing from multiple sources  
✅ **Human-like Behavior** - Random scrolling, mouse movements, and timing  
✅ **Bot Detection Avoidance** - Selenium Stealth integration  
✅ **Comprehensive Logging** - Detailed logs with timestamps for every action  
✅ **Multiple Export Formats** - JSON, CSV, and summary reports  
✅ **Smart Deduplication** - Removes duplicate ads automatically  
✅ **Flexible Search** - Filter by search term and country, or scrape all ads  
✅ **Error Handling** - Screenshot capture on errors, graceful failure recovery  

## Installation

```bash
pip install selenium selenium-stealth webdriver-manager requests
```

## Configuration

Edit the configuration variables at the top of `fbads_scrapy.py`:

```python
MAX_WORKERS = 5              # Number of parallel browsers
MAX_ADS_PER_PROXY = 20       # Ads to collect per proxy
SEARCH_TERM = ""             # Search query (empty = all ads)
COUNTRY_CODE = ""            # 2-letter code (empty = all countries)
HEADLESS_MODE = True         # Run without visible browser
SCROLL_ATTEMPTS = 10         # Times to scroll for more ads
```

## Usage Examples

### 1. Scrape All Recent Ads (No Filters)
```python
SEARCH_TERM = ""
COUNTRY_CODE = ""
```
Scrapes all recently active ads from all countries.

### 2. Search Specific Term in USA
```python
SEARCH_TERM = "nike"
COUNTRY_CODE = "US"
```
Scrapes Nike-related ads shown in the United States.

### 3. Scrape Fitness Ads Globally
```python
SEARCH_TERM = "fitness"
COUNTRY_CODE = ""
```
Searches for fitness ads across all countries.

### 4. Country-Specific Scrape (All Ads)
```python
SEARCH_TERM = ""
COUNTRY_CODE = "GB"
```
All ads targeting the United Kingdom.

## Running the Scraper

```bash
python fbads_scrapy.py
```

The scraper will:
1. Fetch proxies from multiple sources
2. Test proxies for connectivity
3. Start parallel scraping sessions
4. Display real-time progress in logs
5. Save results to JSON, CSV, and summary files

## Output Files

All files are saved in the `output/` directory with timestamps:

### JSON Output (`fb_ads_nike_US_20250103_143022.json`)
```json
[
  {
    "advertiser": "Nike",
    "text": "Just Do It. Shop the latest Nike gear...",
    "media": ["https://...image1.jpg", "https://...image2.jpg"],
    "cta_text": "Shop Now",
    "sponsor_info": "Paid for by Nike Inc.",
    "date_scraped": "2025-01-03T14:30:22",
    "proxy": "123.45.67.89:8080",
    "timestamp": 1704290422
  }
]
```

### CSV Output (`fb_ads_nike_US_20250103_143022.csv`)
Spreadsheet-friendly format with columns:
- advertiser
- text
- cta_text
- sponsor_info
- media_count
- media_urls
- date_scraped
- proxy
- timestamp

### Summary Report (`summary_nike_US_20250103_143022.json`)
```json
{
  "scrape_date": "2025-01-03T14:30:22",
  "search_term": "nike",
  "country_code": "US",
  "total_ads": 87,
  "unique_advertisers": 12,
  "proxies_used": 5,
  "successful_proxies": 4,
  "failed_proxies": 1,
  "cloudflare_blocks": 0,
  "duration_seconds": 124.5,
  "files_generated": {
    "json": "output/fb_ads_nike_US_20250103_143022.json",
    "csv": "output/fb_ads_nike_US_20250103_143022.csv",
    "log": "logs/fbads_scrape_20250103_143022.log"
  }
}
```

## Log Files

Detailed logs saved in `logs/` directory:

```
2025-01-03 14:30:22 - INFO - ============================================================
2025-01-03 14:30:22 - INFO - FACEBOOK ADS SCRAPER - Starting
2025-01-03 14:30:22 - INFO - ============================================================
2025-01-03 14:30:23 - INFO - Fetching proxies...
2025-01-03 14:30:25 - INFO - [123.45.67.89:8080] Starting scrape session
2025-01-03 14:30:28 - INFO - [123.45.67.89:8080] Page loaded
2025-01-03 14:30:30 - INFO - [123.45.67.89:8080] Found 15 ad elements on page
2025-01-03 14:30:31 - INFO - [123.45.67.89:8080] Total ads collected: 15
2025-01-03 14:30:45 - INFO - [123.45.67.89:8080] Completed: 20 ads collected
```

## Country Codes

Common 2-letter ISO country codes:

| Code | Country        | Code | Country       |
|------|---------------|------|---------------|
| US   | United States | GB   | United Kingdom|
| CA   | Canada        | AU   | Australia     |
| DE   | Germany       | FR   | France        |
| JP   | Japan         | BR   | Brazil        |
| IN   | India         | IT   | Italy         |
| ES   | Spain         | MX   | Mexico        |

[Full list](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

## Data Fields

Each scraped ad contains:

- **advertiser** - Company/page name running the ad
- **text** - Main ad copy/description
- **media** - Array of image/video URLs
- **cta_text** - Call-to-action button text ("Shop Now", "Learn More", etc.)
- **sponsor_info** - Sponsorship/funding information
- **date_scraped** - ISO timestamp when scraped
- **proxy** - Proxy server used
- **timestamp** - Unix timestamp

## Advanced Configuration

### Adjust Performance

```python
# Fast scraping (may miss some ads)
MAX_WORKERS = 10
SCROLL_ATTEMPTS = 5

# Thorough scraping (slower but more complete)
MAX_WORKERS = 3
SCROLL_ATTEMPTS = 15
```

### Custom Proxy Lists

Replace the `get_proxies()` function to use your own proxy service:

```python
def get_proxies() -> List[str]:
    return [
        "123.45.67.89:8080",
        "98.76.54.32:3128",
        # ... your proxies
    ]
```

### Debugging Mode

```python
HEADLESS_MODE = False  # Show browser windows
logging.basicConfig(level=logging.DEBUG)  # More detailed logs
```

## Troubleshooting

### "No proxies available"
- Check your internet connection
- Try different proxy sources
- Use your own proxy list

### "Cloudflare blocks"
- Use residential proxies instead of datacenter
- Reduce MAX_WORKERS to look less suspicious
- Increase delays in human_interaction()

### "No ads found"
- Try different search terms
- Remove country filter
- Check if Facebook changed their HTML structure
- Look at error screenshots in output/ directory

### Import errors
```bash
pip install --upgrade selenium selenium-stealth webdriver-manager
```

## Performance Tips

1. **Optimal Workers**: 5-10 workers for best speed/reliability balance
2. **Proxy Quality**: Use residential proxies for better success rates
3. **Rate Limiting**: Add delays between requests if getting blocked
4. **Memory**: Close unused Chrome instances if system slows down

## Legal & Ethical Use

⚠️ **Important**: 
- Use responsibly and respect Facebook's Terms of Service
- This tool is for educational and research purposes
- Do not use for competitive intelligence or spam
- Respect rate limits and don't overload Facebook's servers
- Some jurisdictions may restrict web scraping activities

## Statistics Display

After completion, view detailed statistics:

```
╔═══════════════════════════════════════════════════════════╗
║              FACEBOOK ADS SCRAPER - SUMMARY               ║
╠═══════════════════════════════════════════════════════════╣
║ Total Ads Collected:                                  87 ║
║ Successful Proxies:                                    4 ║
║ Failed Proxies:                                        1 ║
║ Cloudflare Blocks:                                     0 ║
║ Duration:                                         124.50s ║
╚═══════════════════════════════════════════════════════════╝
```

## Example Workflows

### Market Research
```python
SEARCH_TERM = "cryptocurrency"
COUNTRY_CODE = "US"
MAX_ADS_PER_PROXY = 50
```
Analyze crypto ad trends in the US market.

### Competitor Analysis
```python
SEARCH_TERM = "running shoes"
COUNTRY_CODE = ""
MAX_WORKERS = 8
```
See what running shoe brands are advertising globally.

### Ad Creative Research
```python
SEARCH_TERM = "black friday"
COUNTRY_CODE = "GB"
SCROLL_ATTEMPTS = 20
```
Study Black Friday ad creatives in the UK.

## Support

For issues or questions:
1. Check the log files in `logs/` directory
2. Look for error screenshots in `output/` directory
3. Enable debug logging for more details
4. Review the comprehensive inline code comments

## Version History

- **v2.0** - Complete rewrite with async, logging, CSV export
- **v1.0** - Basic scraping functionality

---

**Happy Scraping! 🚀**
