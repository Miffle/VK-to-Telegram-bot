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
        print((group_id[0]["name"] + " | " + zz["items"][i]["last_message"]["text"]), file=f, flush=True)
    else:
        print((group_id[0]["name"] + " | " + zz["items"][i]["last_message"]["attachments"][0]["type"]), file=f,
              flush=True)


def user_message(session, zz, i):
    """Читает последнее сообщение юзера из диалогов"""
    f = open("mes.txt", "a+")
    """Получает id пользователя который написал сообщение"""

    c = session.method("users.get", {"user_ids": zz["items"][i]["conversation"]["peer"]["id"]})

    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    if zz["items"][i]["last_message"]["text"] != "":
        print((c[0]["first_name"] + ' ' + c[0]["last_name"] + " | " + zz["items"][i]["last_message"]["text"]), file=f,
              flush=True)
    else:
        print((c[0]["first_name"] + ' ' + c[0]["last_name"] + " | " +
               zz["items"][i]["last_message"]["attachments"][0]["type"]), file=f, flush=True)


def chat_message(zz, i):
    """Читает последнее сообщение в чате из диалогов"""
    f = open("mes.txt", "a+")
    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    if zz["items"][i]["last_message"]["text"] != "":
        print((
                zz["items"][i]["conversation"]["chat_settings"]["title"] + " | " + zz["items"][i]["last_message"][
                    "text"]), file=f, flush=True)
    else:
        print((zz["items"][i]["conversation"]["chat_settings"]["title"] + " | " +
               zz["items"][i]["last_message"]["attachments"][0]["type"]), file=f, flush=True)
