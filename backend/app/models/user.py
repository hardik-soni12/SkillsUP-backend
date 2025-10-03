from ..extensions import db, bcrypt
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(120), unique= True, nullable = False)
    password_hash = db.Column(db.String(150), nullable = False)
    bio = db.Column(db.Text, nullable = True)

    is_admin = db.Column(db.Boolean, default = False, nullable= False)

    created_at = db.Column(db.DateTime(timezone=True), server_default = db.func.now() , nullable = False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default= db.func.now(), onupdate = db.func.now(), nullable = False)

    # relationships
    skills = db.relationship('Skill', back_populates="user", cascade="all, delete-orphan")
    matches_as_user1 = db.relationship('Match', foreign_keys="Match.user1_id", back_populates="user1")
    matches_as_user2 = db.relationship('Match', foreign_keys="Match.user2_id", back_populates="user2")
    messages = db.relationship("Message", back_populates="sender", cascade="all, delete-orphan")

    def __init__(self, username, email, password, bio=None, is_admin=False):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.bio = bio
        self.is_admin = is_admin

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.id} - {self.email}>"