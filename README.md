# README

This repository provides a performance monitoring script that uses Puppeteer to measure key metrics such as TTFB, DOMContentLoaded, and Load Event End for multiple URLs.

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
- Open `website-speed-test.py` and set the following variables:
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `URLS` (an array of URLs to monitor)
  - `DELAY` (time in seconds between URL checks)
  - `node_script = "/home/USERNAME/measureLoad.js"` (set to the location of this script on your server)


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
0 * * * * /usr/bin/python3 /home/ryan/website-speed-test.py
```


### Example Output
```
TTFB: 996 ms
DOMContentLoaded: 3463 ms
Load event end: 4569 ms
Total request duration: 711 ms
```

If any thresholds are exceeded, a Telegram alert will be sent with the details.
