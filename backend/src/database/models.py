from datetime import datetime, timedelta, timezone
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ..constants import EventType, UserRole
from . import db
from .base import BaseModel
from .utils import generate_slug, utc_now

# Association tables

group_tags = sa.Table(
    "group_tags",
    db.metadata,
    sa.Column("group_id", sa.ForeignKey("groups.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)

group_members = sa.Table(
    "group_members",
    db.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("group_id", sa.ForeignKey("groups.id"), primary_key=True),
)

event_tags = sa.Table(
    "event_tags",
    db.metadata,
    sa.Column("event_id", sa.ForeignKey("events.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)

event_attendees = sa.Table(
    "event_attendees",
    db.metadata,
    sa.Column("event_id", sa.ForeignKey("events.id"), primary_key=True),
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
)


# Models


class User(BaseModel):
    __tablename__ = "users"

    image_id: Mapped[Optional[str]]
    image_path: Mapped[Optional[str]]

    role: Mapped[UserRole] = mapped_column(sa.Enum(UserRole), default=UserRole.USER)
    username: Mapped[str] = mapped_column(sa.String(50), index=True, unique=True)
    first_name: Mapped[str] = mapped_column(sa.String(40))
    last_name: Mapped[str] = mapped_column(sa.String(40))
    email: Mapped[str] = mapped_column(sa.String(254), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255))
    bio: Mapped[str] = mapped_column(sa.String(350), default="No bio")

    owned_groups: Mapped[list["Group"]] = relationship(back_populates="owner")
    owned_events: WriteOnlyMapped[list["Event"]] = relationship(back_populates="owner")
    joined_events: WriteOnlyMapped[list["Event"]] = relationship(
        secondary="event_attendees", back_populates="attendees"
    )
    joined_groups: WriteOnlyMapped[list["Group"]] = relationship(
        secondary="group_members", back_populates="members"
    )

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Tag(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(sa.String(100), unique=True)

    events: Mapped[list["Event"]] = relationship(
        secondary=event_tags, back_populates="tags"
    )
    groups: Mapped[list["Group"]] = relationship(
        secondary=group_tags, back_populates="tags"
    )


class Group(BaseModel):
    __tablename__ = "groups"

    image_id: Mapped[Optional[str]]
    image_path: Mapped[Optional[str]]

    name: Mapped[str] = mapped_column(sa.String(100), index=True, unique=True)
    description: Mapped[str] = mapped_column(sa.String(500), default="No description")
    slug: Mapped[str] = mapped_column(sa.String(200))

    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="owned_groups")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=group_tags, back_populates="groups"
    )
    members: WriteOnlyMapped[list["User"]] = relationship(
        secondary="group_members", back_populates="joined_groups"
    )
    events: WriteOnlyMapped[list["Event"]] = relationship(back_populates="group")

    def count_members(self) -> int:
        return db.session.scalar(
            db.select(db.func.count()).select_from(self.members.select().subquery())
        )

    def is_owner(self, user_id: int) -> bool:
        return self.owner_id == user_id

    def is_member(self, user_id: int) -> bool:
        query = sa.select(group_members).where(
            group_members.c.group_id == self.id, group_members.c.user_id == user_id
        )
        return db.session.scalar(query)


sa.event.listen(Group.name, "set", generate_slug, retval=False)


class Event(BaseModel):
    __tablename__ = "events"

    image_id: Mapped[Optional[str]]
    image_path: Mapped[Optional[str]]

    title: Mapped[str] = mapped_column(sa.String(150))
    description: Mapped[str] = mapped_column(sa.Text, default="No description")
    start_date: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    event_type: Mapped[EventType] = mapped_column(sa.Enum(EventType))
    max_attendees: Mapped[Optional[int]]
    slug: Mapped[str] = mapped_column(sa.String(200))

    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    group_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey("groups.id"))

    owner: Mapped["User"] = relationship(back_populates="owned_events")
    group: Mapped[Optional["Group"]] = relationship(back_populates="events")
    attendees: WriteOnlyMapped[list["User"]] = relationship(
        secondary="event_attendees", back_populates="joined_events"
    )
    location: Mapped[Optional["Location"]] = relationship(back_populates="event")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=event_tags, back_populates="events"
    )

    def duration(self) -> timedelta:
        return self.end_date - self.start_date

    def is_owner(self, user_id: int) -> bool:
        return self.owner_id == user_id

    def is_finished(self) -> bool:
        return utc_now() >= self.end_date.astimezone(timezone.utc)

    def count_attendees(self) -> int:
        return db.session.scalar(
            db.select(db.func.count()).select_from(self.attendees.select().subquery())
        )

    def is_full(self) -> bool:
        if self.max_attendees is None:
            return False
        return self.count_attendees() >= self.max_attendees

    def is_attendee(self, user_id: int) -> bool:
        query = sa.select(event_attendees).where(
            event_attendees.c.event_id == self.id, event_attendees.c.user_id == user_id
        )
        return db.session.scalar(query)

    def update_location(self, location_data: dict) -> None:
        if self.location and self.event_type in [EventType.ONLINE, EventType.WEBINAR]:
            db.session.delete(self.location)

        elif self.location and location_data:
            for key, value in location_data.items():
                setattr(self.location, key, value)

        else:
            self.location = (
                Location.create(commit=False, **location_data)
                if location_data
                else None
            )


sa.event.listen(Event.title, "set", generate_slug, retval=False)


class Location(BaseModel):
    __tablename__ = "event_locations"

    country: Mapped[str] = mapped_column(sa.String(100))
    city: Mapped[str] = mapped_column(sa.String(100))
    state: Mapped[str] = mapped_column(sa.String(100))
    address: Mapped[str] = mapped_column(sa.String(255))

    event_id: Mapped[int] = mapped_column(sa.ForeignKey("events.id"), unique=True)

    event: Mapped["Event"] = relationship(back_populates="location")


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(sa.String(120), unique=True)

    @classmethod
    def blocklist_jti(cls, jti) -> None:
        revoked = cls(jti=jti)

        db.session.add(revoked)

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        query = sa.select(cls.id).where(cls.jti == jti)
        return db.session.scalar(query) is not None
