import threading

import telebot
import vk_api
from telebot import types

import joke_get
import reply_read_def
import auto_check_new_message
import datebase_def
import Info
import bot_messages
import donate

bot = telebot.TeleBot(Info.TGbot_token, parse_mode=None)

markup_with_subscription = types.ReplyKeyboardMarkup(resize_keyboard=True)
write_button = types.KeyboardButton('Написать сообщение')
read_button = types.KeyboardButton("Прочитать сообщения")
unsubscribe_button = types.KeyboardButton('Отписаться')
help_button = types.KeyboardButton('Помощь')
donate_button = types.KeyboardButton('Дать деньги')
markup_with_subscription.row(write_button, read_button)
markup_with_subscription.row(help_button, unsubscribe_button, donate_button)

markup_without_subscription = types.ReplyKeyboardMarkup(resize_keyboard=True)
subscribe_button = types.KeyboardButton('Подписаться')
markup_without_subscription.add(subscribe_button, help_button)

yes_button = types.KeyboardButton('Да')
no_button = types.KeyboardButton('Нет')
yes_no_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(yes_button, no_button)

yandex_button = types.InlineKeyboardButton(text="yoomoney", url=donate.yoomoney_url)
donationalerts_button = types.InlineKeyboardButton(text="Donation Alerts", url=donate.donationalerts_url)
qiwi_button = types.InlineKeyboardButton(text="QIWI", url=donate.qiwi_url)
donate_markup = types.InlineKeyboardMarkup().add(qiwi_button, yandex_button, donationalerts_button)

markup_with_url = types.InlineKeyboardMarkup()
btn_my_site = types.InlineKeyboardButton(text='Дать разрешение', url=(
    "https://oauth.vk.com/authorize?client_id=6121396&scope=593920&redirect_uri=https://oauth.vk.com/blank.html&displa"
    "y=page&response_type=token&revoke=1"))
markup_with_url.add(btn_my_site)

datebase_def.renew_polling_threads(bot)


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
        sub = datebase_def.sub_check(message.chat.id)
        if message.text == subscribe_button.text:
            send = bot.send_message(message.chat.id,
                                    "Отправь сюда <ins>ссылку</ins> со страницы, на которой написано:\n"
                                    "'Пожалуйста, не копируйте данные из адресной строки...'\nДа-да)",
                                    reply_markup=markup_with_url, parse_mode="HTML")
            bot.register_next_step_handler(send, get_api)
        elif message.text == unsubscribe_button.text:
            bot.send_message(message.chat.id, "Очень жаль, если что, то я всегда тут",
                             reply_markup=markup_without_subscription)
            datebase_def.unsubscribe(message.chat.id)
        elif message.text == help_button.text:
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
        elif message.text == write_button.text:
            if sub:
                api_key = datebase_def.api_check(message.chat.id)
                session = vk_api.VkApi(token=api_key)
                names = reply_read_def.get_all_chats(message, session, bot)
                bot.register_next_step_handler(message, processing, names, session)
            else:
                bot.send_message(message.chat.id, "Ты не подписался и не прислал токен!")
        elif message.text == donate_button.text:
            bot.send_message(message.chat.id, "Деньги даются сюда:", reply_markup=donate_markup)
        elif message.text == read_button.text:
            if sub is True:
                api_key = datebase_def.api_check(message.chat.id)
                session = vk_api.VkApi(token=api_key)
                names = reply_read_def.get_all_chats(message, session, bot)
                bot.register_next_step_handler(message, chat_reading, names, session)
            elif message.text == "Отмена":
                bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)
            else:
                bot.send_message(message.chat.id, "Ты не подписался и не прислал токен!")
        else:
            rand_anekdot = joke_get.get_joke()
            if sub:
                bot.send_message(message.chat.id,
                                 f"Я такое не понимаю(нажимай на кнопки), но вот рандомный"
                                 f" анекдот\n\n\n{rand_anekdot[1]}\n\n"
                                 f"(Оригинальная версия, если проблемы с переводом)\n\n"
                                 f"{rand_anekdot[0]}",
                                 reply_markup=markup_with_subscription)
            else:
                bot.send_message(message.chat.id,
                                 f"Я такое не понимаю(нажимай на кнопки), но вот рандомный"
                                 f" анекдот\n\n\n{rand_anekdot[1]}\n\n"
                                 f"(Оригинальная версия, если проблемы с переводом)\n\n"
                                 f"{rand_anekdot[0]}",
                                 reply_markup=markup_without_subscription)


@bot.message_handler(content_types=['text'])
def get_api(message):
    if message.chat.type == 'private':
        if ("=" and "&") in message.text:
            if "vk1.a." in message.text:
                userid = message.chat.id
                vk_user_api_url = message.text
                vk_user_api = vk_user_api_url[vk_user_api_url.find("=") + 1: vk_user_api_url.find("&")]
                datebase_def.insert_in_db(userid, vk_user_api)
                bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup_with_subscription)
                threading.Thread.start(auto_check_new_message.new_message(vk_user_api, userid, bot))
            else:
                bot.send_message(message.chat.id, "Мимо, давай ещё разок(Нажав на кнопку 'Подписаться')",
                                 reply_markup=markup_without_subscription)
        else:
            bot.send_message(message.chat.id, "Мимо, давай ещё разок(Нажав на кнопку 'Подписаться')",
                             reply_markup=markup_without_subscription)


@bot.message_handler(content_types=['text'])
def processing(message, names, session):
    if message.text != "Отмена":
        if message.text == (names[0][0] + f"({names[2][0]})"):
            bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][0]}*", parse_mode="MarkdownV2")
            bot.register_next_step_handler(message, reply, names[1][0], session)
        elif message.text == (names[0][1] + f"({names[2][1]})"):
            bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][1]}*", parse_mode="MarkdownV2")
            bot.register_next_step_handler(message, reply, names[1][1], session)
        elif message.text == (names[0][2] + f"({names[2][2]})"):
            bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][2]}*", parse_mode="MarkdownV2")
            bot.register_next_step_handler(message, reply, names[1][2], session)
        elif message.text == (names[0][3] + f"({names[2][3]})"):
            bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][3]}*", parse_mode="MarkdownV2")
            bot.register_next_step_handler(message, reply, names[1][3], session)
        elif message.text == (names[0][4] + f"({names[2][4]})"):
            bot.send_message(message.chat.id, f"Пиши сообщение для *{names[0][4]}*", parse_mode="MarkdownV2")
            bot.register_next_step_handler(message, reply, names[1][4], session)
    else:
        bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)


@bot.message_handler(content_types=['text'])
def reply(message, chat_id, session):
    if message.text is not None:
        if message.text != "Отмена":
            session.method("messages.send", {"peer_id": chat_id, "message": message.text, "random_id": 0})
            bot.send_message(message.chat.id, "Сообщение успешно отправлено!",
                             reply_markup=markup_with_subscription)

        else:
            bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)
    else:
        bot.send_message(message.chat.id, "Не-не, я андерстенд только текст(возможно пока)",
                         reply_markup=markup_with_subscription)


@bot.message_handler(content_types=['text'])
def chat_reading(message, names, session):
    if message.text != "Отмена":
        if message.text == (names[0][0] + f"({names[2][0]})"):
            reply_read_def.read_chat(message, session, names[1][0], bot, names[2][0])
            bot.send_message(message.chat.id, "Отметить прочитанным?", reply_markup=yes_no_markup)
            bot.register_next_step_handler(message, reading, session, names[1][0])
        elif message.text == (names[0][1] + f"({names[2][1]})"):
            reply_read_def.read_chat(message, session, names[1][1], bot, names[2][1])
            bot.send_message(message.chat.id, "Отметить прочитанным?", reply_markup=yes_no_markup)
            bot.register_next_step_handler(message, reading, session, names[1][1])
        elif message.text == (names[0][2] + f"({names[2][2]})"):
            reply_read_def.read_chat(message, session, names[1][2], bot, names[2][2])
            bot.send_message(message.chat.id, "Отметить прочитанным?", reply_markup=yes_no_markup)
            bot.register_next_step_handler(message, reading, session, names[1][2])
        elif message.text == (names[0][3] + f"({names[2][3]})"):
            reply_read_def.read_chat(message, session, names[1][3], bot, names[2][3])
            bot.send_message(message.chat.id, "Отметить прочитанным?", reply_markup=yes_no_markup)
            bot.register_next_step_handler(message, reading, session, names[1][3])
        elif message.text == (names[0][4] + f"({names[2][4]})"):
            reply_read_def.read_chat(message, session, names[1][4], bot, names[2][4])
            bot.send_message(message.chat.id, "Отметить прочитанным?", reply_markup=yes_no_markup)
            bot.register_next_step_handler(message, reading, session, names[1][4])

    else:
        bot.send_message(message.chat.id, "Ок", reply_markup=markup_with_subscription)


@bot.message_handler(content_types=['text'])
def reading(message, session, names):
    text = message.text
    if text == "Да":
        session.method("messages.markAsRead", {"peer_id": names})
        bot.send_message(message.chat.id, "Отметил", reply_markup=markup_with_subscription)
    else:
        bot.send_message(message.chat.id, "Ок, не буду", reply_markup=markup_with_subscription)


bot.infinity_polling()
