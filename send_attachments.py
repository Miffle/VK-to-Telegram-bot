import time


def send_attachments(bot, all_attachments, chat_id, i, message_sender_name=None, message_text=None):
    """
    This function is used to send attachments after receiving the tuple from the function get-attachments\n
    :param bot: tg bot
    :param all_attachments: Tuple of attachments from get_attachments
    :param chat_id: Telegram user id
    :param i: current attachment id (Usually this function is called in for)
    :param message_sender_name: if this attachments isn't from forward or reply message - vk message sender name
    (optional) default value is None
    :param message_text: if this attachments isn't from forward or reply message - vk message text (optional) default
    value is None
    :return:
    """
    if message_sender_name is None and message_text is None:
        if all_attachments[1][i] == 'audio_message':
            if all_attachments[2][i] != 0:
                transcript = all_attachments[2][i]
            else:
                transcript = "Слова в вк не разобрали"
            bot.send_voice(chat_id, voice=all_attachments[0][i], caption=transcript, parse_mode="HTML",
                           disable_notification=True)
        elif all_attachments[1][i] == 'photo':
            bot.send_photo(chat_id, photo=all_attachments[0][i], parse_mode="HTML",
                           disable_notification=True)
        elif all_attachments[1][i] == 'video':
            title = all_attachments[2][i]
            bot.send_message(chat_id, text=f"<a href='{all_attachments[0][i]}'>{title}</a>", parse_mode="HTML",
                             disable_notification=True)
        elif all_attachments[1][i] == 'audio':
            audio_title = all_attachments[2][i]
            bot.send_audio(chat_id, audio=all_attachments[0][i], caption=audio_title, parse_mode="HTML",
                           disable_notification=True)
        elif all_attachments[1][i] == 'doc':
            title = all_attachments[2][i]
            bot.send_message(chat_id, text=f"<a href='{all_attachments[0][i]}'>{title}</a>", parse_mode="HTML",
                             disable_notification=True)
        elif all_attachments[1][i] == 'sticker':
            bot.send_photo(chat_id, photo=all_attachments[0][i], parse_mode="HTML",
                           disable_notification=True)
        elif all_attachments[1][i] == 'gift':
            bot.send_photo(chat_id, photo=all_attachments[0][i], parse_mode="HTML",
                           disable_notification=True)
        elif all_attachments[1][i] == 'link':
            bot.send_message(chat_id, text=f"<a href={all_attachments[0][i]}>Ссылка</a>", parse_mode="HTML",
                             disable_notification=True)
        elif all_attachments[1][i] == 'wall':
            bot.send_message(chat_id, text=f"[Пост]({all_attachments[0][i]})", parse_mode="MarkdownV2",
                             disable_notification=True)
        else:
            bot.send_message(chat_id, text=all_attachments[1][i], parse_mode="HTML",
                             disable_notification=True)
    else:
        if message_sender_name is not None and message_text is not None:
            if all_attachments[1][i] == 'audio_message':
                if all_attachments[2][i] != 0:
                    transcript = all_attachments[2][i]
                else:
                    transcript = "Слова в вк не разобрали"
                bot.send_voice(chat_id, voice=all_attachments[0][i],
                               caption=f"<b>{message_sender_name}:</b> {message_text}\n <pre>{transcript}</pre>",
                               parse_mode="HTML",
                               disable_notification=True)
            elif all_attachments[1][i] == 'photo':
                bot.send_photo(chat_id, photo=all_attachments[0][i],
                               caption=f"<b>{message_sender_name}:</b> {message_text}\n",
                               parse_mode="HTML",
                               disable_notification=True)
            elif all_attachments[1][i] == 'video':
                title = all_attachments[2][i]
                bot.send_message(chat_id,
                                 text=f"<b>{message_sender_name}:</b> {message_text}\n "
                                      f"<a href='{all_attachments[0][i]}'>{title}</a>",
                                 parse_mode="HTML",
                                 disable_notification=True)
            elif all_attachments[1][i] == 'audio':
                audio_title = all_attachments[2][i]
                bot.send_audio(chat_id, audio=all_attachments[0][i],
                               caption=f"<b>{message_sender_name}:</b> {message_text}\n{audio_title}",
                               parse_mode="HTML",
                               disable_notification=True)
            elif all_attachments[1][i] == 'doc':
                title = all_attachments[2][i]
                bot.send_message(chat_id,
                                 text=(
                                     f"<b>{message_sender_name}:</b> {message_text}\n"
                                     f"<a href='{all_attachments[0][i]}'>{title}</a>"),
                                 parse_mode="HTML",
                                 disable_notification=True)
            elif all_attachments[1][i] == 'sticker':
                bot.send_photo(chat_id, photo=all_attachments[0][i], parse_mode="HTML",
                               disable_notification=True)
            elif all_attachments[1][i] == 'gift':
                bot.send_photo(chat_id, photo=all_attachments[0][i], parse_mode="HTML",
                               disable_notification=True)
            elif all_attachments[1][i] == 'link':
                bot.send_message(chat_id,
                                 text=f"<b>{message_sender_name}:</b> {message_text}\n"
                                      f"<a href={all_attachments[0][i]}>Ссылка</a>",
                                 parse_mode="HTML",
                                 disable_notification=True)
            elif all_attachments[1][i] == 'wall':
                bot.send_message(chat_id,
                                 text=f"*{message_sender_name}:* {message_text}\n"
                                      f"[Пост]({all_attachments[0][i]})",
                                 parse_mode="Markdown",
                                 disable_notification=True)
            else:
                bot.send_message(chat_id, text=f"<b>{message_sender_name}:</b> {message_text}\n{all_attachments[1][i]}",
                                 parse_mode="HTML",
                                 disable_notification=True)
    time.sleep(1)
