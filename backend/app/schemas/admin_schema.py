from ..models.user import User
from marshmallow import fields
from ..models.skill import Skill
from ..models.match import Match 
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AdminSchema(SQLAlchemyAutoSchema):
    # only admin can see user info
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ('password_hash',)

    skills = fields.Nested('SkillSchema', many=True, dump_only=True)