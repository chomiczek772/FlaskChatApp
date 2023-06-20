from app import db
from model.user import User
from datetime import datetime as dt


def getUserById(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        raise Exception(("User id={} not found", id))
    return user


def getUserByUsername(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise Exception(("User username={} not found", username))
    return user


def getNUsersByPhrase(phrase, pageNr, pageSize):
    if pageNr < 0:
       raise Exception("pageNr < 0")
    return User.query.filter(
        User.username.ilike("%{}%".format(phrase))
    )\
        .limit(pageSize) \
        .all()


def setUsersActiveStatus(userId, active):
    user = getUserById(userId)

    if active:
        user.last_active = None
    else:
        user.last_active = dt.now()

    db.session.add(user)
    db.session.commit()


def getUsersActiveStatuses(usersIds):
    users = User.query.filter(
        User.id.in_(usersIds)
    ).all()

    return {user.id: user.last_active for user in users}
