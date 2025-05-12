import logging
import asyncio
import telegram


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)
main_logger = logging.getLogger('Logger')
main_logger.setLevel(logging.INFO)


class TGLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self._send_log_message(log_entry))

    async def _send_log_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)


def send_log_tg(bot_logger_token, chat_id):
    bot = telegram.Bot(token=bot_logger_token)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    telegram_handler = TGLogsHandler(bot, chat_id)
    formatter = logging.Formatter(FORMAT)
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)
    return logger


def logging_exception_log(text, exception):
    logging.error(f'{text}: {exception}', exc_info=True)
