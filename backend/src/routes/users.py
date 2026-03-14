from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint, abort

from ..database import db
from ..database.models import User
from ..schemas.user_schema import (
    UpdateImageSchema,
    UpdateSchema,
    UserProfileSchema,
    UserPublicSchema,
)
from ..utils import delete_image, save_image

bp = Blueprint("User", __name__)

user_profile_schema = UserProfileSchema
user_schema = UserPublicSchema()
users_schema = UserPublicSchema(many=True)
update_user_schema = UpdateSchema(partial=True)
update_image_schema = UpdateImageSchema()


@bp.route("/<string:username>")
class UserPublic(MethodView):
    @bp.response(200, user_schema)
    def get(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username))

        return user or abort(404, message="User not found.")


@bp.route("/me")
class UserProfile(MethodView):
    @jwt_required()
    @bp.response(200, user_profile_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def get(self):
        return current_user

    @jwt_required()
    @bp.arguments(update_user_schema)
    @bp.response(200, user_profile_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, user_data):
        return current_user.update(**user_data)


@bp.route("/me/image")
class UserImage(MethodView):
    @jwt_required()
    @bp.arguments(update_image_schema, location="files")
    @bp.response(200, user_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, image_data):
        if current_user.image_id:
            delete_image(current_user.image_id)

        image = image_data["image"]
        response = save_image(image, "profile_images")

        user = current_user.update(**response)
        return user

    @jwt_required()
    @bp.response(200, user_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self):
        image_id = current_user.image_id

        if not image_id:
            abort(400, message="No profile image to delete.")

        delete_image(image_id)

        user = current_user.update(image_id=None, image_path=None)
        return user
