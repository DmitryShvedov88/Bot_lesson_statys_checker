import os
import asyncio
import time
import requests
from bot import send_message


async def prepare_lesson_review(lesson_review_data: dict) -> dict:
    '''Prepare JSON for result dict
    params:
        lesson_review_data: dict with result
    return:
        result dict for prepare to massege
    '''
    lesson_review = {
        "submitted_at":  lesson_review_data["new_attempts"][0]["submitted_at"],
        "check_status": lesson_review_data["new_attempts"][0]["is_negative"],
        "lesson_title":  lesson_review_data["new_attempts"][0]["lesson_title"],
        "lesson_url": lesson_review_data["new_attempts"][0]["lesson_url"]
        }
    return lesson_review


async def take_lesson_review_data(
    url_long: str,
    headers: dict,
    params: dict
    ) -> dict:
    '''Make a Api reuest
    params:
        url_long: url
        headers: dict autorisation token
        params: dict timestampt
    return:
        json
    '''
    response = requests.get(url_long, headers=headers,  params=params, timeout=30)
    response = response.json()
    params["timestamp"] = response["last_attempt_timestamp"]
    return response


async def main() -> None:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    dvmn_token = os.environ["DVMN_TOKEN"]
    url_long = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f'Token {dvmn_token}'}
    params = {"timestamp": '0'}
    connect_try = 1
    max_connect_try = 5
    while True:
        try:
            lesson_review_data = await take_lesson_review_data(
                url_long,
                headers,
                params
                )
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
        lesson_review = await prepare_lesson_review(lesson_review_data)
        await send_message(tg_token, chat_id, lesson_review)


if __name__ == "__main__":
    asyncio.run(main())
