import requests
import time

# Set the headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
}

def get_site(url, headers=headers, max_attempts=10, delay_seconds=1):
    for _ in range(max_attempts):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res
        time.sleep(delay_seconds)
    return None