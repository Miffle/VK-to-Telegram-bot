import time


def send_attachments(bot, all_attachments, chat_id, i):
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
        bot.send_message(chat_id, text=f"<a href={all_attachments[0][i]}>Пост</a>", parse_mode="HTML",
                         disable_notification=True)
    else:
        bot.send_message(chat_id, text=all_attachments[1][i], parse_mode="HTML",
                         disable_notification=True)
    time.sleep(2)
