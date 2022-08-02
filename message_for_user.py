import telebot.apihelper

import message_for_user_def


def get_last_message(session, count_of_chats, bot, markup, message):
    zz = session.method("messages.getConversations", {"count": count_of_chats})
    for i in range(0, count_of_chats):
        try:
            current_conversation = zz["items"][i]
            messages = ()
            if (current_conversation["conversation"]["unread_count"]) != 0:
                conversation_type = current_conversation["conversation"]["peer"]["type"]
                if conversation_type == "chat":
                    messages = message_for_user_def.chat_message(current_conversation, session)
                elif conversation_type == "user":
                    messages = message_for_user_def.user_message(session, current_conversation)
                elif conversation_type == "group":
                    messages = message_for_user_def.group_message(session, current_conversation)

                if any(messages):
                    if "vk.com" in messages[3][0]:
                        bot.send_message(message, text=f"[__{messages[0]}__]({messages[3][0]}):", reply_markup=markup,
                                         disable_web_page_preview=True, parse_mode="MarkdownV2")
                    else:
                        bot.send_photo(message, photo=messages[3][0], caption=messages[0]  , reply_markup=markup)
                    size = len(messages[1])
                    current_message = 0
                    while current_message < size:
                        if messages[2][current_message] == messages[1][current_message]:
                            bot.send_message(message, text=messages[1][current_message], reply_markup=markup)
                        elif messages[2][current_message] == 'video':
                            bot.send_message(message, text=messages[1][current_message], reply_markup=markup)
                        elif messages[2][current_message] == 'photo':
                            bot.send_photo(message, photo=messages[1][current_message], reply_markup=markup)
                        elif messages[2][current_message] == 'audio':
                            bot.send_audio(message, audio=messages[1][current_message], reply_markup=markup)
                        elif messages[2][current_message] == 'doc':
                            try:
                                bot.send_document(message, document=messages[1][current_message], reply_markup=markup)
                            except telebot.apihelper.ApiTelegramException:
                                bot.send_message(message, text=f"[Документ]({messages[1][current_message]})", reply_markup=markup, parse_mode="MarkdownV2")
                        elif messages[2][current_message] == 'audio_message':
                            bot.send_voice(message, voice=messages[1][current_message], reply_markup=markup)
                        elif messages[2][current_message] == 'sticker':
                            bot.send_photo(message, photo=messages[1][current_message], reply_markup=markup)
                        else:
                            bot.send_message(message, text=messages[1][current_message])
                        current_message+=1
        except KeyError:
            if i == count_of_chats - 1:
                bot.send_message(message, "Больше сообщений нет...", reply_markup=markup)
            continue
