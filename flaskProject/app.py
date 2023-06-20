from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "asdadasJSSKRYPT"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:admin@localhost/flask-chat'
    app.config['CORS_HEADERS'] = 'Content-Type'

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from model.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

app = create_app()

import api.authApi
import api.chatApi
import api.userApi
import api.wsApi
import api.profileApi

socketio = app.socketio


if __name__ == '__main__':
    app.run()
