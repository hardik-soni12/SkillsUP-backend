from ..extensions import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable =False, index= True)
    skill_type = db.Column(db.Enum('knows', 'wants', name='skill_type'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='skills')

    def __repr__(self):
        return f"<Skill {self.id} - {self.name} ({self.skill_type})>"