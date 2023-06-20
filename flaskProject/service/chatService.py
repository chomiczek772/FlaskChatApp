from flask_login import current_user

from model.chat import Chat
from app import db
import service.messageService as messageService
from mapper.chat import toDto as chatToDto

import service.userService as userService
import service.webSocketService as wsService


def getChatById(id):
    chat = Chat.query.filter_by(id=id).first()
    if chat is None:
        raise Exception(("Chat id={} not found", id))
    return chat


def getChatByIdForUser(id, user):
    chat = getChatById(id)
    if chat.user1_id != user.id and chat.user2_id != user.id:
        raise Exception(("Forbidden access to chat. ChatService.getChatByIdForUser({}, {})", id, user.id))
    return chat


def mapChatToDto(chat):
    otherUserId = chat.user2_id if chat.user1_id == current_user.id else chat.user1_id
    userToBeInChat = userService.getUserById(otherUserId)
    lastMessage = messageService.getMessageById(chat.last_message_id) if chat.last_message_id else None
    return chatToDto(chat, userToBeInChat, lastMessage)


def getUsersNChatPreviews(user, lastChatId, lastChatDateString, pageSize):
    if lastChatId == -1:
        chatPage = Chat.query.filter((Chat.user1_id == user.id) | (Chat.user2_id == user.id)) \
            .order_by(Chat.last_date.desc()) \
            .limit(pageSize) \
            .all()
    else:
        chatPage = Chat.query.filter(
            ((Chat.user1_id == user.id) | (Chat.user2_id == user.id)) &
            (Chat.id != lastChatId) &
            (Chat.last_date <= lastChatDateString)
        ) \
            .order_by(Chat.last_date.desc()) \
            .limit(pageSize) \
            .all()

    return list(map(mapChatToDto, chatPage))


def createChat(thisUser, otherUserId):
    thisUserId = thisUser.id
    if thisUserId == otherUserId:
        raise Exception("Invalid arguments in ChatService.createChat({}, {}), u1==u2", thisUserId, otherUserId)

    chatAlreadyExists = Chat.query.filter(
        ((Chat.user1_id == thisUserId) & (Chat.user2_id == otherUserId)) |
        ((Chat.user2_id == thisUserId) & (Chat.user1_id == otherUserId))
    ).first() is not None

    if chatAlreadyExists:
        raise Exception("Invalid arguments in ChatService.createChat({}, {}), alreadyExists", thisUser.id,
                        otherUserId)

    chat = Chat(thisUserId, otherUserId)
    db.session.add(chat)
    db.session.commit()

    # // WebSocket
    wsService.sendChatWS(chat, chat.user1_id)
    wsService.sendChatWS(chat, chat.user2_id)

    return chat


def getNMessagesFromChat(user, chatId, lastMessageId, pageSize):
    chat = getChatByIdForUser(chatId, user)

    # we have to return most recent ones
    if lastMessageId < 0:
        lastNMessages = messageService.getLastNMessagesFromChat(chat.id, pageSize)

    else:
        lastNMessages = messageService.getLastNMessagesFromChatAfterId(chat.id, lastMessageId, pageSize)

    lastNMessages.reverse()

    if len(lastNMessages) != 0:
        updateLastReadAndInformThroughWS(chat, user, int(lastNMessages[-1]['id']))

    return lastNMessages


def sendTextMessage(sender, chatId, content):
    if not isMessageContentValid(content):
        return

    chat = getChatByIdForUser(chatId, sender)
    message = messageService.createMessage(chat, sender, content)

    if chat.first_message_id is None:
        chat.first_message_id = message.id
        db.session.add(chat)
        db.session.commit()

    notifyAboutMessage(chat, sender, message)


def notifyAboutMessage(chat, sender, message):
    updateLastReadAndInformThroughWS(chat, sender, message.id)
    chat.last_message_id = message.id
    chat.last_date = message.date
    db.session.add(chat)
    db.session.commit()


def updateLastReadAndInformThroughWS(chat, user, messageId):
    updated = updateLastReadInChatForUser(chat, user, messageId)
    message = messageService.getMessageById(messageId)

    if not updated:
        return

    db.session.add(chat)
    db.session.commit()

    # WebSocket
    wsService.sendMessageWS(message, chat.user1_id)
    wsService.sendMessageWS(message, chat.user2_id)


def updateLastReadInChatForUser(chat, user, messageId):
    if chat.user1_id == user.id:
        if chat.last_message_read_by_user1_id is None or chat.last_message_read_by_user1_id < messageId:
            chat.last_message_read_by_user1_id = messageId
            return True

    elif chat.last_message_read_by_user2_id is None or chat.last_message_read_by_user2_id < messageId:
        chat.last_message_read_by_user2_id = messageId
        return True

    return False


def isMessageContentValid(content):
    return 0 < len(content) < 10000


def messageRead(user, chatId, messageId):
    chat = getChatByIdForUser(chatId, user)
    message = messageService.getMessageByIdWithinChat(messageId, chatId)
    updateLastReadAndInformThroughWS(chat, user, messageId)
