import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def new_message(vk_user_api, tg_id, bot):
    token = vk_user_api
    session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            curent_chat = session.method("messages.getConversationsById", {"peer_ids": event.peer_id})
            dialog_type = curent_chat["items"][0]["peer"]["type"]
            if dialog_type == "group" and "chat":
                if curent_chat["items"][0]['push_settings']['disabled_forever'] and \
                        curent_chat["items"][0]['push_settings']['no_sound'] is False:
                    bot.send_message(tg_id, "У вас новое сообщение")
            else:
                bot.send_message(tg_id, "У вас новое сообщение")
    new_message(vk_user_api, tg_id, bot)
