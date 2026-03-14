from datetime import datetime, timezone

from slugify import slugify


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_slug(target, value, oldvalue, initiator) -> None:
    if not value:
        return

    if not target.slug or value != oldvalue:
        target.slug = slugify(value)
