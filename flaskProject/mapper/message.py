def toDto(message, chat, userInChatId):
    sent = (message.by_user1 and chat.user2_id == userInChatId) or \
        (not message.by_user1 and chat.user1_id == userInChatId)

    return {
        'id': message.id,
        'content': message.content,
        'date': str(message.date),
        'sent': sent
    }
