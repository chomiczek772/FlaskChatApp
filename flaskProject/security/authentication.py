from functools import wraps

import jwt
from flask import request, make_response, jsonify
from flask_login import login_user

from app import app
from model.user import User


TOKEN_PREFIX = 'Bearer '


def authenticated(endpointFunc):
    @wraps(endpointFunc)
    def decorator(*args, **kwargs):
        token = None
        if request.method != 'OPTIONS':
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'][len(TOKEN_PREFIX):]
            if not token:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                user = User.query.filter_by(id=data['userId']).first()
                login_user(user)
            except:
                return make_response(jsonify({"message": "Invalid token!"}), 401)
        return endpointFunc(*args, **kwargs)
    return decorator
