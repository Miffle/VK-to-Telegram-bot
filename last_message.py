import Info
import last_message_def
import time


def get_last_message(session, count_of_chats, bot, markup):
    zz = session.method("messages.getConversations", {"count": count_of_chats})
    open('mes.txt', 'w').close()
    for i in range(0, count_of_chats):
        try:
            current_conversation = zz["items"][i]
            messages = ()
            if (current_conversation["conversation"]["unread_count"]) != "":
                conversation_type = current_conversation["conversation"]["peer"]["type"]
                if conversation_type == "chat":
                    messages = last_message_def.chat_message(current_conversation, session)
                elif conversation_type == "user":
                    last_message_def.user_message(session, current_conversation)
                elif conversation_type == "group":
                    last_message_def.group_message(session, zz, i)

                if any(messages):
                    bot.send_message(Info.chat_id, messages[0], reply_markup=markup, disable_web_page_preview=True)
                    for current_message in messages[1]:
                        bot.send_message(Info.chat_id, current_message, reply_markup=markup, disable_web_page_preview=True)
        except KeyError:
            continue

