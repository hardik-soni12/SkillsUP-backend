from ..models.message import Message
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        include_fk = True

    sender = fields.Nested('UserSchema', only=('id', 'username', 'email'), dump_only=True)
    match = fields.Nested('MatchSchema', only=('id', 'status'), dump_only=True)