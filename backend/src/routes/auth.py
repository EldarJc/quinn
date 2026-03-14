from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort

from ..database import db
from ..database.models import RevokedTokenModel, User
from ..schemas.auth_schema import (
    LoginSchema,
    TokenSchema,
)
from ..schemas.user_schema import RegisterSchema

bp = Blueprint("Auth", __name__)

login_schema = LoginSchema()
register_schema = RegisterSchema()
token_schema = TokenSchema()


@bp.route("/login")
class Login(MethodView):
    @bp.arguments(login_schema)
    @bp.response(200, token_schema)
    def post(self, user_data):
        username, password = user_data["username"], user_data["password"]
        user = db.session.scalar(db.select(User).where(User.username == username))

        if not user or not user.check_password(password):
            abort(401, message="Invalid username or password")

        tokens = {
            "access_token": create_access_token(
                identity=user.id,
                fresh=True,
                additional_claims={"role": user.role.value},
            ),
            "refresh_token": create_refresh_token(identity=user.id),
        }

        return tokens


@bp.route("/register")
class Register(MethodView):
    @bp.arguments(register_schema)
    @bp.response(201)
    def post(self, user_data):
        user = User.create(**user_data)
        return {"message": "User registered successfully"}


@bp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self):
        jti = get_jwt()["jti"]
        RevokedTokenModel.blocklist_jti(jti)
        db.session.commit()

        return {"message": "Logout successfully!"}


@bp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    @bp.response(200, token_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self):
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)

        jti = get_jwt()["jti"]
        RevokedTokenModel.blocklist_jti(jti)
        db.session.commit()

        tokens = {
            "access_token": create_access_token(
                identity=user_id,
                fresh=False,
                additional_claims={"role": user.role.value},
            ),
            "refresh_token": create_refresh_token(identity=user_id),
        }

        return tokens
