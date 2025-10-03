from ..extensions import db
from datetime import datetime, timezone

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relationships
    match = db.relationship('Match', back_populates='messages')
    sender = db.relationship('User', back_populates='messages')

    def __repr__(self):
        return f"<Message {self.id} from User{self.sender_id} in Match{self.match_id}>"
