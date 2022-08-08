import telebot.apihelper
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import datebase_def


def new_message(vk_user_api, tg_id, bot):
    token = vk_user_api
    session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(session)
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                curent_chat = session.method("messages.getConversationsById", {"peer_ids": event.peer_id})
                dialog_type = curent_chat["items"][0]["peer"]["type"]
                if dialog_type == "group":
                    if (curent_chat["items"][0]['push_settings']['disabled_forever'] is False) or \
                            (curent_chat["items"][0]['push_settings']['no_sound'] is False):
                        bot.send_message(tg_id, "У вас новое сообщение")
                elif dialog_type == "chat":
                    if (curent_chat["items"][0]['push_settings']['disabled_forever'] is False) or \
                            (curent_chat["items"][0]['push_settings']['no_sound'] is False):
                        bot.send_message(tg_id, "У вас новое сообщение")
                else:
                    bot.send_message(tg_id, "У вас новое сообщение")
        except KeyError:
            bot.send_message(tg_id, "У вас новое сообщение")
        except telebot.apihelper.ApiTelegramException as block:
            if block.description == "Forbidden: bot was blocked by the user":
                datebase_def.unsubscribe(tg_id)
    new_message(vk_user_api, tg_id, bot)
