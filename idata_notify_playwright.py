import os
import time
import requests
from bs4 import BeautifulSoup

URL = "https://online.idata.com.tr/randevu/italya/izmir"
CHECK_INTERVAL = 120

# Token ve Chat ID'yi ortam değişkenlerinden al
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=payload, timeout=10)

def check_slots():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        if "Randevu yok" in r.text:
            return False
        return True
    except Exception as e:
        print("Hata:", e)
        return False

if __name__ == "__main__":
    print("İdata randevu takibi başladı...")
    while True:
        if check_slots():
            send_telegram("📢 İzmir İtalya vizesi için İdata randevusu açıldı!")
        time.sleep(CHECK_INTERVAL)
