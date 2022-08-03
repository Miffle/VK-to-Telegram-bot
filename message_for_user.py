import telebot.apihelper

import message_for_user_def


def get_last_message(session, count_of_chats, bot, markup, message):
    conversation_response = session.method("messages.getConversations", {"count": count_of_chats})
    for i in range(0, count_of_chats):
        try:
            current_conversation = conversation_response["items"][i]["conversation"]
            messages = None
            if (current_conversation["unread_count"]) != 0:
                conversation_type = current_conversation["peer"]["type"]
                if conversation_type == "chat":
                    messages = message_for_user_def.chat_message(current_conversation, session)
                elif conversation_type == "user":
                    messages = message_for_user_def.user_message(session, current_conversation)
                elif conversation_type == "group":
                    messages = message_for_user_def.group_message(session, current_conversation)

                if messages is not None:
                    if "vk.com" in messages.link:
                        bot.send_message(message, text=f"[__{messages.name}__]({messages.link}):", reply_markup=markup,
                                         disable_web_page_preview=True, parse_mode="MarkdownV2")
                    else:
                        bot.send_photo(message, photo=messages.link, caption=messages.name, reply_markup=markup)
                    
                    messages_to_send = messages.messages
                    size = len(messages_to_send)
                    current_message_num = 0
                    while current_message_num < size:
                        current_message: message_for_user_def.Message = messages_to_send[current_message_num]
                        bot.send_message(message, text=current_message.sender, reply_markup=markup)
                        if len(current_message.attachments) == 0:
                            if current_message.text != '':
                                bot.send_message(message, text=current_message.text, reply_markup=markup)
                        else:
                            send_attachments(current_message, bot, message, markup)
                        current_message_num += 1
        except KeyError:
            if i == count_of_chats - 1:
                bot.send_message(message, "Больше сообщений нет...", reply_markup=markup)
            continue



def send_attachments(current_message: message_for_user_def.Message, bot, message, markup):
    for attachment in current_message.attachments:
        if attachment.attachment_type == 'video':
            bot.send_message(message, text=attachment.attachment_link, reply_markup=markup)
        elif attachment.attachment_type == 'photo':
            bot.send_photo(message, photo=attachment.attachment_link, reply_markup=markup)
        elif attachment.attachment_type == 'audio':
            bot.send_audio(message, audio=attachment.attachment_link, reply_markup=markup)
        elif attachment.attachment_type == 'doc':
            try:
                bot.send_document(message, document=attachment.attachment_link, reply_markup=markup)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(message, text=f"[Документ]({attachment.attachment_link})", reply_markup=markup,
                                 parse_mode="MarkdownV2")
        elif attachment.attachment_type == 'audio_message':
            bot.send_voice(message, voice=attachment.attachment_link, reply_markup=markup)
        elif attachment.attachment_type == 'sticker':
            bot.send_photo(message, photo=attachment.attachment_link, reply_markup=markup)
        else:
            bot.send_message(message, text=attachment.attachment_link)
