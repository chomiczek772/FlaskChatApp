from app import db
from model.message import Message
from mapper.message import toDto as toMessageDto
import service.chatService as chatService
from flask_login import current_user


def mapToDto(message):
    chat = chatService.getChatByIdForUser(message.chat_id, current_user)
    userInChatId = chat.user1_id if chat.user1_id != current_user.id else chat.user2_id
    return toMessageDto(message, chat, userInChatId)


def createMessage(chat, sender, content):
    message = Message(content, chat.user1_id == sender.id, chat.id)
    db.session.add(message)
    db.session.commit()
    return message


def getMessageById(id):
    message = Message.query.filter_by(id=id).first()
    if message is None:
        raise Exception(("Message id={} not found", id))
    return message


def getMessageByIdWithinChat(messageId, chatId):
    message = getMessageById(messageId)
    if message.chat_id != chatId:
        raise Exception("Message with id={} is not in chat with id={}", messageId, chatId)
    return mapToDto(message)


def getLastNMessagesFromChat(chatId, n):
    messages = Message.query.filter_by(chat_id=chatId) \
        .order_by(Message.date.desc()) \
        .limit(n) \
        .all()
    return list(map(mapToDto, messages))


def getLastNMessagesFromChatAfterId(chatId, lastMessageId, n):
    messages = Message.query.filter(
        (Message.chat_id == chatId) & (Message.id < lastMessageId)
    ) \
        .order_by(Message.date.desc()) \
        .limit(n) \
        .all()
    return list(map(mapToDto, messages))
