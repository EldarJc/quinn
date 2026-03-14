from flask import current_app as app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .database.models import RevokedTokenModel, User
from .extensions import imagekit, jwt


def get_image(image_path: str) -> str | None:
    if not image_path:
        return None

    media_url = imagekit.helper.build_url(
        url_endpoint=app.config["IMAGEKIT_URL_ENDPOINT"],
        src=image_path,
    )

    return media_url


def save_image(image: FileStorage = None, folder: str = None) -> dict[str, str]:
    file = image.stream
    secure_name = secure_filename(image.filename)

    response = imagekit.files.upload(
        file=file,
        file_name=secure_name,
        folder=folder,
        use_unique_file_name=True,
    )

    image_id = response.file_id
    image_path = response.file_path

    return {"image_id": image_id, "image_path": image_path}


def delete_image(image_id: str) -> None:
    imagekit.files.delete(image_id)


@jwt.user_lookup_loader
def user_loader_callback(jwt_header, jwt_data) -> User:
    user_id = jwt_data["sub"]
    return User.get_by_id(user_id)


@jwt.token_in_blocklist_loader
def is_token_in_blocklist(jwt_header, jwt_data) -> bool:
    jti = jwt_data["jti"]
    return RevokedTokenModel.is_blacklisted(jti)


@jwt.token_verification_loader
def verify_token(jwt_header, jwt_data) -> bool:
    user_id = jwt_data["sub"]
    user = User.get_by_id(user_id)

    if not user:
        return False

    return True
