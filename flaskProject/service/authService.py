import jwt
from datetime import datetime as dt

from app import db, app
from model.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def handleRegisterRequest(email, username, password):
    if User.query.filter_by(email=email).first() is not None:
        raise Exception("This email is already registered.")
    if User.query.filter_by(username=username).first() is not None:
        raise Exception("This username is already registered.")

    new_user = User(
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256'),
        last_active=dt.now()
    )
    db.session.add(new_user)
    db.session.commit()


def handleLogin(email, username, password):
    user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()

    if not user or not check_password_hash(user.password, password):
        raise Exception('BAD LOGIN')

    token = jwt.encode({'userId': user.id}, app.config['SECRET_KEY'], 'HS256')
    return token
