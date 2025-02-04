import os
import asyncio
import requests
from bot import send_message


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
    response.raise_for_status()
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
    while True:
        try:
            lesson_review_data = await take_lesson_review_data(
                url_long,
                headers,
                params
                )
        except requests.exceptions.ConnectionError:
            print("ConnectionError occurred")
        await send_message(tg_token, chat_id, lesson_review_data)


if __name__ == "__main__":
    asyncio.run(main())
