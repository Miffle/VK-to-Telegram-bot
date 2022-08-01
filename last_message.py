import last_message_def


def get_last_message(session, count_of_chats, bot, markup, message):
    zz = session.method("messages.getConversations", {"count": count_of_chats})
    for i in range(0, count_of_chats):
        try:
            current_conversation = zz["items"][i]
            messages = ()
            if (current_conversation["conversation"]["unread_count"]) != 0:
                conversation_type = current_conversation["conversation"]["peer"]["type"]
                if conversation_type == "chat":
                    messages = last_message_def.chat_message(current_conversation, session)
                elif conversation_type == "user":
                    messages = last_message_def.user_message(session, current_conversation)
                elif conversation_type == "group":
                    messages = last_message_def.group_message(session, current_conversation)

                if any(messages):
                    bot.send_message(message, text=f"__{messages[0]}:__", reply_markup=markup,
                                     disable_web_page_preview=False, parse_mode="MarkdownV2")
                    for current_message in messages[1]:
                        bot.send_message(message, current_message, reply_markup=markup, disable_web_page_preview=False)

        except KeyError:
            if i == count_of_chats - 1:
                bot.send_message(message, "Больше сообщений нет...", reply_markup=markup)
            continue
