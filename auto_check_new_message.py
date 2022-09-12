import time

import telebot.apihelper
from requests import ReadTimeout
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import datebase_def


def new_message(vk_user_api, tg_id, bot):
    try:
        token = vk_user_api
        session = vk_api.VkApi(token=token)
        longpoll = VkLongPoll(session)
        for event in longpoll.listen():
            try:
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    curent_chat = session.method("messages.getConversationsById", {"peer_ids": event.peer_id})
                    dialog_type = curent_chat["items"][0]["peer"]["type"]
                    if dialog_type == "group":
                        message_sender = session.method("groups.getById",
                                                        {"group_id": curent_chat['items'][0]['peer']['local_id']})
                        message_sender_name = message_sender[0]["name"]
                        if 'push_settings' not in curent_chat['items'][0]:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender_name}")
                        elif curent_chat["items"][0]['push_settings']['disabled_forever'] is True:
                            continue
                        elif curent_chat["items"][0]['push_settings']['no_sound'] is True:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender_name}",
                                             disable_notification=True)

                    elif dialog_type == "chat":
                        message_sender = curent_chat['items'][0]['chat_settings']['title']
                        if 'push_settings' not in curent_chat['items'][0]:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender}")
                        elif curent_chat["items"][0]['push_settings']['disabled_forever'] is True:
                            continue
                        elif curent_chat["items"][0]['push_settings']['no_sound'] is True:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender}",
                                             disable_notification=True)

                    else:
                        message_sender = session.method("users.get",
                                                        {"user_ids": curent_chat['items'][0]['peer']['local_id']})
                        message_sender_name = (message_sender[0]["first_name"] + " " +
                                               message_sender[0]["last_name"])
                        if 'push_settings' not in curent_chat['items'][0]:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender_name}")
                        elif curent_chat["items"][0]['push_settings']['disabled_forever'] is True:
                            continue
                        elif curent_chat["items"][0]['push_settings']['no_sound'] is True:
                            bot.send_message(tg_id, f"У вас новое сообщение от {message_sender_name}",
                                             disable_notification=True)

            except KeyError:
                bot.send_message(tg_id, "У вас новое сообщение")
            except telebot.apihelper.ApiTelegramException as block:
                if block.description == "Forbidden: bot was blocked by the user":
                    datebase_def.unsubscribe(tg_id)
    except ReadTimeout:
        time.sleep(35)
    new_message(vk_user_api, tg_id, bot)
