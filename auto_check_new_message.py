
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def new_message(vk_user_api, tg_id, bot):
    token = vk_user_api
    session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot.send_message(tg_id, "У вас новое сообщение")
    new_message(vk_user_api, tg_id, bot)
