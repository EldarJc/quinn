from flask_smorest.fields import Upload
from marshmallow import Schema, fields, validate

from ..constants import EventType
from ..utils import get_image
from .tag_schema import RelationshipTagSchema, TagSchema


class EventLocationSchema(Schema):
    id = fields.Int(dump_only=True)
    country = fields.Str(dump_only=True)
    state = fields.Str(dump_only=True)
    city = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)


class EventImageSchema(Schema):
    image = Upload(required=True)


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    image_path = fields.Method("get_image_path", dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    start_date = fields.DateTime(dump_only=True, format="%d-%m-%Y %H:%M")
    end_date = fields.DateTime(dump_only=True, format="%d-%m-%Y %H:%M")
    event_type = fields.Enum(enum=EventType, dump_only=True)
    location = fields.Nested(EventLocationSchema, dump_only=True)
    max_attendees = fields.Int(dump_only=True)
    owner_id = fields.Int(dump_only=True)
    tags = fields.List(fields.Nested(TagSchema), dump_only=True)

    def get_image_path(self, obj) -> str:
        return get_image(obj.image_path)


class AddEventLocationSchema(Schema):
    country = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str()
    address = fields.Str(required=True)


class CreateEventSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    event_type = fields.Enum(enum=EventType, required=True)
    max_attendees = fields.Int(allow_none=True)
    location = fields.Nested(AddEventLocationSchema)
    tags = fields.List(
        fields.Pluck(RelationshipTagSchema, "id"),
        required=True,
        validate=validate.Length(min=2, max=5, error="Select between 2 and 5 tags."),
    )
