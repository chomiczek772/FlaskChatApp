import mapper.message as messageMapper


def toDto(chat, userToBeInChat, lastMessage):
    if userToBeInChat.id != chat.user1_id:
        lastReadMessageIdByThis = chat.last_message_read_by_user1_id
        lastReadMessageIdByOther = chat.last_message_read_by_user2_id
    else:
        lastReadMessageIdByThis = chat.last_message_read_by_user2_id
        lastReadMessageIdByOther = chat.last_message_read_by_user1_id

    return {
        'id': chat.id,
        'usersId': userToBeInChat.id,
        'usersName': userToBeInChat.username,
        'usersImageUrl': userToBeInChat.image_url,
        'firstMessageId': chat.first_message_id,
        'message': messageMapper.toDto(lastMessage, chat, userToBeInChat.id) if lastMessage is not None else {},
        'lastReadMessageIdByThis': lastReadMessageIdByThis,
        'lastReadMessageIdByOther': lastReadMessageIdByOther,
        'lastInteractionDate': str(chat.last_date),
        'lastActiveDate': str(userToBeInChat.last_active) if userToBeInChat.last_active is not None else None
    }
