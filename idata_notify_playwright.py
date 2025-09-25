import os
import asyncio
from playwright.async_api import async_playwright
import requests

# Telegram ayarları
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("https://it-tr-appointment.idata.com.tr/tr/appointment-form")
            await page.wait_for_load_state("networkidle")  # Sayfa yüklenmesini bekle

            # Şehir dropdown'unu bekle
            await page.wait_for_selector("select[name='city']", timeout=30000)
            await send_telegram_message("✅ Sayfa başarıyla yüklendi ve şehir seçici bulundu!")

        except Exception as e:
            await send_telegram_message(f"Hata oluştu ❌: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
