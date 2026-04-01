from marshmallow import fields

from src.app import ma


class RoleSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    class Meta:
        fields = ("id", "name")
