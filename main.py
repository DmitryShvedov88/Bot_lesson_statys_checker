import os
from time import sleep
import asyncio
import aiohttp
import requests
from dotenv import load_dotenv, find_dotenv
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
    async with aiohttp.ClientSession() as session:
        async with session.get(url_long, headers=headers, params=params) as response:
            response.raise_for_status()
            response = await response.json()
            params["timestamp"] = response["last_attempt_timestamp"]
            return response


async def main() -> None:
    load_dotenv(find_dotenv())
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    dvmn_token = os.environ["DVMN_TOKEN"]
    url_long = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f'Token {dvmn_token}'}
    while True:
        params = {"timestamp": str()}
        try:
            lesson_review_data = await take_lesson_review_data(
                url_long,
                headers,
                params
                )
            await send_message(tg_token, chat_id, lesson_review_data)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print("ConnectionError occurred")
            sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
