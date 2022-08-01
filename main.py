import telebot
import vk_api
from telebot import types
import datebase_def
import Info
import last_message
import bot_messages

bot = telebot.TeleBot(Info.TGbot_token, parse_mode=None)
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = types.KeyboardButton('Проверка сообщений')
itembtn2 = types.KeyboardButton('Подписаться')
itembtn3 = types.KeyboardButton('Отписаться')
itembtn4 = types.KeyboardButton('Помощь')
markup.add(itembtn2, itembtn4)
markup1.add(itembtn1, itembtn3, itembtn4)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        sub = datebase_def.sub_check(message.chat.id)
        if sub == True:
            bot.send_message(message.chat.id,
                             bot_messages.hello_reply,
                             reply_markup=markup1,
                             parse_mode="HTML")
        else:
            bot.send_message(message.chat.id,
                             bot_messages.hello_reply,
                             reply_markup=markup,
                             parse_mode="HTML")


@bot.message_handler(content_types=['text'])
def support(message):
    if message.chat.type == 'private':
        if message.text == 'Подписаться':
            send = bot.send_message(message.chat.id, "Отправь сюда API ключ", reply_markup=markup)
            bot.register_next_step_handler(send, get_api)
        elif message.text == 'Отписаться':
            bot.send_message(Info.chat_id, "Очень жаль, если что, то я всегда тут", reply_markup=markup)
            datebase_def.unsubscribe(message.chat.id)
        elif message.text == 'Помощь':
            sub = datebase_def.sub_check(message.chat.id)
            if sub == True:
                bot.send_message(message.chat.id,
                                 text=bot_messages.support_reply,
                                 reply_markup=markup1,
                                 parse_mode="HTML")
            else:
                bot.send_message(message.chat.id,
                                 text=bot_messages.support_reply,
                                 reply_markup=markup,
                                 parse_mode="HTML"
                                 )
        elif message.text == 'Проверка сообщений':
            sub = datebase_def.sub_check(message.chat.id)
            if sub == True:
                token = datebase_def.api_check(message.chat.id)
                session = vk_api.VkApi(token=token)
                last_message.get_last_message(session, 10, bot, markup1, message.chat.id)
            else:
                bot.send_message(message.chat.id, "Ты не подписался и не прислал токен!")


@bot.message_handler(content_types=['text'])
def get_api(message):
    if message.chat.type == 'private':
        if len(message.text) > 15:
            userid = message.chat.id
            vk_user_api = message.text
            datebase_def.insert_in_db(userid, vk_user_api)
            bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup1)


if __name__ == "__main__":
    bot.infinity_polling()
