from telebot import types
import vk_api
import telebot
import Info
import last_message
import time
import threading

session = vk_api.VkApi(token=Info.vk_TOKEN)
vk = session.get_api()
bot = telebot.TeleBot(Info.TGbot_token, parse_mode=None)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = types.KeyboardButton('Проверка сообщений')
itembtn2 = types.KeyboardButton('Помощь')
markup.add(itembtn1, itembtn2)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(Info.chat_id,
                     "Привет, думаю, что ты уже знаешь функционал, но, если нет, то можешь нажать на кнопку 'Помощь' 😄",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def support(message):
    if message.chat.type == 'private':
        if message.text == 'Помощь':
            bot.send_message(Info.chat_id, "lalalala", reply_markup=markup)
        if message.text == 'Проверка сообщений':
            last_message.get_last_message(session, 10, bot, markup)
            f = open("mes.txt", "r")
            messages = f.read().splitlines()
            for i in range(0, len(messages)):
                bot.send_message(Info.chat_id, messages[i], reply_markup=markup, disable_web_page_preview=True)
                time.sleep(0.5)
            # threading.Thread.start(last_message.messag(bot, markup, session))


if __name__ == "__main__":
    bot.infinity_polling()
