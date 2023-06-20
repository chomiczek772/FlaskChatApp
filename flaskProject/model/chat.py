from app import db
from datetime import datetime as dt


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer)
    user2_id = db.Column(db.Integer)
    first_message_id = db.Column(db.Integer)
    last_message_id = db.Column(db.Integer)
    last_date = db.Column(db.DATETIME)
    last_message_read_by_user1_id = db.Column(db.Integer)
    last_message_read_by_user2_id = db.Column(db.Integer)
    closed = db.Column(db.Boolean)

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.last_date = dt.now()
        self.closed = False

    def toJson(self):
        return {
            'id': self.id,
            'user1Id': self.user1_id,
            'user2Id': self.user2_id,
            'firstMessageId': self.first_message_id,
            'lastMessageId': self.last_message_id,
            'lastDate': self.last_date,
            'lastMessageRead_byUser1Id': self.last_message_read_by_user1_id,
            'lastMessageRead_byUser2Id': self.last_message_read_by_user2_id,
            'closed': self.closed,
        }
