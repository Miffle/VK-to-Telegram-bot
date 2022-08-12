def get_attachments(vk_message, attachments_count, current_fwd_message):
    attachments = ([], [], [])
    for attachment in range(0, attachments_count):
        attachment_type = vk_message[current_fwd_message]['attachments'][attachment]["type"]
        current_attachment = vk_message[current_fwd_message]['attachments'][attachment]
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
            link_to_post = "vk.com/wall" + current_attachment['wall']['from_id'] + "_" + current_attachment['wall'][
                'id']
            attachments[0].append(link_to_post)
            attachments[2].append(0)
        else:
            attachments[0].append(attachment_type)
            attachments[2].append(0)

    return attachments
