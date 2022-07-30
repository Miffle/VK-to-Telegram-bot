import Info
import last_message_def
import time


def get_last_message(session, count_of_chats):
    zz = session.method("messages.getConversations", {"count": count_of_chats})
    open('mes.txt', 'w').close()
    for i in range(0, count_of_chats):
        try:
            last_message_def.chat_message(zz, i)
        except KeyError:
            try:
                last_message_def.user_message(session, zz, i)
            except IndexError:
                last_message_def.group_message(session, zz, i)


def messag(bot, markup):
    f = open("mes.txt", "r")
    messages = f.read().splitlines()
    while True:
        for i in range(0, 10):
            bot.send_message(Info.chat_id, messages[i], reply_markup=markup, disable_web_page_preview=True)
            time.sleep(0.5)
        time.sleep(10)

