import logging
import os
import asyncio
import aiohttp
import requests
from dotenv import load_dotenv, find_dotenv
from bot import send_message
from tg_logging import main_logger, logging_exception_log, send_log_tg


RETRY_DELAY = 60


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


async def process_lesson_data(
    tg_token: str,
    chat_id: str,
    lesson_review_data: dict,
    params: dict
) -> None:
    """Process lesson review data and send notification if needed.
    params:
        tg_token: TG Token
        chat_id: TG Chat ID
        lesson_review_data: lesson review dict
        params: dict timestampt
    return:
        json
    """
    main_logger.info("Программа запрашивает ревью урока")
    if "last_attempt_timestamp" in lesson_review_data:
        params["timestamp"] = lesson_review_data["last_attempt_timestamp"]
        await send_message(tg_token, chat_id, lesson_review_data)


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
    params = {"timestamp": str()}
    while True:
        try:
            x=1/0
            lesson_review_data = await take_lesson_review(
                url_long,
                headers,
                params
                )
            await process_lesson_data(tg_token, chat_id, lesson_review_data, params)
        except requests.exceptions.ConnectionError as e:
            #send_log_tg(bot_logger_token, chat_id)
            logging_exception_log(requests.exceptions.ConnectionError,  e)
            await asyncio.sleep(RETRY_DELAY)
        except KeyError as e:
            #send_log_tg(bot_logger_token, chat_id)
            logging_exception_log(KeyError,  e)
            await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            #send_log_tg(bot_logger_token, chat_id)
            logging_exception_log(Exception,  e)
            await asyncio.sleep(RETRY_DELAY)


if __name__ == "__main__":
    asyncio.run(main())
