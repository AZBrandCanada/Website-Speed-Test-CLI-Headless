
import subprocess
import re
import requests
import time

# Config
node_script = "/home/ryan/measureLoad.js"
urls = [
    "https://website.com",
    "https://website.com",
    "https://website.ca",
    "https://website.ca"
]
telegram_token = ""
telegram_chat_id = ""

# Thresholds (in ms)
ttfb_threshold = 1000
domcontentloaded_threshold = 6000
load_event_end_threshold = 7000

delay_between_checks = 5  # seconds for each website in the list. 

def send_telegram_message(text):
    url_telegram = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url_telegram, data=payload, timeout=10)
        return response.ok
    except Exception as e:
        print("Failed to send Telegram message:", e)
        return False

def run_measure_load(url):
    cmd = ["xvfb-run", "node", node_script, url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout
    except Exception as e:
        print(f"Error running measureLoad.js for {url}:", e)
        return ""

def parse_metrics(output):
    ttfb = None
    domcontentloaded = None
    load_event_end = None

    ttfb_match = re.search(r"TTFB:\s*(\d+)\s*ms", output)
    dom_match = re.search(r"DOMContentLoaded:\s*(\d+)\s*ms", output)
    load_match = re.search(r"Load event end:\s*(\d+)\s*ms", output)

    if ttfb_match:
        ttfb = int(ttfb_match.group(1))
    if dom_match:
        domcontentloaded = int(dom_match.group(1))
    if load_match:
        load_event_end = int(load_match.group(1))

    return ttfb, domcontentloaded, load_event_end

def check_url(url):
    print(f"Checking {url}...")
    output = run_measure_load(url)
    if not output:
        print(f"No output from measureLoad.js for {url}")
        return

    ttfb, dom, load_end = parse_metrics(output)
    print(f"Results for {url} - TTFB: {ttfb} ms, DOMContentLoaded: {dom} ms, Load event end: {load_end} ms")

    alert_msgs = []

    if ttfb and ttfb > ttfb_threshold:
        alert_msgs.append(f"⚠️ TTFB is high: {ttfb} ms (limit {ttfb_threshold} ms)")
    if dom and dom > domcontentloaded_threshold:
        alert_msgs.append(f"⚠️ DOMContentLoaded is high: {dom} ms (limit {domcontentloaded_threshold} ms)")
    if load_end and load_end > load_event_end_threshold:
        alert_msgs.append(f"⚠️ Load event end is high: {load_end} ms (limit {load_event_end_threshold} ms)")

    if alert_msgs:
        message = f"Load Metrics Alert for {url}:\n" + "\n".join(alert_msgs)
        sent = send_telegram_message(message)
        if sent:
            print("Alert sent to Telegram.")
        else:
            print("Failed to send alert to Telegram.")
    else:
        print(f"All metrics within thresholds for {url}.")

def main():
    for url in urls:
        check_url(url)
        print(f"Waiting {delay_between_checks} seconds before next check...\n")
        time.sleep(delay_between_checks)

if __name__ == "__main__":
    main()

