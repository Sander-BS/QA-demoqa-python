import os
import requests


def send_telegram_notification(
    token: str, chat_id: str, message: str, image_path: str = None
) -> None:
    base_url = f'https://api.telegram.org/bot{token}'

    if image_path and os.path.exists(image_path):
        url = f'{base_url}/sendPhoto'
        with open(image_path, 'rb') as photo:
            payload = {'chat_id': chat_id, 'caption': message, 'parse_mode': 'HTML'}
            files = {'photo': photo}
            response = requests.post(url, files=files, data=payload)
    else:
        url = f'{base_url}/sendMessage'
        payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(
            f'Failed to send Telegram notification: {response.status_code} - {response.text}'
        )
