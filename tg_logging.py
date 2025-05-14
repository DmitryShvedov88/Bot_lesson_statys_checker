import logging
import asyncio


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)


class TGLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self._send_log_message(
            log_entry
            ))

    async def _send_log_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)
