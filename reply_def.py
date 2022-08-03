from telebot import types


def get_chats(message, session, api_key):
    chats_markup = types.InlineKeyboardMarkup
    conversation_response = session.method("messages.getConversations", {"count": 5})
    names = []
    for current_chat in range(0, 5):
        current_conversation = conversation_response["items"][current_chat]["conversation"]
        conversation_type = current_conversation["peer"]["type"]
        if conversation_type == "chat":
            names.append(current_conversation["chat_settings"]["title"])
        elif conversation_type == "user":
            user = session.method("users.get", {"user_ids": current_conversation["peer"]["id"]})[0]
            names.append(user["first_name"] + " " + user["last_name"])
        elif conversation_type == "group":
            group_local_id = current_conversation["peer"]["local_id"]
            group_name = session.method("groups.getById", {"group_id": group_local_id})
            names.append(group_name[0]["name"])

    first_chat_button = names[0]
    second_chat_button = names[1]
    third_chat_button = names[2]
    fourth_chat_button = names[3]
    fifth_chat_button = names[4]
    chats_markup.add(first_chat_button, second_chat_button, third_chat_button, fourth_chat_button, fifth_chat_button)
