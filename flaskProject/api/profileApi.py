from app import app
from flask import request
from flask_cors import cross_origin
from flask_login import current_user
from security.authentication import authenticated

import service.profileService as profileService

USERS_PAGE_SIZE = 10


@app.route('/api/profile/info', methods=['GET'])
@authenticated
@cross_origin()
def getProfileInfo():
    return profileService.getProfileInfo(current_user)


@app.route('/api/profile/image', methods=['POST'])
@authenticated
@cross_origin()
def uploadUserImage():
    file = request.files.get('file')
    profileService.uploadUserImage(current_user, file)
    return "ok"
