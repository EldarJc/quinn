from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint, abort

from ..database import db
from ..database.models import Event
from ..database.utils import CustomPage
from ..schemas.event_schema import (
    CreateEventSchema,
    EventImageSchema,
    EventSchema,
)
from ..utils import delete_image, save_image

event_schema = EventSchema()
events_schema = EventSchema(many=True)
create_event_schema = CreateEventSchema()
update_event_schema = CreateEventSchema(partial=True)

bp = Blueprint("Event", __name__)


@bp.route("")
class Events(MethodView):
    @bp.response(200, events_schema)
    @bp.paginate(CustomPage, page_size=5)
    def get(self):
        query = db.select(Event)
        return query

    @jwt_required()
    @bp.arguments(create_event_schema)
    @bp.response(200, event_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self, event_data):
        location = event_data.pop("location", {})
        new_event = Event.create(commit=False, owner_id=current_user.id, **event_data)
        new_event.update_location(location)
        new_event.attendees.add(current_user)
        new_event.save()
        return new_event


@bp.route("/<int:event_id>")
class EventUpdate(MethodView):
    @jwt_required()
    @bp.arguments(update_event_schema)
    @bp.response(200, event_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, event_data, event_id):
        event = Event.get_by_id(event_id) or abort(404, message="Event not found")
        if not event.is_owner(current_user.id):
            abort(403, message="You are not the owner of this event")

        location = event_data.pop("location", {})
        event.update(commit=False, **event_data)

        if location:
            event.update_location(location)

        event.save()
        return event


@bp.route("/<int:event_id>/image")
class EventPicture(MethodView):
    @jwt_required()
    @bp.arguments(EventImageSchema, location="files")
    @bp.response(200, event_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def put(self, picture_data, event_id):
        event = Event.get_by_id(event_id) or abort(404, message="Event not found")
        if not event.is_owner(current_user.id):
            abort(403, message="You are not the owner of this event")

        image = picture_data["image"]
        response = save_image(image)
        event.update(**response)

        return event

    @jwt_required()
    @bp.response(200, event_schema)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self, event_id):
        event = Event.get_by_id(event_id) or abort(404, message="Event not found")
        if not event.is_owner(current_user.id):
            abort(403, message="You are not the owner of this event")

        image_id = event.image_id

        if not image_id:
            abort(400, message="No event image to delete.")

        delete_image(image_id)
        event.update(image_id=None, image_path=None)

        return event


@bp.route("/<int:event_id>/memberships")
class EventJoin(MethodView):
    @jwt_required()
    @bp.response(204)
    @bp.doc(security=[{"Bearer Auth": []}])
    def post(self, event_id):
        event = Event.get_by_id(event_id) or abort(404, message="Event not found")

        if not event.is_attendee(current_user.id):
            event.attendees.add(current_user)
            db.session.commit()

        return {}

    @jwt_required()
    @bp.response(204)
    @bp.doc(security=[{"Bearer Auth": []}])
    def delete(self, event_id):
        event = Event.get_by_id(event_id) or abort(404, message="Event not found")

        if event.is_attendee(current_user.id) and not event.is_owner(current_user.id):
            event.attendees.remove(current_user)
            db.session.commit()

        return {}
