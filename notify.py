"""Slanje Telegram notifikacija — koristi isti bot/chat_id koncept kao
stan-monitor. Token i chat_id se čitaju iz env varijabli
(u GitHub Actions: iz Secrets)."""

import os
import requests


def send_telegram(message: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram nije podešen (nedostaju TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID). Poruka:")
        print(message)
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=15,
        )
        if resp.status_code != 200:
            print(f"Telegram greška: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Greška pri slanju Telegram poruke: {e}")
