import subprocess
import requests
import time

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""

URLS = [
    "https://website.com",
    "https://website.com",
    "https://website.ca",
    "https://website.ca"
]

DELAY = 5
MEASURE_SCRIPT = "measureLoad.js"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def parse_output(output, url):
    try:
        ttfb = output.split("TTFB: ")[1].split(" ms")[0]
        dom = output.split("DOMContentLoaded: ")[1].split(" ms")[0]
        load_end = output.split("Load event end: ")[1].split(" ms")[0]
        return f"{url}, TTFB {ttfb}, DOM {dom}, END {load_end}"
    except Exception:
        return f"{url}, Error parsing output"

def main():
    results = []
    for url in URLS:
        print(f"Checking {url}...")
        try:
            result = subprocess.run(
                ["node", MEASURE_SCRIPT, url],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                print(f"Node command failed with return code {result.returncode}")
                print("stderr:", result.stderr)
                results.append(f"{url}, Error running node script")
                continue

            output = result.stdout
            print(output)
            results.append(parse_output(output, url))
        except Exception as e:
            print(f"Error checking {url}: {e}")
            results.append(f"{url}, Error: {e}")

        time.sleep(DELAY)

    message = "Website Status:\n" + "\n".join(results)
    send_telegram_alert(message)
    print("Status message sent to Telegram.")

if __name__ == "__main__":
    main()
