from marshmallow import fields, Schema, validate, validates_schema, ValidationError

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=20))
    confirm_password = fields.Str(required=True, load_only=True)
    bio = fields.Str(required=False)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        # check if password == confirm_password
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('passwords must match', field_name='confirm_password')
    

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=20))