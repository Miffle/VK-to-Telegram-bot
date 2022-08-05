from telebot import types

from main import bot


def get_chats(message, session):
    names = ([], [])
    '''
    У names 
    1 - Название
    2 - id
    '''
    chats_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conversation_response = session.method("messages.getConversations", {"count": 5})
    for current_chat in range(0, 5):
        current_conversation = conversation_response["items"][current_chat]["conversation"]
        conversation_type = current_conversation["peer"]["type"]
        if conversation_type == "chat":
            names[0].append(current_conversation["chat_settings"]["title"])
            names[1].append(current_conversation["peer"]["id"])
        elif conversation_type == "user":
            user = session.method("users.get", {"user_ids": current_conversation["peer"]["id"]})[0]
            names[0].append(user["first_name"] + " " + user["last_name"])
            names[1].append(user["id"])
        elif conversation_type == "group":
            group_local_id = current_conversation["peer"]["local_id"]
            group_id = current_conversation["peer"]["id"]
            group_name = session.method("groups.getById", {"group_id": group_local_id})
            names[0].append(group_name[0]["name"])
            names[1].append(group_id)
    first_chat_button = types.KeyboardButton(text=names[0][0])
    second_chat_button = types.KeyboardButton(text=names[0][1])
    third_chat_button = types.KeyboardButton(text=names[0][2])
    fourth_chat_button = types.KeyboardButton(text=names[0][3])
    fifth_chat_button = types.KeyboardButton(text=names[0][4])
    sixth_chat_button = types.KeyboardButton(text="Отмена")
    chats_markup.add(first_chat_button, second_chat_button, third_chat_button, fourth_chat_button, fifth_chat_button,
                     sixth_chat_button)
    if message.text == 'Написать сообщение':
        bot.send_message(message.chat.id, text="Кому ты хочешь написать?", reply_markup=chats_markup)
    elif message.text == 'Прочитать сообщения':
        bot.send_message(message.chat.id, "Какой диалог тебя интересует?", reply_markup=chats_markup)
    return names


def read_chat(message, session, names):
    mes = session.method("messages.getHistory", {"peer_id": names})
    for i in reversed(range(0, len(mes["items"]))):
        current_message = mes["items"][i]
        current_attachment = mes["items"][i]["attachments"]
        current_attachment_count = len(current_attachment)
        if mes['items'][i]['text'] != '':
            bot.send_message(message.chat.id, text=current_message["text"])
        else:
            for attachment in range(0, current_attachment_count):
                if current_attachment[attachment]["type"] == "audio":
                    bot.send_audio(message.chat.id, audio=current_attachment[attachment]["audio"]["url"],
                                   caption=(current_attachment[attachment]["audio"]["artist"] + " - " +
                                            current_attachment[attachment]["audio"]["title"]),
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "photo":
                    sizes = current_attachment[attachment]["photo"]["sizes"]
                    max_size = max(sizes, key=lambda size: size["height"])
                    bot.send_photo(message.chat.id, photo=max_size['url'],
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "video":
                    bot.send_message(message.chat.id, text=current_attachment[attachment]["video"]["player"],
                                     disable_notification=True)
                elif current_attachment[attachment]["type"] == "audio_message":
                    bot.send_voice(message.chat.id, voice=current_attachment[attachment]["audio_message"]["link_ogg"],
                                   disable_notification=True)
                elif current_attachment[attachment]["type"] == "doc":
                    bot.send_document(message.chat.id, document=current_attachment[attachment]["doc"]["url"],
                                      disable_notification=True)
    session.method("messages.markAsRead", {"peer_id": names})
