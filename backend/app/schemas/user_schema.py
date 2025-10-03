from ..models.user import User
from ..models.skill import Skill
from ..models.match import Match 
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True #deserialize to model instances
        include_fk = True #Includes foreign key
        exclude = ('password_hash',) #never expose password

        # nested relationship
        skills = fields.Nested('SkillSchema', many=True, dump_only=True)
        matches_as_user1 = fields.Nested('MatchSchema', many=True, dump_only=True)
        matches_as_user2 = fields.Nested('MatchSchema', many=True, dump_only=True)

class PublicUserSchema(SQLAlchemyAutoSchema):
    ''' schema for public user profiles'''
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'created_at', 'skills')

    skills = fields.Nested('SkillSchema', many=True, dump_only=True)