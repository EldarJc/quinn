from marshmallow import Schema, ValidationError, fields, validate, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..database import db
from ..database.models import Tag


class RelationshipTagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session


class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class CreateTagSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))

    @validates("name")
    def validate_name(self, value, **kwargs):
        if db.session.scalar(db.select(Tag).where(Tag.name == value)):
            raise ValidationError(f"Tag {value} already exists")
