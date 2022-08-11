from telebot import types
import telebot.apihelper


def get_all_chats(message, session, bot):
    names = ([], [], [])
    '''
    У names 
    1 - Название
    2 - id
    3 - Кол-во непрочитанных
    '''
    chats_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conversation_response = session.method("messages.getConversations", {"count": 10})

    for current_chat in range(0, 10):
        try:
            current_conversation = conversation_response["items"][current_chat]["conversation"]
            conversation_type = current_conversation["peer"]["type"]
            if conversation_type == "chat":
                names[0].append(current_conversation["chat_settings"]["title"])
                names[1].append(current_conversation["peer"]["id"])
                if current_conversation['in_read_cmid'] != current_conversation['out_read_cmid']:
                    names[2].append(current_conversation['unread_count'])
                else:
                    names[2].append("0")
            elif conversation_type == "user":
                user = session.method("users.get", {"user_ids": current_conversation["peer"]["id"]})[0]
                names[0].append(user["first_name"] + " " + user["last_name"])
                names[1].append(user["id"])
                if current_conversation['in_read_cmid'] != current_conversation['out_read_cmid']:
                    names[2].append(current_conversation['unread_count'])
                else:
                    names[2].append("0")
            elif conversation_type == "group":
                group_local_id = current_conversation["peer"]["local_id"]
                group_id = current_conversation["peer"]["id"]
                group_name = session.method("groups.getById", {"group_id": group_local_id})
                names[0].append(group_name[0]["name"])
                names[1].append(group_id)
                if current_conversation['in_read_cmid'] != current_conversation['out_read_cmid']:
                    names[2].append(current_conversation['unread_count'])
                else:
                    names[2].append("0")
        except KeyError:
            names[2].append('0')

    first_chat_button = types.KeyboardButton(text=(names[0][0] + f"({names[2][0]})"))
    second_chat_button = types.KeyboardButton(text=(names[0][1] + f"({names[2][1]})"))
    third_chat_button = types.KeyboardButton(text=(names[0][2] + f"({names[2][2]})"))
    fourth_chat_button = types.KeyboardButton(text=(names[0][3] + f"({names[2][3]})"))
    fifth_chat_button = types.KeyboardButton(text=(names[0][4] + f"({names[2][4]})"))
    sixth_chat_button = types.KeyboardButton(text=(names[0][5] + f"({names[2][5]})"))
    seventh_chat_button = types.KeyboardButton(text=(names[0][6] + f"({names[2][6]})"))
    eighth_chat_button = types.KeyboardButton(text=(names[0][7] + f"({names[2][7]})"))
    ninth_chat_button = types.KeyboardButton(text=(names[0][8] + f"({names[2][8]})"))
    tenth_chat_button = types.KeyboardButton(text=(names[0][9] + f"({names[2][9]})"))
    eleventh_chat_button = types.KeyboardButton(text="Отмена")
    chats_markup.add(first_chat_button, second_chat_button, third_chat_button, fourth_chat_button, fifth_chat_button,
                     sixth_chat_button, seventh_chat_button, eighth_chat_button, ninth_chat_button, tenth_chat_button,
                     eleventh_chat_button)
    if message.text == 'Написать сообщение':
        bot.send_message(message.chat.id, text="Кому ты хочешь написать?", reply_markup=chats_markup)
    elif message.text == 'Прочитать сообщения':
        bot.send_message(message.chat.id, "Какой диалог тебя интересует?", reply_markup=chats_markup)
    return names


def read_chat(message, session, names, markup_with_subscription, bot):
    mes = session.method("messages.getHistory", {"peer_id": names, "count": 15})
    dialog = session.method("messages.getConversationsById", {"peer_ids": names})
    dialog_type = dialog["items"][0]["peer"]["type"]
    group_local_id = dialog["items"][0]["peer"]["local_id"]
    for i in reversed(range(0, len(mes["items"]))):
        current_message = mes["items"][i]
        if dialog_type == "group":
            message_sender = session.method("groups.getById", {"group_id": group_local_id})
            message_sender_name = message_sender[0]["name"]
        else:
            message_sender = session.method("users.get", {"user_ids": current_message["from_id"]})
            message_sender_name = message_sender[0]["first_name"] + " " + message_sender[0]["last_name"]
        current_attachment = mes["items"][i]["attachments"]
        current_attachment_count = len(current_attachment)
        if current_attachment_count == 0 and 'reply_message' not in mes["items"][i] and len(current_message["fwd_messages"]) == 0:
            bot.send_message(message.chat.id, text=(f'<b>{message_sender_name}:</b> \n' + current_message["text"]),
                             parse_mode='HTML', reply_markup=markup_with_subscription, disable_notification=True)
        elif 'reply_message' in mes["items"][i]:
            replied_message_sender_id = session.method("users.get", {"user_ids": current_message['reply_message']['from_id']})
            replied_message_sender_name = replied_message_sender_id[0]["first_name"] + " " + replied_message_sender_id[0]["last_name"]
            replied_message_text = current_message['reply_message']['text']
            bot.send_message(message.chat.id, text=(f"<b>{message_sender_name}:</b>  {current_message['text']}\n"
                                                    f"\t↩️️{replied_message_sender_name}: {replied_message_text}"),
                             parse_mode="HTML")
        elif len(current_message['fwd_messages']) != 0:
            for fwd_messages in range(0, len(current_message['fwd_messages'])):
                forward_message_sender_id = session.method("users.get",
                                                           {"user_ids": current_message['fwd_messages'][fwd_messages]['from_id']})
                forward_message_sender_name = forward_message_sender_id[0]["first_name"] + " " + \
                                              forward_message_sender_id[0]["last_name"]
                fwd_messages_text = current_message['fwd_messages'][fwd_messages]['text']
                bot.send_message(message.chat.id, text=(f"<b>{message_sender_name}:</b>  {current_message['text']}\n"
                                                        f"\t📩 {forward_message_sender_name}: {fwd_messages_text}"),
                                 parse_mode="HTML")
        else:
            for attachment in range(0, current_attachment_count):
                if current_attachment[attachment]["type"] == "audio":
                    bot.send_audio(message.chat.id, audio=current_attachment[attachment]["audio"]["url"],
                                   caption=(current_attachment[attachment]["audio"][
                                                "artist"] + " - " +
                                            current_attachment[attachment]["audio"][
                                                "title"] + "\n" + f"<b>{message_sender_name}:</b> " + current_message[
                                                'text']),
                                   disable_notification=True, parse_mode="HTML")
                elif current_attachment[attachment]["type"] == "photo":
                    sizes = current_attachment[attachment]["photo"]["sizes"]
                    max_size = max(sizes, key=lambda size: size["height"])
                    bot.send_photo(message.chat.id, photo=max_size['url'],
                                   caption=f"<b>{message_sender_name}:</b> " + current_message['text'],
                                   disable_notification=True, parse_mode="HTML")
                elif current_attachment[attachment]["type"] == "video":
                    bot.send_message(message.chat.id,
                                     text=(f"<b>{message_sender_name}:</b> " + current_message['text'] + '\n' +
                                           f'<a href="{current_attachment[attachment]["video"]["player"]}">Видео</a>'),
                                     parse_mode="HTML",
                                     disable_notification=True,
                                     disable_web_page_preview=False)
                elif current_attachment[attachment]["type"] == "audio_message":
                    bot.send_voice(message.chat.id, voice=current_attachment[attachment]["audio_message"]["link_ogg"],
                                   caption=f"<b>{message_sender_name}:</b> " +
                                           current_message['text'], parse_mode="HTML",
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "doc":
                    doc_url = current_attachment[attachment]["doc"]["url"]
                    try:
                        bot.send_document(message.chat.id, document=current_attachment[attachment]["doc"]["url"],
                                          caption=f"<b>{message_sender_name}:</b> " +
                                                  current_message['text'], parse_mode="HTML",
                                          disable_notification=True)
                    except telebot.apihelper.ApiTelegramException:
                        bot.send_message(message.chat.id,
                                         text=f"[Документ]({doc_url})" + '\n' + f"<b>{message_sender_name}:</b> " +
                                              current_message['text'],
                                         parse_mode="MarkdownV2", disable_notification=True)
                elif current_attachment[attachment]["type"] == "sticker":
                    bot.send_photo(message.chat.id, photo=current_attachment[attachment]["sticker"]["images"][2]["url"],
                                   caption=f"<b>{message_sender_name}</b>", parse_mode="HTML",
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "gift":
                    bot.send_photo(message.chat.id, photo=current_attachment[attachment]["gift"]["thumb_256"],
                                   caption=f"<b>{message_sender_name}:</b> "+current_message['text'], parse_mode="HTML",
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "link":
                    bot.send_message(message.chat.id,
                                     text=(
                                             f"*{message_sender_name}:* " +
                                             f"[Ссылка]({current_attachment[attachment]['link']['url']})"),
                                     parse_mode="MarkdownV2",
                                     disable_notification=True)
                elif current_attachment[attachment]["type"] == "wall":
                    bot.send_message(message.chat.id,
                                     text=(
                                             f"*{message_sender_name}:* " +
                                             f"[Пост](vk.com/wall{current_attachment[attachment]['wall']['from_id']}_"
                                             f"{current_attachment[attachment]['wall']['id']})"),
                                     parse_mode="MarkdownV2",
                                     disable_notification=True)
                else:
                    bot.send_message(message.chat.id,
                                     text=(f"<b>{message_sender_name}:</b> " + current_attachment[attachment]["type"]),
                                     parse_mode="HTML")
    session.method("messages.markAsRead", {"peer_id": names})
