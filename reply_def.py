from telebot import types

from main import bot


def get_chats(message, session):
    names = ([], [])
    '''
    У names 
    1 - Название
    2 - id
    3 - Тип
    4 - id последнего сообщения
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
    bot.send_message(message.chat.id, text="Кому ты хочешь написать?", reply_markup=chats_markup)
    return names
