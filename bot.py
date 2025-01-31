import telegram


async def preparing_message(lesson_review: dict) -> str:
    '''Prepare result dict for send by telegram bot
    params:
        lesson_review: dict with result
    return:
        text massage for telegram bot
    '''
    result_review = (
        "К сожалению в работе нашлись ошибки",
        "Преподавателю понравилось, можно приступать к следующему уроку"
    )[lesson_review["check_status"]]
    massage = (
        f'У Вас проверили работу!\n\n'
        f'Урок: "{lesson_review["lesson_title"]}"\n'
        f'Ссылка на урок: {lesson_review["lesson_url"]}\n\n'
        f'Результат проверки: {result_review}'
    )
    return massage


async def send_message(
    tg_token: str,
    chat_id: str,
    lesson_review: dict
    ) -> None:
    '''Sand a massage to TG_Chat
    params:
        tg_token: telegram_bot token
        chat_id: telegram cat id
        lesson_review: dict with result
    '''
    message = await preparing_message(lesson_review)
    bot = telegram.Bot(token=tg_token)
    await bot.send_message(text=message, chat_id=chat_id)
