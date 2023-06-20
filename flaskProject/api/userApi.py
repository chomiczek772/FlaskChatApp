from app import app
from flask import request
from flask_cors import cross_origin
from flask_login import current_user
import service.userService as userService
from security.authentication import authenticated
from util.json import toJson

USERS_PAGE_SIZE = 10


@app.route('/api/users-by-phrase', methods=['GET'])
@authenticated
@cross_origin()
def getNUsersByPhrase():
    phrase = request.args.get('phrase')
    pageNr = int(request.args.get('pageNr'))

    return toJson(userService.getNUsersByPhrase(phrase, pageNr, USERS_PAGE_SIZE))


@app.route('/api/get-username', methods=['GET'])
@authenticated
@cross_origin()
def getUsernameFromJWT():
    return current_user.username


@app.route('/api/users-active-status', methods=['GET'])
@authenticated
@cross_origin()
def getUsersActiveStatuses():
    usersIds = request.args.getlist('usersIds')
    return userService.getUsersActiveStatuses(usersIds)
