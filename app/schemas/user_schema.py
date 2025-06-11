from app import ma
from app.models.user import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ['password_hash']
    
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    role = fields.Str(dump_only=True)
    avatar_url = fields.URL(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class RegisterSchema(ma.Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

