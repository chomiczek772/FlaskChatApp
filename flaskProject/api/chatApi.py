from app import app
from flask import request, make_response
from flask_cors import cross_origin
from flask_login import current_user
import service.chatService as chatService
from security.authentication import authenticated
from util.json import toJson

CHATS_PAGE_SIZE = 10
MESSAGES_PAGE_SIZE = 15


@app.route('/api/chats', methods=['GET', 'POST'])
@authenticated
@cross_origin()
def handleChats():
    if request.method == 'GET':
        return getUsersNChatPreviews()
    elif request.method == 'POST':
        return createChat()


def getUsersNChatPreviews():
    lastChatId = request.args.get('lastId') or -1
    lastChatDate = request.args.get('lastDate') or -1
    return toJson(chatService.getUsersNChatPreviews(current_user, lastChatId, lastChatDate, CHATS_PAGE_SIZE))


def createChat():
    userId = request.args.get('id')
    try:
        createdChat = chatService.createChat(current_user, userId)
        return {'chatId': createdChat.id}
    except Exception as e:
        return make_response({'message': e.args[0]}, 400)


@app.route("/api/chats/<id>/messages", methods=['GET', 'POST'])
@authenticated
@cross_origin()
def handleMessages(id):
    if request.method == 'GET':
        return getNMessagesFromChat(id)
    elif request.method == 'POST':
        return sendMessage(id)


def getNMessagesFromChat(id):
    lastMessageId = int(request.args.get('lastMessageId')) if request.args.get('lastMessageId') else -1
    messages = chatService.getNMessagesFromChat(current_user, id, lastMessageId, MESSAGES_PAGE_SIZE)
    return toJson(messages)


def sendMessage(id):
    content = request.args.get('content')
    chatService.sendTextMessage(current_user, id, content)
    return {}


@app.route("/api/chats/<id>/message-read", methods=['POST'])
@authenticated
@cross_origin()
def messageRead(id):
    messageId = int(request.args.get('messageId'))
    chatService.messageRead(current_user, int(id), messageId)
    return {}
