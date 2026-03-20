import logging.config
import os
from typing import Optional

from flask import Flask

from .config import config_options
from .database import db, migrate
from .extensions import api, cache, cors, imagekit, jwt


def create_app(config_name: Optional[str] = None) -> Flask:
    app = Flask(__name__)
    if not config_name:
        config_name = os.getenv("APP_CONFIG", "development")

    config_class = config_options[config_name]

    app.config.from_object(config_class)
    logging.config.dictConfig(config_class.LOGGING)

    init_extensions(app)
    register_blueprints()

    return app


def init_extensions(app: Flask) -> None:
    """Initialize the extensions"""
    jwt.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    imagekit.private_key = app.config["IMAGEKIT_PRIVATE_KEY"]
    cache.init_app(app)


def register_blueprints() -> None:
    """Register the blueprints"""
    from .routes.auth import bp as auth_bp
    from .routes.groups import bp as groups_bp
    from .routes.tags import bp as tags_bp
    from .routes.users import bp as users_bp
    from .routes.events import bp as events_bp
    from .routes.locations import bp as locations_bp

    api.register_blueprint(auth_bp, url_prefix="/auth")
    api.register_blueprint(users_bp, url_prefix="/users")
    api.register_blueprint(groups_bp, url_prefix="/groups")
    api.register_blueprint(tags_bp, url_prefix="/tags")
    api.register_blueprint(events_bp, url_prefix="/events")
    api.register_blueprint(locations_bp, url_prefix="/locations")
