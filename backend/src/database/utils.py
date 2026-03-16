from datetime import datetime, timezone

from flask_smorest import Page
from slugify import slugify

from . import db


class CustomPage(Page):
    @property
    def items(self):
        query = self.collection.offset(self.page_params.first_item).limit(
            self.page_params.page_size
        )
        return db.session.scalars(query).all()

    @property
    def item_count(self):
        query = db.select(db.func.count()).select_from(self.collection.subquery())
        return db.session.scalar(query)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_slug(target, value, oldvalue, initiator) -> None:
    if not value:
        return

    if not target.slug or value != oldvalue:
        target.slug = slugify(value)
