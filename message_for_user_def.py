def group_message(session, current_conversation):
    """Читает последнее сообщение группы из диалогов"""

    """ Получает ID группы, которая написала сообщение"""
    group_local_id = current_conversation["conversation"]["peer"]["local_id"]
    group_id = current_conversation["conversation"]["peer"]["id"]
    group_name = session.method("groups.getById", {"group_id": group_local_id})

    """ 
    Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения
    """
    group_messages = (group_name[0]["name"], [], [], ["vk.com/club" + str(group_local_id)])

    group_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
    group_unread_count = current_conversation["conversation"]["unread_count"]
    start = (group_last_mes - group_unread_count) + 1
    for current_message_id in range(start, group_last_mes + 1):
        mes = (session.method("messages.getByConversationMessageId",
                              {"peer_id": group_id, "conversation_message_ids": current_message_id}))
        count = len(mes['items'][0]['attachments'])
        attachment_number = 0
        if mes["items"][0]["text"] != "":
            group_messages[1].append(mes["items"][0]["text"])
            group_messages[2].append(
                mes["items"][0]['text'])
        else:
            while attachment_number < count:
                attachment_type = mes["items"][0]["attachments"][attachment_number]["type"]
                if mes["items"][0]["attachments"][attachment_number]["type"] == "video":
                    group_messages[1].append((
                        mes["items"][0]["attachments"][attachment_number]["video"]["player"]))
                    group_messages[2].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "type"])
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "photo":
                    sizes = mes["items"][0]["attachments"][attachment_number]["photo"]["sizes"]
                    max_size = max(sizes, key=lambda size: size["height"])
                    group_messages[1].append(max_size["url"])

                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio_message":
                    group_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio_message"]["link_ogg"]))
                    group_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio":
                    group_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio"]["url"]))
                    group_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "doc":
                    group_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "doc"]["url"])
                    group_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "sticker":
                    group_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "sticker"]["images_with_background"][2]["url"])
                    group_messages[2].append(attachment_type)
                else:
                    group_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "type"])
                    group_messages[2].append(attachment_type)
                attachment_number += 1
    return group_messages


def user_message(session, current_conversation):
    """Читает последнее сообщение юзера из диалогов"""
    """Получает id пользователя который написал сообщение"""
    c = session.method("users.get", {"user_ids": current_conversation["conversation"]["peer"]["id"]})

    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    user_id = current_conversation["conversation"]["peer"]["id"]
    user_messages = (c[0]["first_name"] + " " + c[0]["last_name"], [], [], ["vk.com/id" + str(user_id)])
    user_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
    user_unread_count = current_conversation["conversation"]["unread_count"]
    start = (user_last_mes - user_unread_count) + 1
    for current_message_id in range(start, user_last_mes + 1):
        mes = (session.method("messages.getByConversationMessageId",
                              {"peer_id": user_id, "conversation_message_ids": current_message_id}))
        count = len(mes['items'][0]['attachments'])
        attachment_number = 0
        if mes["items"][0]["text"] != "":

            user_messages[1].append(mes["items"][0]["text"])
            user_messages[2].append(
                mes["items"][0]['text'])
        else:
            while attachment_number < count:
                attachment_type = mes["items"][0]["attachments"][attachment_number]["type"]
                if mes["items"][0]["attachments"][attachment_number]["type"] == "video":
                    user_messages[1].append((
                        mes["items"][0]["attachments"][attachment_number]["video"]["player"]))
                    user_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "photo":
                    sizes = mes["items"][0]["attachments"][attachment_number]["photo"]["sizes"]
                    max_size = max(sizes, key=lambda size: size["height"])
                    user_messages[1].append(max_size["url"])
                    user_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio_message":
                    user_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio_message"]["link_ogg"]))
                    user_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio":
                    user_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio"]["url"]))
                    user_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "doc":
                    user_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "doc"]["url"])
                    user_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "sticker":
                    user_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "sticker"]["images_with_background"][2]["url"])
                    user_messages[2].append(attachment_type)
                else:
                    user_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "type"])
                    user_messages[2].append(attachment_type)
                attachment_number += 1

    return user_messages


def chat_message(current_conversation, session):
    """Читает последнее сообщение в чате из диалогов"""
    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""
    chat_messages = ((current_conversation["conversation"]["chat_settings"]["title"]), [], [],
                     [current_conversation["conversation"]["chat_settings"]["photo"]["photo_200"]])

    chat_id = current_conversation["conversation"]["peer"]["id"]
    chat_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
    chat_unread_count = current_conversation["conversation"]["unread_count"]
    start = (chat_last_mes - chat_unread_count) + 1

    for current_message_id in range(start, chat_last_mes + 1):
        mes = (session.method("messages.getByConversationMessageId",
                              {"peer_id": chat_id, "conversation_message_ids": current_message_id}))
        user = (session.method("users.get", {"user_ids": mes["items"][0]["from_id"]}))
        count = len(mes['items'][0]['attachments'])
        attachment_number = 0
        if mes["items"][0]["text"] != "":
            """Несколько id"""
            chat_messages[1].append(
                (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + mes["items"][0]["text"])
            chat_messages[2].append(
                (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + mes["items"][0]["text"])

        else:
            while attachment_number < count:
                attachment_type = mes["items"][0]["attachments"][attachment_number]["type"]
                if mes["items"][0]["attachments"][attachment_number]["type"] == "video":
                    chat_messages[1].append((
                        mes["items"][0]["attachments"][attachment_number]["video"]["player"]))
                    chat_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "photo":
                    sizes = mes["items"][0]["attachments"][attachment_number]["photo"]["sizes"]
                    max_size = max(sizes, key=lambda size: size["height"])
                    chat_messages[1].append(max_size["url"])
                    chat_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio_message":
                    chat_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio_message"]["link_ogg"]))
                    chat_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "audio":
                    chat_messages[1].append(
                        (mes["items"][0]["attachments"][attachment_number]["audio"]["url"]))
                    chat_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "doc":
                    chat_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "doc"]["url"])
                    chat_messages[2].append(attachment_type)
                elif mes["items"][0]["attachments"][attachment_number]["type"] == "sticker":
                    chat_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "sticker"]["images_with_background"][2]["url"])
                    chat_messages[2].append(attachment_type)
                else:
                    chat_messages[1].append(
                        mes["items"][0]["attachments"][attachment_number][
                            "type"])
                    chat_messages[2].append(attachment_type)
                attachment_number += 1

    return chat_messages
