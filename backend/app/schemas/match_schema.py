from ..models.match import Match
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class MatchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Match
        load_instance = True
        include_fk = True

    # relationships
    user1 = fields.Nested('PublicUserSchema', only=('id', 'username'), dump_only=True)
    user2 = fields.Nested('PublicUserSchema', only=('id', 'username'), dump_only=True)
    messages = fields.Nested('MessageSchema', many=True, dump_only=True)