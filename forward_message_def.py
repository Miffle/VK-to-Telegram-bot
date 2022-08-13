import get_attachments
import send_attachments


def get_forward_message(current_message, session, bot, chat_id, message_sender_name):
    forward_message = current_message['fwd_messages']
    forward_messages_count = len(forward_message)
    for current_fwd_messages in range(0, forward_messages_count):
        fwd_messages = ([], [])
        forward_message_sender_id = session.method("users.get",
                                                   {"user_ids": forward_message[current_fwd_messages][
                                                       'from_id']})
        forward_message_sender_name = (forward_message_sender_id[0]["first_name"] + " " +
                                       forward_message_sender_id[0]["last_name"])
        fwd_messages_text = forward_message[current_fwd_messages]['text']
        fwd_messages[0].append(forward_message_sender_name)
        fwd_messages[1].append(fwd_messages_text)
        attachments_count = len(forward_message[current_fwd_messages]['attachments'])
        attachments_in_current_message = get_attachments.get_attachments(forward_message, attachments_count,
                                                                         current_fwd_messages)
        if attachments_count == 1:
            bot.send_message(chat_id, text=(f"<b>{message_sender_name}:</b>  {current_message['text']}\n"
                                            f"\t\t\t\t\t📩 {fwd_messages[0][0]}: {fwd_messages[1][0]}"),
                             parse_mode="HTML")
            send_attachments.send_attachments(bot, attachments_in_current_message, chat_id, 0, None, None)
            if 'reply_message' in forward_message[0]:
                get_reply_message(forward_message[0], session, bot, chat_id, message_sender_name="", message_text="")
            if 'fwd_messages' in forward_message[0]:
                get_forward_message(forward_message[0], session, bot, chat_id, message_sender_name="")
        elif attachments_count > 1:
            bot.send_message(chat_id, text=(f"<b>{message_sender_name}:</b>  {current_message['text']}\n"
                                            f"\t\t\t\t\t📩 {fwd_messages[0][0]}: {fwd_messages[1][0]}"),
                             parse_mode="HTML")
            for i in range(0, attachments_count):
                send_attachments.send_attachments(bot, attachments_in_current_message, chat_id, i, None, None)
            if 'reply_message' in forward_message[0]:
                get_reply_message(forward_message[0], session, bot, chat_id, message_sender_name="", message_text="")
            if 'fwd_messages' in forward_message[0]:
                get_forward_message(forward_message[0], session, bot, chat_id, message_sender_name="")
        else:
            bot.send_message(chat_id, text=(f"<b>{message_sender_name}:</b>  {current_message['text']}\n"
                                            f"\t\t\t\t\t📩 {fwd_messages[0][0]}: {fwd_messages[1][0]}"),
                             parse_mode="HTML")
            if 'reply_message' in forward_message[0]:
                get_reply_message(forward_message[0], session, bot, chat_id, message_sender_name="", message_text="")
            if 'fwd_messages' in forward_message[0]:
                get_forward_message(forward_message[0], session, bot, chat_id, message_sender_name="")


def get_reply_message(current_message, session, bot, chat_id, message_sender_name, message_text):
    if 'reply_message' in current_message:
        replied_message_sender_id = session.method("users.get",
                                                   {"user_ids": current_message['reply_message']['from_id']})
        replied_message_sender_name = (
                replied_message_sender_id[0]["first_name"] + " " + replied_message_sender_id[0]["last_name"])
        replied_message_text = current_message['reply_message']['text']
        attachments_count = len(current_message['reply_message']['attachments'])
        bot.send_message(chat_id, text=(f"<b>{message_sender_name}:</b>  {message_text}\n"
                                        f"\t↩️️{replied_message_sender_name}: {replied_message_text}"),
                         parse_mode="HTML")
        all_attachments = get_attachments.get_attachments(current_message['reply_message'], attachments_count, None)
        count_of_attachments = len(all_attachments[0])
        for current_attachment_in_message in range(0, count_of_attachments):
            send_attachments.send_attachments(bot, all_attachments, chat_id, current_attachment_in_message, None, None)
