def get_attachments(vk_message, attachments_count, current_fwd_message=None):
    """
    Function for getting all attachments from a current message or list of messages
    :param vk_message: current message with attachments
    :param attachments_count: Number of attachments in messages
    :param current_fwd_message: The number of the forwarded message(Optional) default value is None
    :return: all attachments in current_message: 1 - url, 2 - type of attachments, 3 - transcript of audio message or
     title of video/audio/post/document or 0
    """
    attachments = ([], [], [])
    for attachment in range(0, attachments_count):
        if current_fwd_message is not None:
            attachment_type = vk_message[current_fwd_message]['attachments'][attachment]["type"]
            current_attachment = vk_message[current_fwd_message]['attachments'][attachment]
        else:
            attachment_type = vk_message['attachments'][attachment]["type"]
            current_attachment = vk_message['attachments'][attachment]
        attachments[1].append(attachment_type)
        if attachment_type == "audio":
            attachments[0].append(current_attachment['audio']['url'])
            attachments[2].append(
                current_attachment["audio"]["artist"] + " - " + current_attachment["audio"][
                    "title"])
        elif attachment_type == "photo":
            sizes = current_attachment["photo"]["sizes"]
            max_size = max(sizes, key=lambda size: size["height"])
            attachments[0].append(max_size['url'])
            attachments[2].append(0)
        elif attachment_type == "video":
            attachments[0].append(current_attachment['video']['player'])
            attachments[2].append(current_attachment['video']['title'])
        elif attachment_type == "audio_message":
            attachments[0].append(current_attachment['audio_message']['link_ogg'])
            if 'transcript' in current_attachment['audio_message']:
                attachments[2].append(current_attachment['audio_message']['transcript'])
            else:
                attachments[2].append(0)
        elif attachment_type == "doc":
            doc_link = current_attachment['doc']['url']
            attachments[0].append(doc_link)
            attachments[2].append(current_attachment['doc']['title'])
        elif attachment_type == "sticker":
            attachments[0].append(current_attachment['sticker']['images'][2]['url'])
            attachments[2].append(0)
        elif attachment_type == "gift":
            attachments[0].append(current_attachment['gift']['thumb_256'])
            attachments[2].append(0)
        elif attachment_type == "link":
            attachments[0].append(current_attachment['link']['url'])
            attachments[2].append(0)
        elif attachment_type == "wall":
            link_to_post = (
                f"vk.com/wall{current_attachment['wall']['from_id']}_{current_attachment['wall']['id']}")
            attachments[0].append(link_to_post)
            attachments[2].append(0)
        else:
            attachments[0].append(attachment_type)
            attachments[2].append(0)

    return attachments
