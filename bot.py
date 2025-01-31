import telegram


async def preparing_message(lesson_review):
    if lesson_review["check_status"]:
        result = "Преподавателю понравилось, можно приступать к следующему уроку"
    else:
        result = "К сожалению в работе нашлись ошибки"
    massage = (
        f'У Вас проверили работу!\n\n'
        f'Урок: "{lesson_review["lesson_title"]}"\n'
        f'Ссылка на урок: {lesson_review["lesson_url"]}\n'
        f'Результат проверки: {result}'
    )
    return massage


async def send_message(tg_token, chat_id, lesson_review):
    message = await preparing_message(lesson_review)
    bot = telegram.Bot(token=tg_token)
    await bot.send_message(text=message, chat_id=chat_id)
