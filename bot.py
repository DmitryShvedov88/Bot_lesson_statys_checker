import telegram


async def preparing_message(lesson_review_data: dict) -> str:
    '''Prepare result dict for send by telegram bot
    params:
        lesson_review_data: dict with data
    return:
        text massage for telegram bot
    '''
    result_review = (
        "К сожалению в работе нашлись ошибки",
        "Преподавателю понравилось, можно приступать к следующему уроку"
    )[lesson_review_data["new_attempts"][0]["is_negative"]]
    massage = (
        f'У Вас проверили работу!\n\n'
        f'Урок: "{lesson_review_data["new_attempts"][0]["lesson_title"]}"\n'
        f'Ссылка на урок: {lesson_review_data["new_attempts"][0]["lesson_url"]}\n\n'
        f'Результат проверки: {result_review}'
    )
    return massage


async def send_message(
    tg_token: str,
    chat_id: str,
    lesson_review_data: dict
    ) -> None:
    '''Sand a massage to TG_Chat
    params:
        tg_token: telegram_bot token
        chat_id: telegram cat id
        lesson_review: dict with result
    '''
    message = await preparing_message(lesson_review_data)
    bot = telegram.Bot(token=tg_token)
    await bot.send_message(text=message, chat_id=chat_id)
