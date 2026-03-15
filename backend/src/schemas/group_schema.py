from flask_smorest.fields import Upload
from marshmallow import Schema, ValidationError, fields, validate, validates

from ..database import db
from ..database.models import Group
from ..utils import get_image
from .tag_schema import RelationshipTagSchema, TagSchema


class CreateGroupSchema(Schema):
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=100),
            validate.Regexp(
                r"^[a-zA-Z0-9'\s]+$",
                error="Group name can only contain letters and numbers",
            ),
        ],
    )
    description = fields.Str(validate=[validate.Length(max=500)])
    tags = fields.List(
        fields.Pluck(RelationshipTagSchema, "id"),
        required=True,
        validate=validate.Length(min=2, max=5, error="Select between 2 and 5 tags."),
    )

    @validates("name")
    def validate_name(self, value, **kwargs):
        if db.session.scalar(db.select(Group).where(Group.name == value)):
            raise ValidationError("That name is already taken")


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    tags = fields.List(fields.Nested(TagSchema), dump_only=True)
    image_url = fields.Method("get_image_path", dump_only=True)

    def get_image_path(self, obj) -> str:
        return get_image(obj.image_path)


#


class UpdateGroupSchema(CreateGroupSchema):
    pass


class GroupImageSchema(Schema):
    image = Upload(required=True)


class GroupMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
