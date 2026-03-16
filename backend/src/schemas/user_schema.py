from flask_jwt_extended import current_user
from flask_smorest.fields import Upload
from marshmallow import Schema, ValidationError, fields, validate, validates

from ..database import db
from ..database.models import User
from ..utils import get_image


class UserPublicSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    bio = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format="%d-%m-%Y")
    image_url = fields.Method("get_image_path", dump_only=True)

    def get_image_path(self, obj) -> str:
        return get_image(obj.image_path)


class UserProfileSchema(UserPublicSchema):
    email = fields.Email(dump_only=True)


class BaseUserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20, error="Please use at least 3 characters"),
            validate.Regexp(
                r"^[a-zA-Z0-9_-]+$",
                error="username can only contain letters, numbers, '-', and '_'",
            ),
        ],
    )
    first_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=40),
            validate.Regexp(
                r"^[a-zA-Z'\s]+$", error="First name can only contain letters"
            ),
        ],
    )
    last_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=40),
            validate.Regexp(
                r"^[a-zA-Z'\s]+$", error="Last name can only contain letters"
            ),
        ],
    )
    email = fields.Email(required=True, validate=[validate.Length(max=255)])

    @validates("username")
    def validate_username(self, value, **kwargs):
        user_username = current_user.username if current_user else None
        user = db.session.scalar(db.select(User).where(User.username == value))
        if value != user_username and user:
            raise ValidationError("That username is already taken")

    @validates("email")
    def validate_email(self, value, **kwargs):
        user_email = current_user.email if current_user else None
        user = db.session.scalar(db.select(User).where(User.email == value))
        if value != user_email and user:
            raise ValidationError("That email is already taken")


class RegisterSchema(BaseUserSchema):
    password = fields.Str(
        required=True, load_only=True, validate=[validate.Length(min=8)]
    )


class UpdateSchema(BaseUserSchema):
    bio = fields.Str(validate=[validate.Length(max=350)])


class UpdateImageSchema(Schema):
    image = Upload(required=True)


class UserSearchSchema(Schema):
    username = fields.Str(required=False)
