from app import db
from uuid import uuid4
import service.fileService as fileService


def uploadUserImage(user, file):
    if file is None:
        removeUsersImage(user)
    else:
        checkIfImageIsValidElseThrow(user, file)
        if user.image_url is not None:
            removeUsersImage(user)
        saveUsersImage(user, file)

    db.session.commit()


def saveUsersImage(user, file):
    blob = file.read()

    metadata = {
        "Content-Type": file.content_type,
        "Content-Length": str(len(blob))
    }

    extension = file.filename[file.filename.rindex('.'):]
    fileName = str(uuid4()) + extension
    pathFileName = "images/" + fileName

    try:
        fileService.save(pathFileName, metadata, blob)
        user.image_url = fileName
    except:
        print("User id={} tried to upload image, file.getInputStream() exception", user.id)


def checkIfImageIsValidElseThrow(user, file):
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise Exception("User id={} tried to upload {} file.", user.id, file.getContentType())


def removeUsersImage(user):
    fileService.remove(user.image_url)
    user.image_url = None


def getProfileInfo(current_user):
    return {
        'username': current_user.username,
        'email': current_user.email,
        'imageUrl': current_user.image_url,
    }
