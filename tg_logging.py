import logging
import asyncio


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
        asyncio.create_task(self._send_log_message(
            log_entry
            ))

    async def _send_log_message(self, message):
        print("message")
        print(message)
        await self.bot.send_message(chat_id=self.chat_id, text=message)
