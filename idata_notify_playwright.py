import time
import requests
from playwright.sync_api import sync_playwright

URL = "https://it-tr-appointment.idata.com.tr/tr/appointment-form"
CHECK_INTERVAL = 120  # saniye (2 dk)

TELEGRAM_BOT_TOKEN = "8458891629:AAEWlT6XYXYRE_gRtNukKIer8uKMVh7_UeE"
TELEGRAM_CHAT_ID = "8149792607"

def send_telegram(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                     params={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram gönderim hatası:", e)

def check_slots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        try:
            # Şehir seç
            page.wait_for_selector("select#city", timeout=60000)
            page.select_option("select#city", label="İzmir")

            # Ofis seç
            page.wait_for_selector("select#office", timeout=60000)
            page.select_option("select#office", label="İzmir Ofis")

            # Başvuru türü seç
            page.wait_for_selector("select#getapplicationtype", timeout=60000)
            page.select_option("select#getapplicationtype", label="Turistik")

            # Servis tipi seç
            page.wait_for_selector("select#officetype", timeout=60000)
            page.select_option("select#officetype", label="STANDART")

            # Kişi sayısı seç
            page.wait_for_selector("select#totalPerson", timeout=60000)
            page.select_option("select#totalPerson", label="2 Kişi")

            time.sleep(5)  # Sayfanın güncellenmesi için bekle

            # Uyarı yazısını kontrol et
            text = page.inner_text("body")
            if "Uygun randevu tarihi bulunmamaktadır" not in text:
                send_telegram("İzmir İtalya için RANDEVU açıldı! 🚨")
                print("Randevu bulundu, Telegram'a mesaj gönderildi.")
            else:
                print("Henüz randevu yok.")

        except Exception as e:
            print("Form doldurulamadı:", e)

        browser.close()

if __name__ == "__main__":
    print("İdata randevu takibi başladı...")
    while True:
        check_slots()
        time.sleep(CHECK_INTERVAL)
