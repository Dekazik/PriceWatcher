import requests
from core.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("   ⚠️  Telegram not configured (fill in TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in core/config.py)")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }, timeout=10)

        if response.status_code == 200:
            print("    Telegram notification sent!")
            return True
        else:
            print(f"   ❌ Error sending Telegram message: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Failed to send Telegram message: {e}")
        return False
