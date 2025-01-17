import threading

import telebot
from django.conf import settings


bot = telebot.TeleBot(settings.TELEBOT_ID)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, f"Привет, чем я могу тебе помочь?{message.chat.id}")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def send_message_zapis(telegram_id: int, data: dict[str, str]):
    comment = data.get("comment", "")
    bot.send_message(
        telegram_id,
        f"Тип: {data['type']} \n"
        f"Сервер: {data['server']} \n"
        f"Фракция: {data['fraction']} \n"
        f"Класс: {data['class']} \n"
        f"Учитель: {data['mentor']} \n"
        f"Способ связи: {data['communication']} \n"
        f"Ник: {data['username']} \n"
        f"Комментарий: {comment}",
    )


class AsyncActionTelegramBot(threading.Thread):
    """Класс работающий не в основном потоке, который запускаем телеграмм бота"""

    def run(self):
        bot.polling(none_stop=True, interval=0)


# создаем экземпляр класса отправки меседжей
async_action_telegram_bot = AsyncActionTelegramBot()
async_action_telegram_bot.daemon = True
# async_action_telegram_bot.start()
