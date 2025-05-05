import logging
import os
from time import sleep
import asyncio
import aiohttp
import requests
from dotenv import load_dotenv, find_dotenv
from bot import send_message
from tg_logging import main_logger


async def take_lesson_review(
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
        async with session.get(
            url_long, headers=headers, params=params
        ) as response:
            response.raise_for_status()
            response = await response.json()
            return response


async def main() -> None:
    main_logger.info("Программа стартует")
    load_dotenv(find_dotenv())
    tg_token = os.environ["TG_TOKEN"]
    bot_logger_token = os.environ["TG_BOT_LOGGER_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    dvmn_token = os.environ["DVMN_TOKEN"]
    url_long = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f'Token {dvmn_token}'}
    main_logger.info("Программа готова")
    while True:
        params = {"timestamp": str()}
        try:
            lesson_review_data = await take_lesson_review(
                url_long,
                headers,
                params
                )
            params["timestamp"] = lesson_review_data["last_attempt_timestamp"]
            await send_message(tg_token, chat_id, lesson_review_data)
        except requests.exceptions.ConnectionError as e:
            main_logger.warning('ConnectionError occurred')
            logging.error(f'{requests.exceptions.ConnectionError}: {e}', exc_info=True)
            sleep(60)
        except Exception as e:
            main_logger.exception('BotFail')
            logging.error(f'{Exception}: {e}', exc_info=True)
            sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
