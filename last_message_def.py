def group_message(session, zz, i):
    f = open("mes.txt", "a+")
    """Читает последнее сообщение группы из диалогов"""

    """ Получает ID группы, которая написала сообщение"""

    group_id = session.method("groups.getById",
                              {"group_id": zz["items"][i]["conversation"]["peer"]["local_id"]})

    """ 
    Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения
    """

    if zz["items"][i]["last_message"]["text"] != "":
        print((group_id[0]["name"] + ":"), file=f, flush=True)
        group_last_mes = zz["items"][i]["conversation"]["last_conversation_message_id"]
        group_unread_count = zz["items"][i]["conversation"]["unread_count"]
        start = (group_last_mes - group_unread_count)+1
        for k in range(start, group_last_mes):
            mes = (session.method("messages.getByConversationMessageId",
                                  {"peer_id": group_id, "conversation_message_ids": k}))
            print(mes["items"][0]["text"], file=f, flush=True)
    else:
        print((group_id[0]["name"] + " | " + zz["items"][i]["last_message"]["attachments"][0]["type"]), file=f,
              flush=True)


def user_message(session, current_conversation):
    """Читает последнее сообщение юзера из диалогов"""
    f = open("mes.txt", "a+")
    """Получает id пользователя который написал сообщение"""

    c = session.method("users.get", {"user_ids": current_conversation["conversation"]["peer"]["id"]})

    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    if current_conversation["last_message"]["text"] != "":
        print((c[0]["first_name"] + ' ' + c[0]["last_name"] + ":"), file=f,
              flush=True)
        user_id = current_conversation["conversation"]["peer"]["id"]
        user_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
        user_unread_count = current_conversation["conversation"]["unread_count"]
        start = (user_last_mes - user_unread_count) + 1
        for current_message_id in range(start, user_last_mes+1):
            mes = (session.method("messages.getByConversationMessageId",
                                  {"peer_id": user_id, "conversation_message_ids": current_message_id}))
            print(mes["items"][0]["text"], file=f, flush=True)
    else:
        print((c[0]["first_name"] + ' ' + c[0]["last_name"] + " | " +
               current_conversation["last_message"]["attachments"][0]["type"]), file=f, flush=True)


def chat_message(current_conversation, session):
    """Читает последнее сообщение в чате из диалогов"""
    f = open("mes.txt", "a+")
    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    chat_messages = ((current_conversation["conversation"]["chat_settings"]["title"]), [])

    if current_conversation["last_message"]["text"] != "":
        # print((
        #         current_conversation["conversation"]["chat_settings"]["title"] + ":"), file=f, flush=True)
        chat_id = current_conversation["conversation"]["peer"]["id"]
        chat_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
        chat_unread_count = current_conversation["conversation"]["unread_count"]
        start = (chat_last_mes - chat_unread_count) + 1
        for current_message_id in range(start, chat_last_mes+1):
            """Несколько id"""
            mes = (session.method("messages.getByConversationMessageId",
                                  {"peer_id": chat_id, "conversation_message_ids": current_message_id}))
            user = (session.method("users.get", {"user_ids": mes["items"][0]["from_id"]}))
            chat_messages[1].append((user[0]["first_name"] + ' ' + user[0]["last_name"] + ": ") + mes["items"][0]["text"])
            # print(((user[0]["first_name"] + ' ' + user[0]["last_name"] + ": ") + mes["items"][0]["text"]), file=f, flush=True)
    else:
        # print((current_conversation["conversation"]["chat_settings"]["title"] + " | " +
        #        current_conversation["last_message"]["attachments"][0]["type"]), file=f, flush=True)
        chat_messages[1].append(current_conversation["conversation"]["chat_settings"]["title"] + " | " +
                                current_conversation["last_message"]["attachments"][0]["type"])
    return chat_messages

