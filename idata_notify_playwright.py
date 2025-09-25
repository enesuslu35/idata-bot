import os
import asyncio
from playwright.async_api import async_playwright
import requests

# Telegram token ve chat_id gizli olarak GitHub Secrets'tan alınır
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Örnek: İdata sayfasına git
        await page.goto("https://idata.com.tr")  

        # Burada kendi locator / işlem kodunu yaz
        try:
            await page.wait_for_selector("#city", timeout=10000)
            message = "İdata bot başarılı şekilde çalıştı ✅"
        except Exception as e:
            message = f"Hata oluştu ❌: {e}"

        # Telegram'a mesaj gönder
        send_message(message)

        await browser.close()

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

if __name__ == "__main__":
    asyncio.run(run_bot())
