from ..extensions import db
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint

class Match(db.Model):
    __tablename__ = 'matches'
    __table_args__=(CheckConstraint('user1_id != user2_id', name='check_different_users'),)

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='match_status'), default='pending', nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

    # relationships
    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='matches_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], back_populates='matches_as_user2')
    messages = db.relationship('Message', back_populates='match', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Match {self.id} - User{self.user1_id} <-> User{self.user2_id} ({self.status})>"