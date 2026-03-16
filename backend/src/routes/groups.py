from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint, abort

from ..database import db
from ..database.models import Group, Tag
from ..database.utils import CustomPage
from ..schemas.group_schema import (
    CreateGroupSchema,
    GroupImageSchema,
    GroupMemberSchema,
    GroupSchema,
    SearchGroupSchema,
    UpdateGroupSchema,
)
from ..utils import delete_image, save_image

bp = Blueprint("Group", __name__)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
create_group_schema = CreateGroupSchema()
update_group_schema = UpdateGroupSchema(partial=True)
group_image_schema = GroupImageSchema()
group_members_schema = GroupMemberSchema(many=True)


@bp.route("")
class Groups(MethodView):
    @bp.arguments(SearchGroupSchema, location="query")
    @bp.response(200, groups_schema)
    @bp.paginate(CustomPage, page_size=5)
    def get(self, args):
        query = db.select(Group)

        name_search = args.get("name")
        tags = args.get("tags")

        if name_search:
            query = query.where(Group.name.ilike(f"%{name_search}%"))

        if tags:
            query = query.where(Group.tags.any(Tag.name.in_(tags)))

        return query.order_by(Group.id)

    @jwt_required()
    @bp.arguments(create_group_schema)
    @bp.response(201, group_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self, group_data):
        group = Group.create(commit=False, owner_id=current_user.id, **group_data)
        group.members.add(current_user)
        group.save()
        return group


@bp.route("/<string:name>")
class GroupDetails(MethodView):
    @bp.response(200, group_schema)
    def get(self, name):
        group = db.session.scalar(db.select(Group).where(Group.name == name))

        return group or abort(404, message=f"Group {name} not found")


@bp.route("/<int:group_id>")
class GroupUpdate(MethodView):
    @jwt_required()
    @bp.arguments(update_group_schema)
    @bp.response(200, group_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, group_data, group_id):
        group = Group.get_by_id(group_id) or abort(404, message="Group not found")

        if not group.is_owner(current_user.id):
            abort(403, message="You are not the owner of this group")

        return group.update(**group_data)


@bp.route("/<int:group_id>/image")
class GroupImage(MethodView):
    @jwt_required()
    @bp.arguments(group_image_schema, location="files")
    @bp.response(200, group_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, image_data, group_id):
        group = Group.get_by_id(group_id) or abort(404, message="Group not found")

        if not group.is_owner(current_user.id):
            abort(403, message="You are not the owner of this group")

        image = image_data["image"]
        response = save_image(image, "group_images")
        return group.update(**response)

    @jwt_required()
    @bp.response(200, group_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self, group_id):
        group = Group.get_by_id(group_id) or abort(404, message="Group not found")

        if not group.is_owner(current_user.id):
            abort(403, message="You are not the owner of this group")

        image_id = group.image_id

        if not image_id:
            abort(400, message="No group image to delete.")

        delete_image(image_id)

        return group.update(image_id=None, image_path=None)


@bp.route("/<int:group_id>/memberships")
class GroupJoin(MethodView):
    @jwt_required()
    @bp.response(204)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self, group_id):
        group = Group.get_by_id(group_id) or abort(404, message="Group not found")

        if not group.is_member(current_user.id):
            group.members.add(current_user)
            db.session.commit()

        return {}

    @jwt_required()
    @bp.response(204)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self, group_id):
        group = Group.get_by_id(group_id) or abort(404, message="Group not found")

        if group.is_member(current_user.id) and not group.is_owner(current_user.id):
            group.members.remove(current_user)
            db.session.commit()

        return {}
