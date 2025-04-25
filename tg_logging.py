import logging
import asyncio
import telegram
from time import sleep


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)
main_logger = logging.getLogger('Logger')
main_logger.setLevel(logging.INFO)


class TGLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    async def emit_async(self, record):
        log_entry = self.format(record)
        await self.tg_bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )

    def emit(self, record):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            asyncio.create_task(self.emit_async(record))
        else:
            asyncio.run(self.emit_async(record))


def logger_setting(bot_logger_token, chat_id):
    bot = telegram.Bot(token=bot_logger_token)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    telegram_handler = TGLogsHandler(bot, chat_id)
    formatter = logging.Formatter(FORMAT)
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)
    return logger


def exception_log(text, exception):
    logging.error(f'{text}: {exception}', exc_info=True)
    sleep(4)
