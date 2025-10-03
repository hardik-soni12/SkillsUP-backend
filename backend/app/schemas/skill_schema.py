from ..models.skill import Skill
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class SkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        load_instance = True
        include_fk = True

    user = fields.Nested('UserSchema', only=('id', 'username'), dump_only=True)