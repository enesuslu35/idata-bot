import asyncio
from playwright.async_api import async_playwright
from aiogram import Bot, Dispatcher
import os

# Telegram bot bilgileri
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # GitHub Secrets'ten alınacak
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # GitHub Secrets'ten alınacak

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def run_bot():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Siteye git
            await page.goto("https://it-tr-appointment.idata.com.tr/tr/appointment-form", timeout=60000)
            await bot.send_message(CHAT_ID, "🌍 Sayfa açıldı!")

            # Şehir seçimi (otomatik İzmir)
            try:
                await page.wait_for_selector("select[name='city']", timeout=60000)
                await page.select_option("select[name='city']", label="İzmir")
                await bot.send_message(CHAT_ID, "✅ Şehir otomatik seçildi: İzmir")
            except Exception as e:
                await bot.send_message(CHAT_ID, f"❌ Şehir seçilemedi: {e}")

            # Burada diğer adımlar eklenecek...

            await browser.close()

    except Exception as e:
        await bot.send_message(CHAT_ID, f"🚨 Genel hata: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
