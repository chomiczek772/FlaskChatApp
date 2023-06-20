from app import db
from datetime import datetime as dt


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATETIME)
    content = db.Column(db.String(10000))
    by_user1 = db.Column(db.Boolean)
    chat_id = db.Column(db.Integer)

    def __init__(self, content, byUser1, chatId):
        self.content = content
        self.date = dt.now()
        self.by_user1 = byUser1
        self.chat_id = chatId

    def toJson(self):
        return {
            'id': self.id,
            'date': self.date,
            'content': self.content,
            'byUser1': self.by_user1,
            'chatId': self.chat_id,
        }
