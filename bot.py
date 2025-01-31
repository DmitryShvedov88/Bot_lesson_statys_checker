import asyncio
import os
import telegram


last_lesson = {
    "submitted_at":  lesson_review["new_attempts"][0]["submitted_at"],
    "is_negative": lesson_review["new_attempts"][0]["is_negative"],
    "lesson_title":  lesson_review["new_attempts"][0]["lesson_title"],
    "lesson_url": lesson_review["new_attempts"][0]["lesson_url"]
    }



massage_accept = "Преподавателю понравилось, можно приступать к следующему уроку"
massage_task_no_accepted = "К сожалению в работе нашлись ошибки"
massage_task_checked = "У Вас проверили работу <<Отправляем уведомление о проверке работ>>"


async def send_message():
    await bot.send_message(text="Привет Дима", chat_id=chat_id)

