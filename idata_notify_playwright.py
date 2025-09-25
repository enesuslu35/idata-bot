import time
import requests
from playwright.sync_api import sync_playwright

# ---------- AYARLAR ----------
URL = "https://online.idata.com.tr/randevu/italya/izmir"  # İzmir İtalya randevu sayfası
CHECK_INTERVAL = 120  # saniye, 2 dakika

TELEGRAM_BOT_TOKEN = "8458891629:AAEtR5lhmD2tCay-gSciPvGW7B7HN7m8Ag0"
TELEGRAM_CHAT_ID = "8149792607"  # senin chat ID’n
# --------------------------------

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram mesajı gönderildi.")
        else:
            print("❌ Telegram mesaj gönderilemedi:", r.text)
    except Exception as e:
        print("❌ Hata:", e)

def check_slots():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, timeout=30000)
            page.wait_for_timeout(2000)  # sayfanın yüklenmesini bekle
            content = page.content()
            browser.close()
            if "Randevu yok" in content:
                return False
            return True
    except Exception as e:
        print("❌ Randevu kontrol hatası:", e)
        return False

if __name__ == "__main__":
    print("🟡 İdata randevu takibi başladı...")
    while True:
        if check_slots():
            send_telegram("📢 İzmir İtalya vizesi için İdata randevusu açıldı!")
        time.sleep(CHECK_INTERVAL)
