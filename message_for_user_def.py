class ConversationMessages(object):
    """
    Сообщения диалога
    """
    name = ""
    link = ""
    messages = []


class Message(object):
    """
    Сообщение
    """
    sender = ""
    text = ""
    attachments = []

    def add_attachments(self, conversation_message):
        """
        Добавить вложения из json сообщения диалога
        """
        conversation_message_attachments = conversation_message["attachments"]
        self.attachments = []

        for current_attachment in conversation_message_attachments:
            attachment_to_add = Attachment()
            attachment_to_add.attachment_type = current_attachment["type"]
            if attachment_to_add.attachment_type == "video":
                attachment_to_add.attachment_link = current_attachment["video"]["player"]
            elif attachment_to_add.attachment_type == "photo":
                sizes = current_attachment["photo"]["sizes"]
                max_size = max(sizes, key=lambda size: size["height"])
                attachment_to_add.attachment_link = max_size["url"]
            elif attachment_to_add.attachment_type == "audio_message":
                attachment_to_add.attachment_link = current_attachment["audio_message"]["link_ogg"]
            elif attachment_to_add.attachment_type == "audio":
                attachment_to_add.attachment_link = current_attachment["audio"]["url"]
            elif attachment_to_add.attachment_type == "doc":
                attachment_to_add.attachment_link = current_attachment["doc"]["url"]
            elif attachment_to_add.attachment_type == "sticker":
                attachment_to_add.attachment_link = current_attachment["sticker"]["images_with_background"][2]["url"]
            else:
                attachment_to_add.attachment_link = attachment_to_add.attachment_type
            self.attachments.append(attachment_to_add)


class Attachment(object):
    """
    Вложение
    """
    attachment_type = ""
    attachment_link = ""


def group_message(session, current_conversation):
    """Читает последнее сообщение группы из диалогов"""

    """ Получает ID группы, которая написала сообщение"""
    group_local_id = current_conversation["peer"]["local_id"]
    group_id = current_conversation["peer"]["id"]
    group_name = session.method("groups.getById", {"group_id": group_local_id})

    """ 
    Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения
    """
    group_conv_messages = ConversationMessages()
    group_conv_messages.messages = []
    group_conv_messages.name = group_name[0]["name"]
    group_conv_messages.link = "vk.com/club" + str(group_local_id)

    group_last_mes = current_conversation["last_conversation_message_id"]
    group_unread_count = current_conversation["unread_count"]
    start = (group_last_mes - group_unread_count) + 1
    for current_message_id in range(start, group_last_mes + 1):
        conversation_message_response = (session.method("messages.getByConversationMessageId",
                                                        {"peer_id": group_id,
                                                         "conversation_message_ids": current_message_id}))
        conversation_message = conversation_message_response["items"][0]
        current_message = Message()
        current_message.sender = group_conv_messages.name

        if conversation_message["text"] != "":
            current_message.text = conversation_message["text"]
        else:
            current_message.add_attachments(conversation_message)
        group_conv_messages.messages.append(current_message)
    return group_conv_messages


def user_message(session, current_conversation):
    """Читает последнее сообщение юзера из диалогов"""
    """Получает id пользователя который написал сообщение"""
    user = session.method("users.get", {"user_ids": current_conversation["peer"]["id"]})[0]

    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    user_id = current_conversation["peer"]["id"]

    user_conv_messages = ConversationMessages()
    user_conv_messages.messages = []
    user_conv_messages.name = user["first_name"] + " " + user["last_name"]
    user_conv_messages.link = "vk.com/id" + str(user_id)

    user_last_mes = current_conversation["last_conversation_message_id"]
    user_unread_count = current_conversation["unread_count"]
    start = (user_last_mes - user_unread_count) + 1
    for current_message_id in range(start, user_last_mes + 1):
        conversation_message_response = (session.method("messages.getByConversationMessageId",
                                                        {"peer_id": user_id,
                                                         "conversation_message_ids": current_message_id}))
        conversation_message = conversation_message_response["items"][0]
        current_message = Message()
        current_message.sender = user_conv_messages.name

        if conversation_message["text"] != "":
            current_message.text = conversation_message["text"]
        else:
            current_message.add_attachments(conversation_message)
        user_conv_messages.messages.append(current_message)

    return user_conv_messages


def chat_message(current_conversation, session):
    """Читает последнее сообщение в чате из диалогов"""
    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""
    chat_conv_messages = ConversationMessages()
    chat_conv_messages.messages = []
    chat_conv_messages.name = current_conversation["chat_settings"]["title"]
    chat_conv_messages.link = current_conversation["chat_settings"]["photo"]["photo_200"]

    chat_id = current_conversation["peer"]["id"]
    chat_last_mes = current_conversation["last_conversation_message_id"]
    chat_unread_count = current_conversation["unread_count"]
    start = (chat_last_mes - chat_unread_count) + 1

    for current_message_id in range(start, chat_last_mes + 1):
        conversation_message_response = (session.method("messages.getByConversationMessageId",
                                                        {"peer_id": chat_id,
                                                         "conversation_message_ids": current_message_id}))

        conversation_message = conversation_message_response["items"][0]
        user = (session.method("users.get", {"user_ids": conversation_message["from_id"]}))[0]
        current_message = Message()
        current_message.sender = user["first_name"] + ' ' + user["last_name"] + ":"

        if conversation_message["text"] != "":
            current_message.text = conversation_message["text"]
        else:
            current_message.add_attachments(conversation_message)
        chat_conv_messages.messages.append(current_message)
    return chat_conv_messages
