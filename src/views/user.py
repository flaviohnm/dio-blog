from marshmallow import fields

from src.app import ma
from src.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class UserIParameter(ma.Schema):
    user_id = fields.Int(required=True)


class CreateUserSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role_id = fields.Int(required=True, strict=True)
