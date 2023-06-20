from app import db
from flask_login import UserMixin
from dataclasses import dataclass


@dataclass
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    image_url = db.Column(db.String(65122))
    last_active = db.Column(db.DATETIME)

    def toJson(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'imageUrl': self.image_url,
            'last_active': self.last_active,
        }
