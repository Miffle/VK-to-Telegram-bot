import telebot
import vk_api
from telebot import types
import datebase_def
import Info
import message_for_user
import bot_messages
import reply_def

bot = telebot.TeleBot(Info.TGbot_token, parse_mode=None)
markup_with_subscription = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_without_subscription = types.ReplyKeyboardMarkup(resize_keyboard=True)

check_messages_button = types.KeyboardButton('Проверка сообщений')
subscribe_button = types.KeyboardButton('Подписаться')
write_button = types.KeyboardButton('Написать сообщение')
unsubscribe_button = types.KeyboardButton('Отписаться')
help_button = types.KeyboardButton('Помощь')

markup_without_subscription.add(subscribe_button, help_button)
markup_with_subscription.add(check_messages_button, unsubscribe_button, help_button, write_button)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        sub = datebase_def.sub_check(message.chat.id)
        if sub is True:
            bot.send_message(message.chat.id,
                             bot_messages.hello_reply,
                             reply_markup=markup_with_subscription,
                             parse_mode="HTML")
        else:
            bot.send_message(message.chat.id,
                             bot_messages.hello_reply,
                             reply_markup=markup_without_subscription,
                             parse_mode="HTML")


@bot.message_handler(content_types=['text'])
def support(message):
    if message.chat.type == 'private':
        if message.text == subscribe_button.text:
            send = bot.send_message(message.chat.id, "Отправь сюда API ключ", reply_markup=markup_without_subscription)
            bot.register_next_step_handler(send, get_api)
        elif message.text == unsubscribe_button.text:
            bot.send_message(Info.chat_id, "Очень жаль, если что, то я всегда тут",
                             reply_markup=markup_without_subscription)
            datebase_def.unsubscribe(message.chat.id)
        elif message.text == help_button.text:
            sub = datebase_def.sub_check(message.chat.id)
            if sub:
                bot.send_message(message.chat.id,
                                 text=bot_messages.support_reply,
                                 reply_markup=markup_with_subscription,
                                 parse_mode="HTML")
            else:
                bot.send_message(message.chat.id,
                                 text=bot_messages.support_reply,
                                 reply_markup=markup_without_subscription,
                                 parse_mode="HTML"
                                 )
        elif message.text == check_messages_button.text:
            sub = datebase_def.sub_check(message.chat.id)
            if sub is True:
                token = datebase_def.api_check(message.chat.id)
                session = vk_api.VkApi(token=token)
                message_for_user.get_last_message(session, 15, bot, markup_with_subscription, message.chat.id)
            else:
                bot.send_message(message.chat.id, "Ты не подписался и не прислал токен!")
        elif message.text == write_button.text:
            api_key = datebase_def.api_check(message.chat.id)
            session = vk_api.VkApi(token=api_key)
            names = reply_def.get_chats(message, session)
            bot.register_next_step_handler(message, processing, names, session)

        elif message.text == "Отмена":
            bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)


@bot.message_handler(content_types=['text'])
def get_api(message):
    if message.chat.type == 'private':
        if "vk1.a." in message.text:
            userid = message.chat.id
            vk_user_api = message.text
            datebase_def.insert_in_db(userid, vk_user_api)
            bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup_with_subscription)


@bot.message_handler(content_types=['text'])
def processing(message, names, session):
    if message.text == names[0][0]:
        bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][0]}*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, reply, names[1][0], session)
    elif message.text == names[0][1]:
        bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][1]}*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, reply, names[1][1], session)
    elif message.text == names[0][2]:
        bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][2]}*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, reply, names[1][2], session)
    elif message.text == names[0][3]:
        bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][3]}*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, reply, names[1][3], session)
    elif message.text == names[0][4]:
        bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][4]}*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, reply, names[1][4], session)


@bot.message_handler(content_types=['text'])
def reply(message, chat_id, session):
    if message.text != "Отмена":
        session.method("messages.send", {"peer_id": chat_id, "message": message.text, "random_id": 0})
        bot.send_message(message.chat.id, "Сообщение успешно отправлено!",
                         reply_markup=markup_with_subscription)

    else:
        bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)


if __name__ == "__main__":
    bot.infinity_polling()
