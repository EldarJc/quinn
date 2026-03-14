from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class EventType(Enum):
    ONLINE = "online"
    MEETUP = "meetup"
    WORKSHOP = "workshop"
    CONFERENCE = "conference"
    WEBINAR = "webinar"
    TRIP = "trip"
