import logging
import asyncio
import telegram


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)


class TGLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        print("TGLogsHandler(logging.Handler)")
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        print("chat_id")
        print(chat_id)
        print("bot")
        print(bot)

    def emit(self, record):
        print("record")
        print(record)
        log_entry = self.format(record)
        print("log_entry")
        print(log_entry)
        asyncio.create_task(self._send_log_message(chat_id=self.chat_id, text=log_entry))

    async def _send_log_message(self, message):
        print("message")
        print(message)
        await self.bot.send_message(chat_id=self.chat_id, text=message)


def logging_exception_log(text, exception, bot_logger_token, chat_id, logger):
    print("я тут")
    logger.setLevel(logging.ERROR)
    logging.error(f'{text}: {exception}', exc_info=True)
    print("прошел логгер в консоль")
    
    telegram_handler = TGLogsHandler(bot, chat_id)
    formatter = logging.Formatter(FORMAT)
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)
