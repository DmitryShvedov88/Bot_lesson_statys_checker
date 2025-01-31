import requests
import os
from bot import send_message
import asyncio
import os
import telegram
import time
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def take_lesson_review(url_long, headers, params):
    response = requests.get(url_long, headers=headers,  params=params, timeout=30)
    response = response.json()
    params["timestamp"] = response["last_attempt_timestamp"]
    return response.json()


def main():
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    dvmn_token = os.environ["DVMN_TOKEN"]
    bot = telegram.Bot(token=tg_token)
    
    url_long = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f'Token {dvmn_token}'}
    params = {"timestamp": '0'}
   
    connect_try = 1
    max_connect_try = 5
 
    while True:
        try:
            lesson_review = take_lesson_review(url_long, headers, params)
        except requests.exceptions.Timeout:
            print("Timeout occurred")
            continue
        except requests.exceptions.ConnectionError:
            print("ConnectionError occurred")
            if connect_try == 1:
                print("Reconnecting")
            elif connect_try > max_connect_try:
                time.sleep(15)
            connect_try += 1
            continue
        connect_try = 1
        # asyncio.run(send_message())


if __name__ == "__main__":
    main()
