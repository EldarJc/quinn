from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..database import db
from ..database.models import Tag
from ..database.utils import CustomPage
from ..decorators import admin_required
from ..schemas.tag_schema import CreateTagSchema, TagSchema

bp = Blueprint("Tag", __name__)

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
create_tag_schema = CreateTagSchema()


@bp.route("")
class Tags(MethodView):
    @bp.route("")
    class TagList(MethodView):
        @bp.response(200, TagSchema(many=True))
        @bp.paginate(CustomPage)
        def get(self):
            query = db.select(Tag).order_by(Tag.name)
            return query

    @admin_required()
    @bp.arguments(create_tag_schema)
    @bp.response(200, tag_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self, tag_data):
        tag = Tag.create_tag(**tag_data)
        return tag


@bp.route("/<int:tag_id>")
class DeleteTag(MethodView):
    @admin_required()
    @bp.response(200)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self, tag_id):
        tag = Tag.get_by_id(tag_id) or abort(404, message="Tag not found")
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted successfully"}
