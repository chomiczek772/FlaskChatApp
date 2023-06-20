from app import app

import service.chatService as chatService

from mapper.chat import toDto as toChatDto
from mapper.message import toDto as toMessageDto
import service.userService as userService


def sendMessageWS(message, receiverId):
    chat = chatService.getChatById(message.chat_id)
    response = createMessage(chat, message, receiverId)
    app.socketio.emit('message', {'data': response}, to=receiverId)


def sendChatWS(chat, receiverId):
    response = createMessage(chat, None, receiverId)
    app.socketio.emit('message', {'data': response}, to=receiverId)


def createMessage(chat, message, receiverId):
    userInChatId = chat.user1_id if receiverId == chat.user2_id else chat.user2_id
    user = userService.getUserById(userInChatId)

    response = {
        'chat': toChatDto(chat, user, message)
    }

    if message is not None:
        response['message'] = toMessageDto(message, chat, userInChatId)

    return response
