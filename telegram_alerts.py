
import requests

def send_alert(token, chat_id, message):

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass
