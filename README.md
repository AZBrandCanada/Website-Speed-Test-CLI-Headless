# README

This repository provides a performance monitoring script that uses Puppeteer to measure key metrics such as TTFB, DOMContentLoaded, and Load Event End for multiple URLs.

## Supported Operating Systems
Ubuntu 20.04, 24.04 Maybe others
May work on other operating systems but untested.

## Features
- Monitor multiple URLs sequentially
- Sends alerts to Telegram if thresholds are exceeded
- Adjustable delay between checks

### Requirements can be installed with chmod +x install.sh && sudo ./install.sh
- Node.js
- npm
- Xvfb
- Puppeteer
- chromium

### Installation
1. Clone the repository:

```bash
git clone https://github.com/AZBrandCanada/Website-Speed-Test-CLI-Headless
cd Website-Speed-Test-CLI-Headless
```

2. Run the installer:

```bash
chmod +x install.sh
./install.sh
```

3. Configure the script:
```bash
nano website-speed-test.py
```
- Open `website-speed-test.py` and set the following variables:
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `URLS` (an array of URLs to monitor)
  - `DELAY` (time in seconds between URL checks)
  - Set the Metrics you want for TTFB, DomContentLoaded and final load time.
  - telegram_token = "89989878dhha988876677" # your telegram token found with botfather
  - telegram_chat_id = "-8882737773" # your telegram chat itd
  - # Thresholds (in ms Default settings)
  - ttfb_threshold = 1000
  - domcontentloaded_threshold = 5000
  - load_event_end_threshold = 7000
  - delay_between_checks = 5  # seconds




### Usage
To run the script:

```bash
./website-speed-test.py
```
Add it to crontab to run every hour 
```bash
crontab -e
```
```bash
0 * * * * /usr/bin/python3 /home/USERNAME/Website-Speed-Test-CLI-Headless/website-speed-test.py
```
If you want to run a status check 3 times per day and send you results of all websites you can optionally create this crontab 
```bash
0 4,10,22 * * * /usr/bin/python3 /home/USERNAME/Website-Speed-Test-CLI-Headless/status-website.py
```


### Example Output
```
Results for https://website.com-
TTFB: 643 ms,
DOMContentLoaded: 2333 ms,
Load event end: 2959 ms

```

If any thresholds are exceeded, a Telegram alert will be sent with the details.
